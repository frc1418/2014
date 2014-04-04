#
#    This file is part of Team 1418 Dashboard
#
#    Team 1418 Dashboard is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, version 3.
#
#    Team 1418 Dashboard is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Team 1418 Dashboard.  If not, see <http://www.gnu.org/licenses/>.
#


import cv2
import numpy as np

import sys

from image_preprocessor import ImagePreprocessor

class BackDetector(object):
    '''
        Detects objects in the back of the robot... which is what's pointing
        at the hot goal when the autonomous mode starts
        
        This code is essentially a translation of the 2014 Vision Sample 
        into OpenCV/Python
    '''
    
    def __init__(self):
        self.preprocessor = ImagePreprocessor()
    
        # each of these attributes that start with show_ will be 
        # turned into booleans
        self.show_contours = (False, 'Show all found contours')
        self.show_toosmall = (False, 'Show too small contours')
        self.show_horizontal = (True, 'Show horizontal targets')
        self.show_vertical = (True, 'Show vertical targets')
        
        self.show_aspect = (False, 'Show aspect ratios')
        self.show_rectangularity = (False, 'Show rectangularity')
        
        self.show_hot = (True, 'Show hot targets')
        self.show_hot_text = (True, 'Show hot text')
    
    def ratioToScore (self, ratio):
        return float(max(0, min(100.0*(1.0-float(abs(1.0-float(ratio)))), 100.0)))
    
    def scoreRectangularity(self, contour):
        x, y, w, h = cv2.boundingRect(contour)  
        if float(w) * float(h) != 0:
            return 100.0* cv2.contourArea(contour)/(w * h)
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
        
        
        #rectangularityLimit = 40
        #aspectRatioLimit = 55
        
        # on a smaller image, I'm willing to fudge a bit
        rectangularityLimit = 30
        aspectRatioLimit = 40
        
        
        isTarget = isTarget and rectangularity > rectangularityLimit
        if vertical == True:
            isTarget = isTarget and verticalAspectRatio > aspectRatioLimit
        else:
            isTarget = isTarget and horizontalAspectRatio > aspectRatioLimit
            
        return isTarget
    
    def hotOrNot(self, tTapeWidthScore, tVerticalScore, tLeftScore, tRightScore):
        isHot = True
        
        tape_Width_Limit = 10
        vertical_Score_Limit = 50
        lr_Score_Limit = 50
        
        isHot = isHot and tTapeWidthScore >= tape_Width_Limit
        isHot = isHot and tVerticalScore >= vertical_Score_Limit
        isHot = isHot and (tLeftScore > lr_Score_Limit or tRightScore > lr_Score_Limit)
        
        return isHot
            
    def print_text(self, img, text, x, y, color=(255,255,255)):
        # TODO: could do some fancy layout here.. 
        cv2.putText(img, text, (int(x+5),int(y+5)), cv2.FONT_HERSHEY_PLAIN, 2, color, bottomLeftOrigin=False)
        
    def minAreaRect(self, contour):
        
        x, y, w, h = cv2.boundingRect(contour)
        ((cx, cy), (rw, rh), rotation) = cv2.minAreaRect(contour)  
            
        # sometimes minAreaRect decides to rotate the rectangle too much.
        # detect that and fix it.       
        if (w > h and rh < rw) or (h > w and rw < rh):
            rh, rw = rw, rh  # swap
            rotation = -90.0 - rotation
            
        return (x, y, w, h, cx, cy, rw, rh, rotation)
        
        
    def process_image(self, img):
       
       
        p = []  
        vertical_targets = []
        horizontal_targets=[]
        
        show_toosmall = self.show_toosmall
        toosmall = []
        
        isHotLeft = False
        isHotRight = False
        
        # colors
        FOUND_CONTOURS = (0,255,255)
        TOOSMALL_CONTOURS = (255, 0, 255)
        HORIZ_CONTOURS = (255, 255, 0)
        VERTICAL_CONTOURS = (255, 0, 0)
        
        #IDENTIFIED_COLOR = (44,0,232)
        HOT_COLOR = (0, 0, 255) 
       
        img, processed_img = self.preprocessor.process_image(img)
       
        contours, hierarchy = cv2.findContours(processed_img.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_KCOS)
        
        if self.show_contours:
            cv2.drawContours(img, contours, -1, FOUND_CONTOURS, thickness=1)
        
        
        for contour in contours:
            #p = cv2.approxPolyDP(contour, 45, False)
            
            # filtering smaller contours from pictures
            if cv2.contourArea(contour) >=  40:
                p.append(contour)
            
            elif cv2.contourArea(contour) < 40:
                if show_toosmall:
                    toosmall.append(contour)
                continue
            
            #getting lengths of sides of rectangle around the contours
            x, y, w, h, cx, cy, rw, rh, rotation = self.minAreaRect(contour)
                
            #score rectangularity
            rectangularity = self.scoreRectangularity(contour)
            
            # score aspect ratio vertical
            verticalAspectRatio = self.scoreAspectRatio(w, h, vertical=True)
            # score aspect ratio horizontal
            horizontalAspectRatio = self.scoreAspectRatio(w, h, vertical=False)
            # determine if horizontal
            
            if self.show_rectangularity:
                self.print_text(img, '%.1f' % (rectangularity), cx, cy)
            
            if self.show_aspect:
                self.print_text(img, '%.1f, %.1f' % (verticalAspectRatio, horizontalAspectRatio), cx, cy)
                
            
            if self.scoreCompare(False, rectangularity, verticalAspectRatio, horizontalAspectRatio):
                horizontal_targets.append(contour)
            elif self.scoreCompare(True, rectangularity, verticalAspectRatio, horizontalAspectRatio):
                vertical_targets.append(contour)
            # store vertical targets in vertical array, horizontal targets in horizontal array
        # Match up the targets to each other
        #final targets array declaration
        
        if show_toosmall:
            cv2.drawContours(img, toosmall, -1, TOOSMALL_CONTOURS, thickness=1)
        
        if self.show_horizontal:
            cv2.drawContours(img, horizontal_targets, -1, HORIZ_CONTOURS, thickness=1)
            
        if self.show_vertical:
            cv2.drawContours(img, vertical_targets, -1, VERTICAL_CONTOURS, thickness=1)
        
        #tTotalScore = tLeftScore = tRightScore = tTapeWidthScore = tVerticalScore = 0.0
        hotTargets = []
    
        # for each vertical target
        for vertical_target in vertical_targets:
            x1, y1, w1, h1, cx1, cy1, rw, rh, rotation = self.minAreaRect(vertical_target)

            # for each horizontal target            
            for horizontal_target in horizontal_targets:
                # measure equivalent rectangle sides
                
                x2, y2, w2, h2, cx2, cy2, rw, rh, rotation = self.minAreaRect(horizontal_target)
                
                #a, b, w2, h2 = cv2.boundingRect(horizontal_target)
                    
                # determine if horizontal target is in expected location
                # -> to the right
                rightScore = self.ratioToScore(1.2*(float(cx2) - float(x1) - float(w1))/float(w2))

                # -> to the left
                leftScore = self.ratioToScore(1.2*(float(x1) - float(cx2))/ float(w2))                   

                # determine if the tape width is the same
                tapeWidthScore = self.ratioToScore(float(w1)/float(h2))
                
                # determine if vertical location of horizontal target is correct
                verticalScore = self.ratioToScore(1.0-(float(y2) - cy2)/(4.0*h2))
                total = max(leftScore,rightScore)
                total = total + tapeWidthScore + verticalScore

                # if the targets match up enough, store it in an array of potential matches
                #if (total >= tTotalScore):
                #    tHorizontalIndex = horizontal_target
                #    tVerticalIndex = vertical_target
                #    tTotalScore = total
                #    tLeftScore = leftScore
                #    tRightScore = rightScore
                #    tTapeWidthScore = tapeWidthScore
                    
                #    tVerticalScore = verticalScore
                    
                #else:
                #    continue
                
                # for the potential matched targets
                #possibleHTarget = self.hotOrNot(tTapeWidthScore, tVerticalScore, tLeftScore, tRightScore)
                #print(tTapeWidthScore, tVerticalScore, tLeftScore, tRightScore)
            
                #
                # actually, the best target doesn't matter. just determine whether
                # it's hot to the left or hot to the right. That's all we *really* care about
                #
            
                if self.hotOrNot(tapeWidthScore, verticalScore, leftScore, rightScore):
                    if rightScore > leftScore:
                        isHotLeft = True
                        
                        if self.show_hot_text:
                            self.print_text(img, "R", cx2, cy1, HOT_COLOR)
                        
                    else:
                        
                        if self.show_hot_text:
                            self.print_text(img, "L", cx1, cy2, HOT_COLOR)
                        
                        isHotRight = True
                    
                    # TODO: left/right?
                    hotTargets.append(horizontal_target)
                    hotTargets.append(vertical_target)
            
            # determine if the target is hot or not
            #if len(horizontal_targets) == 0:
            #    possibleHTarget = False
                
            #if len(vertical_targets) > 0:
            #    if possibleHTarget == True:
            #        print ("hot target Located")
            #        isHot = True
                     
            #    elif possibleHTarget == False:
            #        print ("hot target not Located")
            #        isHot = True
                
            # determine the best target
            
        if self.show_hot:
            cv2.drawContours(img, hotTargets, -1, HOT_COLOR, thickness=1)
            
        # print out the data or something. 
        #if (len(horizontal_targets) != 0):
        #    if tHorizontalIndex is not None:
        #        cv2.drawContours(img, [tHorizontalIndex,], -1, IDENTIFIED_COLOR, thickness=1) 
        #    if tVerticalIndex is not None:
        #        cv2.drawContours(img, [tVerticalIndex,], -1, IDENTIFIED_COLOR, thickness=1)     
            
   
        # TODO: return data for targeting and stuff
        return img, (isHotRight, isHotLeft)

    
if __name__ == '__main__':
    
    if len(sys.argv) != 2:
        print "Usage: %s image" % (sys.argv[0])
        exit(1)   
    
    img = cv2.imread(sys.argv[1])
    
    detector = BackDetector()
    detector.process_image(img)
    
