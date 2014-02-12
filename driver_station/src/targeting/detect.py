'''
Created on Jan 23, 2014

@author: Brice
'''
import cv2
import numpy as np

import sys

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


def ratioToScore (ratio):
    print "ratio", ratio
    print "ratio to score score"
    print 100*(1.0-float(abs(float(1.0-ratio))))
    
    print float(max(0, min(100*(1.0-float(abs(float(1.0-ratio)))), 100.0)))
    return float(max(0, min(100*(1.0-float(abs(1.0-float(ratio)))), 100.0)))

def scoreRectangularity(contour):
    x, y, w, h = cv2.boundingRect(contour)  
    if (float(w) * float(h) != 0):
        return 100* cv2.contourArea(contour)/ w * h
    else:
        return 0

def scoreAspectRatio(bool, width, height):
    #bool used as boolean use 1 for true and 0 for false
    #vertical
    print width
    print"width above"
    print height
    print "height above"
    if (bool == 1):
        idealAspectRatio = 4.0/32
    #horizontal
    elif(bool == 0):
        idealAspectRatio = 23.5/4
    #determine the long and shortsides of the rectangle
    if (float(width) > float(height)):
        
        rectLong = float(width)
        rectShort = float(height)
        print width
    elif(height > width):
        rectLong = float(height)
        rectShort = float(width)
    
    if (width > height):
        aspectRatio = ratioToScore(float(rectLong)/float(rectShort)/float(idealAspectRatio))
    else:
        aspectRatio = aspectRatio = ratioToScore(float(rectShort)/float(rectLong)/float(idealAspectRatio))
        print "aspect ratio"
        print aspectRatio
    return aspectRatio

def scoreCompare(vertical, rectangularity, verticalAspectRatio, horizontalAspectRatio):
    isTarget = True
    rectangularityLimit = 40
    aspectRatioLimit = 55
    isTarget = isTarget and  rectangularity > rectangularityLimit
    if(vertical == True):
        isTarget = isTarget and verticalAspectRatio > aspectRatioLimit
    else:
        isTarget = isTarget and horizontalAspectRatio > aspectRatioLimit
    return isTarget
def hotOrNot(tTapeWidthScore, tVerticalScore, tLeftScore, tRightScore):
    isHot = True
    tape_Width_Limit = 50
    vertical_Score_Limit = 50
    lr_Score_Limit = 50
    isHot = isHot and tTapeWidthScore >= tape_Width_Limit
    print ("tapeWidth")
    print tTapeWidthScore
    isHot = isHot and tVerticalScore >= vertical_Score_Limit
    print "vertical score"
    print tVerticalScore
    isHot = isHot and tLeftScore > lr_Score_Limit or tRightScore >lr_Score_Limit
    print "leftScore"
    print tLeftScore
    print "rightScore"
    print tRightScore
    print "isHot"
    return isHot
    
