'''
    This tries to demonstrate tracking an object shown on your webcam. It
    works with some types of objects in particular lighting conditions. 
    
    Usage:
    
        Click twice on the webcam image, and that will define a rectangular 
        area to be tracked. The area as tracked will be displayed on the
        screen when detected.
    
    Currently not optimized at all. Derived from the find_obj.py sample
    demo included with OpenCV
'''

#
# Derived from find_obj.py sample demo
#

import cv2
import numpy as np

# flann enum params are missing
FLANN_INDEX_KDTREE = 1  # bug: flann enums are missing
FLANN_INDEX_KMEANS = 2
FLANN_INDEX_COMPOSITE = 3
FLANN_INDEX_KDTREE_SINGLE = 4
FLANN_INDEX_HIERARCHICAL = 5
FLANN_INDEX_LSH    = 6
FLANN_INDEX_AUTOTUNED = 255

class DemoGoalie(object):
    
    def __init__(self, vc):
        self.vc = vc
        
        self.reset()
        
        # TODO: various types of detectors are available
        #self.detector = cv2.SIFT()
        self.detector = cv2.SURF(800)
        
        # TODO: various types of matchers available..
        #flann_args = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
        #flann_args = dict(algorithm=FLANN_INDEX_LSH,
        #                  table_number=6,
        #                  key_size=12,
        #                  multi_probe_level=1)
        
        #flann_args = dict(algorithm=FLANN_INDEX_AUTOTUNED)
        #self.matcher = cv2.FlannBasedMatcher(flann_args, {})
        
        #self.matcher = cv2.BFMatcher(cv2.NORM_HAMMING)
        
        self.matcher = cv2.BFMatcher(cv2.NORM_L2)
        
        
    def reset(self):
        self.click1 = None
        self.click2 = None
        self.drag = None
        self.keypoints = None
        
    
    # do something with the matches. why?
    
    def define_interesting_features(self, img, coordinates):
        
        (x1, y1), (x2, y2) = coordinates
        self.feature_shape = [y2-y1, x2-x1]
        self.feature_offset = (x1, y1)
        
        # this is broken, support malformed rectangles
        mask = np.zeros(shape=(img.shape[0], img.shape[1]), dtype=np.uint8)
        mask[y1:y2, x1:x2] = 255
        
        self.keypoints, self.descriptors = self.detector.detectAndCompute(img, mask)
        
        if self.descriptors is None or len(self.descriptors) == 0:
            self.reset()
            return
        
        new_image = cv2.drawKeypoints(img, self.keypoints)
        cv2.imshow("Interest", new_image[y1:y2, x1:x2, :])
        
        print "%s keypoints found" % (len(self.keypoints))
        
        
    def filter_matches(self, kp1, kp2, matches, ratio = 0.75):
        '''From find_obj.py'''
        mkp1, mkp2 = [], []
        for m in matches:
            if len(m) == 2 and m[0].distance < m[1].distance * ratio:
                m = m[0]
                mkp1.append( kp1[m.queryIdx] )
                mkp2.append( kp2[m.trainIdx] )
        p1 = np.float32([kp.pt for kp in mkp1])
        p2 = np.float32([kp.pt for kp in mkp2])
        kp_pairs = zip(mkp1, mkp2)
        return p1, p2, kp_pairs
        
        
    def match(self, img):
        '''From find_obj.py'''
        
        kps, desc = self.detector.detectAndCompute(img, None)
        
        # don't try to match when there's nothing to match against
        if desc is None or len(desc) == 0:
            return
        
        # errors happen here depending on the algorithm parameters for flann. Not sure why.
        try:  
            raw_matches = self.matcher.knnMatch(self.descriptors, desc, k=2)
        except cv2.error:
            return
            
        p1, p2, kp_pairs = self.filter_matches(self.keypoints, kps, raw_matches)
        
        # this allows us to transform the matched item if it has moved in 3d space 
        if len(p1) >= 4:
            H, status = cv2.findHomography(p1, p2, cv2.RANSAC, 5.0)
        else:
            H, status = None, None
   
        self.draw_matches(img, kp_pairs, status, H)
        
    def draw_matches(self, img, kp_pairs, status, H):
        '''Derived from find_obj.py'''
        
        vis = img

        h, w = self.feature_shape[:2]
        
        if H is not None:   
            corners = np.float32([[0, 0], [w, 0], [w, h], [0, h]]) + self.feature_offset
            corners = np.int32( cv2.perspectiveTransform(corners.reshape(1, -1, 2), H).reshape(-1, 2))
            cv2.polylines(vis, [corners], True, (255, 255, 255))
    
        if status is None:
            status = np.ones(len(kp_pairs), np.bool_)
            
        p2 = np.int32([kpp[1].pt for kpp in kp_pairs])
    
        green = (0, 255, 0)
        red = (0, 0, 255)
        
        for (x2, y2), inlier in zip(p2, status):
            if inlier:
                col = green
                cv2.circle(vis, (x2, y2), 2, col, -1)
            else:
                col = red
                r = 2
                thickness = 3
                cv2.line(vis, (x2-r, y2-r), (x2+r, y2+r), col, thickness)
                cv2.line(vis, (x2-r, y2+r), (x2+r, y2-r), col, thickness)

        
    
    def onmouse(self, event, x, y, flags, param):

        self.drag = (x, y)
        
        if flags & cv2.EVENT_FLAG_LBUTTON:
            if self.click1 is None:
                self.click1 = (x, y)
            elif self.click2 is None:
                self.click2 = (x, y)
                
    
    def process_video(self):
        
        cv2.namedWindow('Webcam')
        cv2.setMouseCallback('Webcam', self.onmouse)
        
        while cv2.waitKey(30) <= 0:
            success, img = self.vc.read()
            if not success:
                break
            
            if self.keypoints is None:
                
                # wait for the user to define the keypoints
            
                if self.click1 is not None:
                    if self.click2 is not None:
                        
                        # extract rectangle, start finding matches
                        self.define_interesting_features(img, (self.click1, self.click2))
                        
                        
                    elif self.drag is not None:
                        cv2.rectangle(img, self.click1, self.drag, (255, 0 ,0) )
                        
                kp,desc = self.detector.detectAndCompute(img, None)
                img = cv2.drawKeypoints(img, kp)
                        
            else:
                
                # do matching in realtime and display the results
                # - might need to do some buffering to make this work
                self.match(img)
            
            
            cv2.imshow("Webcam", img)


if __name__ == '__main__':
    
    vc = cv2.VideoCapture()
    
    if not vc.open(0):
        print "Could not connect to webcam"
        exit(1)
        
    demo = DemoGoalie(vc)
    demo.process_video()
    
