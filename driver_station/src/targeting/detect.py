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
    return (max(0, min(100*(1-abs(1-ratio)), 100)))
def process_image(img):
    
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
    
    
    #    contour = contours[i]
    
    for contour in contours:
        #p = cv2.approxPolyDP(contour, 45, False)
    # filtering smaller contours from pictures
        if  cv2.contourArea(contour) >=  40:
            p.append(contour)
        
        elif   cv2.contourArea(contour) < 40:
            continue
        #getting lenghts of sides of rectangle around the contours
        x, y, w, h = cv2.boundingRect(contour)
        
        if (w > h):
            horizontal_targets.append(contour)
        elif (h > w):
            vertical_targets.append(contour)
            
    conto = morphed_img
    cv2.drawContours(conto, vertical_targets, -1, (44,0,232), thickness=2) 
    cv2.imshow('h identify', conto)    
    cv2.waitKey(0)
    
    ''' 
    cv2.imshow('contours', conto)
    cv2.waitKey(0)
    
    # score rectangularity
    
    ((centerX, centerY), (rw, rh), rotation) = cv2.minAreaRect(p)  
    # sometimes minAreaRect decides to rotate the rectangle too much.
            # detect that and fix it.       
    if (w > h and rh < rw) or (h > w and rw < rh):
        rh, rw = rw, rh  # swap
        rotation = -90.0 - rotation'''
        # score aspect ratio vertical
        
        # score aspect ratio horizontal
        
        # determine if horizontal
        
        # store vertical targets in vertical array, horizontal targets in horizontal array
        
    # 
    # Match up the targets to each other
    #final targets array declaration
    
        
    # for each vertical target
    for vertical_target in vertical_targets:
        x, y, w1, h1 = cv2.boundingRect(vertical_target)
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
            ((centerA, centerB), (rw, rh), rotation) = cv2.minAreaRect(horizontal_target)  
    # sometimes minAreaRect decides to rotate the rectangle too much.
            # detect that and fix it.       
            if (w2 > h2 and rh < rw) or (h > w and rw < rh):
                rh, rw = rw, rh  # swap
                rotation = -90.0 - rotation 
            # determine if horizontal target is in expected location
            # -> to the right
            rightScore = ratioToScore(1.2*(centerX - x - w1)/w2)
            # -> to the left
            leftScore = ratioToScore(1.2*(x - centerA)/ w2)
                
            # determine if the tape width is the same
            tapeWidthScore =ratioToScore(w1/h2)
            # determine if vertical location of horizontal target is correct
            verticalScore = ratioToScore(1-(w1 - centerB)/(4*h2))
            total = max(leftScore,rightScore)
            total = total + tapeWidthScore + verticalScore
            # if the targets match up enough, store it in an array of potential matches
            if (total > target
    
    # for the potential matched targets
    
        # determine if the target is hot or not
    
        # determine the best target
        
    
    # print out the data or something. 
    
    

    
if __name__ == '__main__':
    
    if len(sys.argv) != 2:
        print "Usage: %s image" % (sys.argv[0])
        exit(1)
        
    
    img = cv2.imread(sys.argv[1])
    process_image(img)
    
    
