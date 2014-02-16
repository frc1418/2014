'''
Created on Jan 23, 2014

@author: Brice
'''
import cv2
import numpy as np

import sys

from image_preprocessor import ImagePreprocessor

class BackDetector(object):
    '''
        Detects objects in the back of the robot... which is what's pointing
        at the hot goal when the autonomous mode starts
    '''
    
    def __init__(self):
        self.preprocessor = ImagePreprocessor()
    
        # each of these attributes that start with show_ will be 
        # turned into booleans
        self.show_test = (True, 'Test setting')
    
    def ratioToScore (self, ratio):
        return float(max(0, min(100*(1.0-float(abs(1.0-float(ratio)))), 100.0)))
    
    def scoreRectangularity(self, contour):
        x, y, w, h = cv2.boundingRect(contour)  
        if float(w) * float(h) != 0:
            return 100* cv2.contourArea(contour)/(w * h)
        else:
            return 0
    
    def scoreAspectRatio(self, width, height, vertical):
        
        if vertical:
            idealAspectRatio = 4.0/32.0
        else:
            idealAspectRatio = 23.5/4.0
            
        #determine the long and shortsides of the rectangle
        
        if float(width) > float(height):
            rectLong = float(width)
            rectShort = float(height)
        elif(height >= width):
            rectLong = float(height)
            rectShort = float(width)
        
        if width > height:
            aspectRatio = self.ratioToScore(float(rectLong)/float(rectShort)/float(idealAspectRatio))
        else:
            aspectRatio = self.ratioToScore(float(rectShort)/float(rectLong)/float(idealAspectRatio))
            
        return aspectRatio
    
    def scoreCompare(self, vertical, rectangularity, verticalAspectRatio, horizontalAspectRatio):
        isTarget = True
        
        rectangularityLimit = 40
        aspectRatioLimit = 55
        
        isTarget = isTarget and rectangularity > rectangularityLimit
        if vertical == True:
            isTarget = isTarget and verticalAspectRatio > aspectRatioLimit
        else:
            isTarget = isTarget and horizontalAspectRatio > aspectRatioLimit
            
        return isTarget
    
    def hotOrNot(self, tTapeWidthScore, tVerticalScore, tLeftScore, tRightScore):
        isHot = True
        
        tape_Width_Limit = 50
        vertical_Score_Limit = 50
        lr_Score_Limit = 50
        
        isHot = isHot and tTapeWidthScore >= tape_Width_Limit
        isHot = isHot and tVerticalScore >= vertical_Score_Limit
        isHot = isHot and (tLeftScore > lr_Score_Limit or tRightScore > lr_Score_Limit)
        
        return isHot
        
    def process_image(self, img):
       
       
        p = []  
        vertical_targets = []
        horizontal_targets=[]
        
        isHot = False
        
        tHorizontalIndex = None
        tVerticalIndex = None
        
        #contour = contours[i]
        verticalTargetCount = 0
        horizontalTargetCount = 0
       
        img, processed_img = self.preprocessor.process_image(img)
       
        contours, hierarchy = cv2.findContours(processed_img.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_KCOS)
        
        for contour in contours:
            #p = cv2.approxPolyDP(contour, 45, False)
        # filtering smaller contours from pictures
            if  cv2.contourArea(contour) >=  40:
                p.append(contour)
            
            elif   cv2.contourArea(contour) < 40:
                continue
            #getting lengths of sides of rectangle around the contours
            x, y, w, h = cv2.boundingRect(contour)
            
            
            
            
            '''if (w > h):
                horizontal_targets.append(contour)
            elif (h > w):
                vertical_targets.append(contour)'''
                
            '''conto = morphed_img
            
            
             
            cv2.imshow('contours', conto)
            '''
                
            #score rectangularity
            rectangularity = self.scoreRectangularity(contour)
            #print"check"
            # score aspect ratio vertical
            verticalAspectRatio = self.scoreAspectRatio(w, h, vertical=True)
            # score aspect ratio horizontal
            horizontalAspectRatio = self.scoreAspectRatio(w, h, vertical=False)
            # determine if horizontal
            if(self.scoreCompare(False, rectangularity, verticalAspectRatio, horizontalAspectRatio)== True):
                horizontal_targets.append(contour)
                horizontalTargetCount = horizontalTargetCount + 1
            elif(self.scoreCompare(True, rectangularity, verticalAspectRatio, horizontalAspectRatio)== True):
                vertical_targets.append(contour)
                verticalTargetCount = verticalTargetCount + 1
            # store vertical targets in vertical array, horizontal targets in horizontal array
        # Match up the targets to each other
        #final targets array declaration
        
        
        tTotalScore = tLeftScore = tRightScore = tTapeWidthScore = tVerticalScore = 0.0
        #if len(vertical_targets) == 0:
        #    print "no vertical targets"
    
        # for each vertical target
        for vertical_target in vertical_targets:
            x, y, w1, h1 = cv2.boundingRect(vertical_target)
            #print "check 2"
            ((centerX, centerY), (rw, rh), rotation) = cv2.minAreaRect(vertical_target)  
            # sometimes minAreaRect decides to rotate the rectangle too much.
                # detect that and fix it.       
            if (w1 > h1 and rh < rw) or (h1 > w1 and rw < rh):
                    rh, rw = rw, rh  # swap
                    rotation = -90.0 - rotation
            # for each horizontal target
            
            for horizontal_target in horizontal_targets:
                # measure equivalent rectangle sides
                a, b, w2, h2 = cv2.boundingRect(horizontal_target)
                #print"a", a
                #print "b", b
                #print "w2", w2
                #print "h2", h2
                ((centerA, centerB), (rw, rh), rotation) = cv2.minAreaRect(horizontal_target)  
                # sometimes minAreaRect decides to rotate the rectangle too much.
                # detect that and fix it.       
                if (w2 > h2 and rh < rw) or (h > w and rw < rh):
                    rh, rw = rw, rh  # swap
                    rotation = -90.0 - rotation 
                # determine if horizontal target is in expected location
                # -> to the right
                rightScore = self.ratioToScore(1.2*(float(centerA) - float(x) - float(w1))/float(w2))
                #print "rightScore", rightScore
                #print"x", x
                #print "centerA", centerA
                #print "w1", w1
                #print "w2", w2
                # -> to the left
                leftScore = self.ratioToScore(1.2*(float(x) - float(centerA))/ float(w2))                   
                #print "leftScore", leftScore  
                #print "centerA", centerA 
                #print"w2", w2
                #print "x", x
                # determine if the tape width is the same
                tapeWidthScore = self.ratioToScore(float(w1)/float(h2))
                # determine if vertical location of horizontal target is correct
                '''somthing is messed up so if statement requirement is not met trying to figure out the problem now'''
                verticalScore = self.ratioToScore(1.0-(float(y) - centerB)/(4.0*h2))
                total = max(leftScore,rightScore)
                total = total + tapeWidthScore + verticalScore
                #print "tape Width score", tapeWidthScore
                #print w1,   w2
                #print "vertical score", verticalScore
                #print "total", total
                # if the targets match up enough, store it in an array of potential matches
                #print "tTotalSCore", tTotalScore
                if (total >= tTotalScore):
                    tHorizontalIndex = horizontal_target
                    #print ("horizontal_target")
                    #print horizontal_target
                    tVerticalIndex = vertical_target
                    #print ("vertical_target")
                    #print vertical_target
                    tTotalScore = total
                    #print ("total")
                    #print total
                    tLeftScore = leftScore
                    #print ("left score")
                    #print leftScore
                    tRightScore = rightScore
                    #print ("rightScore")
                    #print (rightScore)
                    tTapeWidthScore = tapeWidthScore
                    
                    tVerticalScore = verticalScore
                    
                else:
                    continue
                
                # for the potential matched targets
                possibleHTarget = self.hotOrNot(tTapeWidthScore, tVerticalScore, tLeftScore, tRightScore)
                print(tTapeWidthScore, tVerticalScore, tLeftScore, tRightScore)
            # determine if the target is hot or not
            if len(horizontal_targets) == 0:
                possibleHTarget = False
            if(verticalTargetCount > 0):
                if(possibleHTarget == True):
                    print ("hot target Located")
                    isHot = True
                     
                elif(possibleHTarget == False):
                    print ("hot target not Located")
                    isHot = False
                
            # determine the best target
            
        # print out the data or something. 
        if (len(horizontal_targets) != 0):
            if tHorizontalIndex is not None:
                cv2.drawContours(img, [tHorizontalIndex,], -1, (44,0,232), thickness=2) 
            if tVerticalIndex is not None:
                cv2.drawContours(img, [tVerticalIndex,], -1, (44,0,232), thickness=2) 
            #cv2.imshow('all contours', img)    
            
   
        # TODO: return data for targeting and stuff
        return img, isHot

    
if __name__ == '__main__':
    
    if len(sys.argv) != 2:
        print "Usage: %s image" % (sys.argv[0])
        exit(1)   
    
    img = cv2.imread(sys.argv[1])
    
    detector = BackDetector()
    detector.process_image(img)
    
