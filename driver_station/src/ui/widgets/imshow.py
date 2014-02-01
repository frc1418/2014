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

'''
    This nifty module replaces the imshow function of cv2. When we're in a
    GTK environment, we can't use cv2.imshow because it will freeze the
    environment, as its message loop will not be serviced. So we just replace
    it. :) 
    
    To use this module, just import it, and it will do the magic for you.
'''

import cairo
import gtk
import glib

import cv2
import numpy as np

import cv_widget


class ImshowWidget(cv_widget.CvWidget):
    
    def __init__(self):
        cv_widget.CvWidget.__init__(self)
    
    def set_from_np(self, img):
        
        # determine height/width/channels of incoming image
        if len(img.shape) >= 3:
            h, w, c = img.shape[:3]
        else:
            h, w = img.shape[:2]
            c = 1
        
        # if the image is a different size, reallocate it
        if self._fixed_size is None or h != self._fixed_size[1] or w != self._fixed_size[0]:
            
            self._fixed_size = (w, h)
            
            self.surface = cairo.ImageSurface(cairo.FORMAT_RGB24, w, h)
            self.buffer = np.frombuffer(self.surface, dtype=np.uint8)
            self.buffer.shape = (h, w, -1)
            self.set_size_request(w, h)
            
        # opencv stores images in BGR, convert to the cairo colorspace
        if c == 1:
            cv2.cvtColor(img, cv2.COLOR_GRAY2RGBA, self.buffer)
        else:
            cv2.cvtColor(img, cv2.COLOR_BGR2RGBA, self.buffer)
        
        self.queue_draw()
        


class ImshowWindow(gtk.Window):
    '''
        A window that holds a single image in it
        
        TODO: manage the window layout better, along with the possibility of
        docking all of the windows in the same container?
    '''

    windows = {}

    @staticmethod
    def imshow(name, img):
        windows = ImshowWindow.windows
        if name not in windows:
            window = ImshowWindow(name)
            window.show_all()
            
            windows[name] = window 
        else:
            window = windows[name]
            
        window.widget.set_from_np(img)

    def __init__(self, name):
        gtk.Window.__init__(self)
        self.set_title(name)
        self.set_resizable(False)
        
        self.window_name = name
        
        self.widget = ImshowWidget()
        self.add(self.widget)
        self.widget.show()
        
        self.connect('destroy', self.on_destroy)
        self.connect('key-press-event', self.on_key_press)
    
    def on_key_press(self, widget, event):
        if event.keyval == gtk.keysyms.Escape:
            self.destroy()
        
    def on_destroy(self, widget):
        del ImshowWindow.windows[self.window_name]
    

def imshow(name, img):
    glib.idle_add(ImshowWindow.imshow, name, img.copy())
    
# replace the function
cv2.imshow = imshow

