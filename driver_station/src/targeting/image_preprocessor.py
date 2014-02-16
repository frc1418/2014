#
#   This file is part of KwarqsDashboard.
#
#   KwarqsDashboard is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, version 3.
#
#   KwarqsDashboard is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with KwarqsDashboard.  If not, see <http://www.gnu.org/licenses/>.
#


import math
import sys

import cv2
import numpy as np

from common import settings

# using python 2.7, get some python 3 builtins
from future_builtins import zip

import logging
logger = logging.getLogger(__name__)


class ImagePreprocessor(object):

    
    def __init__(self):
        self.size = None
        
        # debug settings        
        self.show_hue = False
        self.show_sat = False
        self.show_val = False
        self.show_bin = False
        self.show_bin_overlay = False
        
        
        # thresholds are not initialized here, someone else does it
    
    def process_image(self, img):
        '''
            Processes an image and thresholds it. Returns the original
            image, and a binary version of the image indicating the area
            that was filtered
            
            :returns: img, bin
        '''
        
        # reinitialize any time the image size changes         
        if self.size is None or self.size[0] != img.shape[0] or self.size[1] != img.shape[1]:
            h, w = img.shape[:2]
            self.size = (h, w)
            
            # these are preallocated so we aren't allocating all the time
            self.bin = np.empty((h, w, 1), dtype=np.uint8)
            self.hsv = np.empty((h, w, 3), dtype=np.uint8)
            self.hue = np.empty((h, w, 1), dtype=np.uint8)
            self.sat = np.empty((h, w, 1), dtype=np.uint8)
            self.val = np.empty((h, w, 1), dtype=np.uint8)
            
            # for overlays
            self.zeros = np.zeros((h, w, 1), dtype=np.bool)
            
            # these settings should be adjusted according to the image size
            # and noise characteristics
            
            # TODO: What's the optimal setting for this? For smaller images, we
            # cannot morph as much, or the features blend into each other. 
            
            # TODO: tune kMinWidth
            
            # Note: if you set k to an even number, the detected
            # contours are offset by some N pixels. Sometimes.
            
            if w <= 320:
                k = 2
                offset = (0,0)
                self.kHoleClosingIterations = 1 # originally 9
                
                self.kMinWidth = 2
                
                # drawing 
                self.kThickness = 1
                self.kTgtThickness = 1 
                
                # accuracy of polygon approximation
                self.kPolyAccuracy = 10.0
                
            elif w <= 480:
                k = 2
                offset = (1,1)
                self.kHoleClosingIterations = 9 # originally 9
                
                self.kMinWidth = 5
                
                # drawing
                self.kThickness = 1
                self.kTgtThickness = 2
                
                # accuracy of polygon approximation
                self.kPolyAccuracy = 15.0
                 
            else:
                k = 3
                offset = (1,1)
                self.kHoleClosingIterations = 6 # originally 9
                
                self.kMinWidth = 10
                
                # drawing
                self.kThickness = 1 
                self.kTgtThickness = 2
                
                # accuracy of polygon approximation
                self.kPolyAccuracy = 20.0
            
            self.morphKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (k,k), anchor=offset)
            
            logging.info("New image size: %sx%s, morph size set to %s, %s iterations", w,h,k, self.kHoleClosingIterations)
        
        # get this outside the loop
        ih, iw = self.size
        centerOfImageY = ih/2.0
        
        # convert to HSV
        cv2.cvtColor(img, cv2.cv.CV_BGR2HSV, self.hsv)
        cv2.split(self.hsv, [self.hue, self.sat, self.val])
        
        # Threshold each component separately
        
        # Hue
        cv2.threshold(self.hue, self.thresh_hue_p, 255, type=cv2.THRESH_BINARY, dst=self.bin)
        cv2.threshold(self.hue, self.thresh_hue_n, 255, type=cv2.THRESH_BINARY_INV, dst=self.hue)
        cv2.bitwise_and(self.hue, self.bin, self.hue)
        
        if self.show_hue:
            # overlay green where the hue threshold is non-zero
            img[np.dstack((self.zeros, self.hue != 0, self.zeros))] = 255
        
        # Saturation
        cv2.threshold(self.sat, self.thresh_sat_p, 255, type=cv2.THRESH_BINARY, dst=self.bin)
        cv2.threshold(self.sat, self.thresh_sat_n, 255, type=cv2.THRESH_BINARY_INV, dst=self.sat)
        cv2.bitwise_and(self.sat, self.bin, self.sat)
        
        if self.show_sat:
            # overlay blue where the sat threshold is non-zero
            img[np.dstack((self.sat != 0, self.zeros, self.zeros))] = 255
        
        # Value
        cv2.threshold(self.val, self.thresh_val_p, 255, type=cv2.THRESH_BINARY, dst=self.bin)
        cv2.threshold(self.val, self.thresh_val_n, 255, type=cv2.THRESH_BINARY_INV, dst=self.val)
        cv2.bitwise_and(self.val, self.bin, self.val)
        
        if self.show_val:
            # overlay red where the val threshold is non-zero
            img[np.dstack((self.zeros, self.zeros, self.val != 0))] = 255
        
        # Combine the results to obtain our binary image which should for the most
        # part only contain pixels that we care about        
        cv2.bitwise_and(self.hue, self.sat, self.bin)
        cv2.bitwise_and(self.bin, self.val, self.bin)

        # Fill in any gaps using binary morphology
        cv2.morphologyEx(self.bin, cv2.MORPH_CLOSE, self.morphKernel, dst=self.bin, iterations=self.kHoleClosingIterations)
        
        #print 'bin',self.show_bin
        if self.show_bin:
            cv2.imshow('bin', self.bin)
        
        # overlay the binarized image on the displayed image, instead of a separate picture
        if self.show_bin_overlay:
            img[np.dstack((self.bin, self.bin, self.bin)) != 0] = 255
            
            
        return img, self.bin
