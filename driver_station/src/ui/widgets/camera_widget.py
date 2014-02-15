
import cv_widget

import glib
import gtk

import threading



class CameraWidget(cv_widget.CvWidget):
    '''
        Generic widget used to display a camera image. Works with the ImageCapture
        class, and can display errors and camera timeouts and other things.
    '''
    
    
    def __init__(self, fixed_size):
        cv_widget.CvWidget.__init__(self, fixed_size)
        
        self.lock = threading.Lock()
        self.show_error = None    
    
    def start(self):
        # don't set this right away, wait for 3 seconds -- otherwise the user 
        # might think there's an error when there really isn't one
        # -> if True/False, set camera/error appropriately. show blank if None
        if self.show_error is None:
            glib.timeout_add_seconds(3, self._no_camera_timer)
        
    def _no_camera_timer(self):
        '''Called after N seconds starting up, to see if we found a camera yet'''
        with self.lock:
            if self.show_error is None:
                self.show_error = True
                self.queue_draw()
    
    def set_error(self, img=None):
        '''Causes an error icon to be shown'''
        with self.lock:
            self.show_error = True
            
        self.set_from_np(img)
    
    def set_target_data(self, data):
        '''Override this to do something with the data'''
        img, data = data
        
        self.set_from_np(img)
    
        with self.lock:
            self.show_error = False
    
    def on_expose(self, widget, event):
        cv_widget.CvWidget.on_expose(self, widget, event)
        
        with self.lock:
            show_error = self.show_error
        
        ww, wh = event.window.get_size()
        
        # if there is an error, draw a warning icon 
        if show_error == True:
            pixbuf = self.render_icon(gtk.STOCK_DIALOG_WARNING, gtk.ICON_SIZE_DIALOG)
            
            # center it
            pw = pixbuf.get_width()
            ph = pixbuf.get_height()
            
            
            x = int(ww/2.0 - pw/2.0)
            y = int(wh/2.0 - ph/2.0)
            
            event.window.draw_pixbuf(None, pixbuf, 0, 0, x, y)
        
    