def process_image(img):
    print img
    cv2.imshow("Starting image", img)
    cv2.waitKey(0)
    # threshold hsv
    hsv = cv2.cvtColor(img, cv2.cv.CV_BGR2HSV)
    h, s, v = cv2.split(hsv)

    # these parameters will find 'green' on the image
    h = threshold_range(h, 0, 255)
    s = threshold_range(s, 150, 255)
    v = threshold_range(v, 100, 170)
    cv2.imshow("v",v)
    #combine them
    combined = cv2.bitwise_and(h, cv2.bitwise_and(s, v))
    cv2.imshow('combined', combined)
    cv2.waitKey(0)
    # fill in the holes
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    morphed_img = cv2.morphologyEx(combined, cv2.MORPH_CLOSE, kernel, iterations=3)
    # analyze particles
    cv2.cvtColor(morphed_img, cv2.cv.CV_GRAY2BGR)
    cv2.imshow("morphed", morphed_img)
    cv2.waitKey(0)
    contours, hierarchy = cv2.findContours(morphed_img.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_KCOS)  
    p = []  
    vertical_targets = []
    horizontal_targets=[] 
    # remove small particles
    # for each particle
    
    
    #contour = contours[i]
    verticalTargetCount = 0
    horizontalTargetCount = 0
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
        cv2.waitKey(0)'''
        #score rectangularity
        rectangularity = scoreRectangularity(contour)
        print"check"
        # score aspect ratio vertical
        verticalAspectRatio = scoreAspectRatio(1, w, h)
        # score aspect ratio horizontal
        horizontalAspectRatio = scoreAspectRatio(0, w, h)
        # determine if horizontal
        if(scoreCompare(False, rectangularity, verticalAspectRatio, horizontalAspectRatio)== True):
            horizontal_targets.append(contour)
            horizontalTargetCount = horizontalTargetCount + 1
        elif(scoreCompare(True, rectangularity, verticalAspectRatio, horizontalAspectRatio)== True):
            vertical_targets.append(contour)
            verticalTargetCount = verticalTargetCount + 1
        # store vertical targets in vertical array, horizontal targets in horizontal array
    # Match up the targets to each other
    #final targets array declaration
    
    
    tTotalScore = tLeftScore = tRightScore = tTapeWidthScore = tVerticalScore = 0.0
    if len(vertical_targets) == 0:
        print "no vertical targets"

    # for each vertical target
    for vertical_target in vertical_targets:
        x, y, w1, h1 = cv2.boundingRect(vertical_target)
        print "check 2"
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
            print"a", a
            print "b", b
            print "w2", w2
            print "h2", h2
            ((centerA, centerB), (rw, rh), rotation) = cv2.minAreaRect(horizontal_target)  
            # sometimes minAreaRect decides to rotate the rectangle too much.
            # detect that and fix it.       
            if (w2 > h2 and rh < rw) or (h > w and rw < rh):
                rh, rw = rw, rh  # swap
                rotation = -90.0 - rotation 
            # determine if horizontal target is in expected location
            # -> to the right
            rightScore = ratioToScore(1.2*(float(centerA) - float(x) - float(w1))/float(w2))
            print "rightScore", rightScore
            print"x", x
            print "centerA", centerA
            print "w1", w1
            print "w2", w2
            # -> to the left
            leftScore = ratioToScore(1.2*(float(x) - float(centerA))/ float(w2))                   
            print "leftScore", leftScore  
            print "centerA", centerA 
            print"w2", w2
            print "x", x
            # determine if the tape width is the same
            tapeWidthScore =ratioToScore(float(w1)/float(h2))
            # determine if vertical location of horizontal target is correct
            '''somthing is messed up so if statement requirement is not met trying to figure out the problem now'''
            verticalScore = ratioToScore(1.0-(float(y) - centerB)/(4.0*h2))
            total = max(leftScore,rightScore)
            total = total + tapeWidthScore + verticalScore
            print "tape Width score", tapeWidthScore
            print w1,   w2
            print "vertical score", verticalScore
            print "total", total
            # if the targets match up enough, store it in an array of potential matches
            print "tTotalSCore", tTotalScore
            if (total >= tTotalScore):
                tHorizontalIndex = horizontal_target
                print ("horizontal_target")
                print horizontal_target
                tVerticalIndex = vertical_target
                print ("vertical_target")
                print vertical_target
                tTotalScore = total
                print ("total")
                print total
                tLeftScore = leftScore
                print ("left score")
                print leftScore
                tRightScore = rightScore
                print ("rightScore")
                print (rightScore)
                tTapeWidthScore = tapeWidthScore
                
                tVerticalScore = verticalScore
                
            else:
                continue
            
            # for the potential matched targets
            possibleHTarget = hotOrNot(tTapeWidthScore, tVerticalScore, tLeftScore, tRightScore)
            print(tTapeWidthScore, tVerticalScore, tLeftScore, tRightScore)
        # determine if the target is hot or not
        if len(horizontal_targets) == 0:
            possibleHTarget = False
        if(verticalTargetCount > 0):
            if(possibleHTarget == True):
                print ("hot target Located")
                 
            elif(possibleHTarget == False):
                print ("hot target not Located")
            
        # determine the best target
        
    # print out the data or something. 
    if (len(horizontal_targets) != 0):
        cv2.drawContours(img, (tHorizontalIndex, tVerticalIndex), -1, (44,0,232), thickness=2) 
        cv2.imshow('all contours', img)    
        cv2.waitKey(0)
   

    
if __name__ == '__main__':
    
    if len(sys.argv) != 2:
        #print "Usage: %s image" % (sys.argv[0])
        exit(1)   
    
    img = cv2.imread(sys.argv[1])
    process_image(img)