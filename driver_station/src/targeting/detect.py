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
    
if __name__ == '__main__':
    
    img = cv2.imread('center_18ft_off.jpg')
    cv2.imshow("color", img)
    cv2.waitKey(0)
    # convert to HSV colorspace
    hsv = cv2.cvtColor(img, cv2.cv.CV_BGR2HSV)

    h, s, v = cv2.split(hsv)

    # these parameters will find 'green' on the image
    h = threshold_range(h, 0, 255)
    s = threshold_range(s, 250, 255)
    v = threshold_range(v, 50, 155)
    
    #cv2.imshow("hue only", h)
    #cv2.imshow("saturation only", s)
    #cv2.imshow("value only", v)
    # combine them all and show that
    combined = cv2.bitwise_and(h, cv2.bitwise_and(s, v))
    cv2.imshow('combined', combined)
    
    # store the image for other demo projects
    cv2.imwrite('combined.png', combined)
    
if __name__ == '__main__':
    
    img = cv2.imread('combined.png')
    
    # fill in the holes
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2,2), anchor=(1,1))
    morphed_img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel, iterations=9)
    
    # show it
    cv2.imshow('morphed', morphed_img)
    
    # store that for other demo code
    cv2.imwrite('morphed.png', morphed_img)
    
    cv2.waitKey(0)
    
if __name__ == '__main__':
    
    # the '0' parameter means load a grayscale image
    img = cv2.imread('morphed.png', 0)
   
    # nothing easier
    contours, hierarchy = cv2.findContours(img.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_KCOS)
    #print contours
    
    # draw the found contours on the image
    # -> but you can't show colors on a grayscale image, so convert it to color
    color_img = cv2.cvtColor(img, cv2.cv.CV_GRAY2BGR)
    x = []
    # then draw it
    for contour in contours:
        p = cv2.approxPolyDP(contour, 45, False)
        
        if  cv2.contourArea(contour) >=  40:
            x.append(contour)
            
        elif   cv2.contourArea(contour) < 40:
            continue
    
    x, y, w, h = cv2.boundingRect(contour)
    
    cv2.drawContours(color_img, x, -1, (0,0,255), thickness=2)
    ((centerX, centerY), (rw, rh), rotation) = cv2.minAreaRect(p)

            # sometimes minAreaRect decides to rotate the rectangle too much.
            # detect that and fix it. 
            
    if (w > h and rh < rw) or (h > w and rw < rh):
        rh, rw = rw, rh  # swap
        rotation = -90.0 - rotation    
    verticalTargets = []
    horizontalTargets = []
            
        
    # show it
    cv2.imwrite('contours.png', color_img)
    cv2.imshow('contours', color_img)
  
    cv2.waitKey(0)

    