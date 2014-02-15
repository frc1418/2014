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

import cairo
import glib
import gtk

import cv2
import numpy as np

class CvWidget(gtk.DrawingArea):
    '''
        This is a class to show an OpenCV image in a GTK widget
        
        Initialized to a fixed size for now
        
        One way that you could do this is by just copying the OpenCV images
        to a pixbuf... but that would involve a lot of memory allocation and
        unnecessary copies. The way this works is we have a buffer stored
        that has a cairo surface associated with it, and we copy onto that
        and draw it using the expose event for the widget.
    '''
    
    
    def __init__(self, fixed_size=None):
        gtk.DrawingArea.__init__(self)
        
        self._fixed_size = fixed_size
        self.zoom = 1
        
        if fixed_size is not None:
            w, h = fixed_size
            
            self.surface = cairo.ImageSurface(cairo.FORMAT_RGB24, w, h)
            self.buffer = np.frombuffer(self.surface, dtype=np.uint8)
            self.resize_buffer = np.empty(shape=(h,w,3), dtype=np.uint8)
            
            self.buffer.shape = (h, w, -1) # numpy w/h are switched
            self.buffer.fill(0x00)
        
            self.set_size_request(w, h)
            
        self.connect('expose-event', self.on_expose)
        
        # TODO: should we turn off double buffering?
        
    def draw_contour(self, cxt, contour, fill_color, outline_color):    
        '''Utility function to draw a contour from on_expose'''
        
        for x,y in contour[:,0,:]:
            cxt.line_to(int(x), int(y))
            
        # close it off
        cxt.close_path()
        
        # fill it in
        cxt.set_source_rgba(*fill_color)
        cxt.fill_preserve()
        
        # outline it
        cxt.set_source_rgb(*outline_color)
        cxt.set_line_width(3)
        cxt.stroke()
        
    def on_expose(self, widget, event):
        '''
            This draws the contents of the surface onto the widget.
        '''
        
        if self.surface is None:
            return
        
        cr = event.window.cairo_create()
        cr.set_source_surface(self.surface)
        cr.paint()
    
    
    def set_from_np(self, img):
        '''Sets the contents of the image from a numpy array'''
        
        if img is None:
            w, h = self._fixed_size
            cv2.rectangle(self.buffer, (0,0), (w, h), (0,0,0,0))
        else:        
            # if resize needed, then do it
            h, w, c = img.shape
            if w != self._fixed_size[0] or h != self._fixed_size[1]:
                self.zoom = float(w) / self._fixed_size[0]
                cv2.resize(img, self._fixed_size, self.resize_buffer)
                src = self.resize_buffer
            else:
                self.zoom = 1
                src = img
            
            # now copy it to the buffer and convert to the right format
            if c == 1:
                cv2.cvtColor(src, cv2.COLOR_GRAY2BGRA, self.buffer)
            else:
                cv2.cvtColor(src, cv2.COLOR_BGR2BGRA, self.buffer)
        
        # .. and invalidate? Make sure to use idle_add to dispatch it on the UI 
        # thread, otherwise you will get random crashes
        glib.idle_add(self.queue_draw)
        
    