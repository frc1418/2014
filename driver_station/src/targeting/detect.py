'''
Created on Jan 23, 2014

@author: Brice
'''
import cv2
import numpy as np

def binarize(im):
    '''Turn into white any portion of the image that is not zero'''
    new = np.zeros_like(im, dtype=np.uint8)
    new[im > 1] = 255
    return new


def threshold_range(im, lo, hi):
    '''Returns a binary image if the values are between a certain value'''
    
    unused, t1 = cv2.threshold(im, lo, 255, type=cv2.THRESH_BINARY)
    unused, t2 = cv2.threshold(im, hi, 255, type=cv2.THRESH_BINARY_INV)
    return cv2.bitwise_and(t1, t2)


def process_image(img):
    
    cv2.imshow("Starting image", img)
    cv2.waitKey(0)
    # threshold hsv
    hsv = cv2.cvtColor(img, cv2.cv.CV_BGR2HSV)
    h, s, v = cv2.split(img)

    # these parameters will find 'green' on the image
    h = threshold_range(h, 0, 255)
    s = threshold_range(s, 250, 255)
    v = threshold_range(v, 50, 155)
    #combine them
    combined = cv2.bitwise_and(h, cv2.bitwise_and(s, v))
    # store the image for other demo projects
    cv2.imwrite('combined.png', combined)
    
    img = cv2.imread('combined.png')
    
    # fill in the holes
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2,2), anchor=(1,1))
    morphed_img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel, iterations=9)
    cv2.imwrite('morphed.png', morphed_img)
    img = cv2.imread('morphed.png', 0)
    # analyze particles
    contours, hierarchy = cv2.findContours(img.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_KCOS)
    color_img = cv2.cvtColor(img, cv2.cv.CV_GRAY2BGR)  
    p = []   
    # remove small particles
    # for each particle
    for contour in contours:
            #p = cv2.approxPolyDP(contour, 45, False)
        
            if  cv2.contourArea(contour) >=  40:
                p.append(contour)
            
            elif   cv2.contourArea(contour) < 40:
                continue
    cv2.drawContours(color_img, p, -1, (0,0,255), thickness=2)
   

        # score rectangularity
    x, y, w, h = cv2.boundingRect(contour)    
    ((centerX, centerY), (rw, rh), rotation) = cv2.minAreaRect(p)  
    # sometimes minAreaRect decides to rotate the rectangle too much.
            # detect that and fix it. 
            
    if (w > h and rh < rw) or (h > w and rw < rh):
        rh, rw = rw, rh  # swap
        rotation = -90.0 - rotation
        # score aspect ratio vertical
        
        # score aspect ratio horizontal
        
        # determine if horizontal
        
        # store vertical targets in vertical array, horizontal targets in horizontal array
        
    # 
    # Match up the targets to each other
    #
        
    # for each vertical target
    
        # for each horizontal target
        
            # measure equivalent rectangle sides
            
            # determine if horizontal target is in expected location
            # -> to the right
            # -> to the left
            
            # determine if the tape width is the same
            
            # determine if vertical location of horizontal target is correct
            
            # if the targets match up enough, store it in an array of potential matches
            
    
    # for the potential matched targets
    
        # determine if the target is hot or not
    
        # determine the best target
        
    
    # print out the data or something. 
    
    

    
if __name__ == '__main__':
    
    img = cv2.imread('C:\Users\Brice\Desktop\VisionImages\2014 Vision Target')
    process_image(img)
    
    