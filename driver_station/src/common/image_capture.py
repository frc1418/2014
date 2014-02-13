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


import os.path
import time
import threading

import cv2
import gtk
import numpy as np

from ui import util

from image_logger import ImageLogger

import logging
import logutil, settings
logger = logging.getLogger(__name__)


class _FakeDetector(object):
    def processImage(self, img):
        return (img, None)

class ImageCapture(object):
    '''
        This class manages the image processing stuff. It determines what
        actions to take, and then performs them on another thread.
        
        The actual image processing takes place in a different class. That 
        class processes the image, and then returns a dictionary that has
        targeting information in it.
    '''
    
    def __init__(self, detector=None, name=''):    
        
        if detector is None:
            self.detector = _FakeDetector()
        else:
            self.detector = detector
        
        self.prefix = name if name == '' else '%s_' % name
        self.lock = threading.Lock()
        self.condition = threading.Condition(self.lock)
        self.image_log_enabled = False
        self.using_live_feed = False
    
    def initialize(self, options, camera_widget):
        
        def _get_option(name):
            return getattr(options, '%s%s' % (self.prefix, name))
        
        self.do_stop = False
        self.do_refresh = False
        
        #self.use_webcam = _get_option('webcam')
        self.use_webcam = None
        self.camera_ip = _get_option('camera_ip')
        self.camera_widget = camera_widget
        
        self.img_logger = None
        
        
        #if options.ask:
        #    options.static_images = util.get_directory(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'logs')))
        #    if options.static_images is None:
        #        raise RuntimeError()
        
        #if options.log_images:
        #    self.img_logger = ImageLogger(options.log_dir)
        
        # detect live or static processing
        #if options.static_images is not None:
        #    self._initialize_static(options)
        #    thread_fn = self._static_processing
        #else:
        
        self.using_live_feed = True
        thread_fn = self._live_processing
            
        self.thread = threading.Thread(target=thread_fn)
        self.thread.setDaemon(True)
        
    def is_live_feed(self):
        return self.using_live_feed
        
    def start(self):
        if self.img_logger is not None:
            self.img_logger.start()
        
        if not self.thread.is_alive():
            self.thread.start()
        
    def stop(self):
        self.do_stop = True
        with self.condition:
            self.condition.notify()
            
        if self.thread.is_alive():
            self.thread.join()
        
        if self.img_logger is not None:
            self.img_logger.stop()
            
    def enable_image_logging(self):
        with self.lock:
            self.image_log_enabled = True
            
    def disable_image_logging(self):
        with self.lock:
            self.image_log_enabled = False
        
    def refresh(self):
        with self.condition:
            self.do_refresh = True
            self.condition.notify()
        
    def _initialize_static(self, options):
        
        path = options.static_images
        self.idx = 0
        self.idx_increment = 1
        
        if not os.path.exists(path):
            logger.error("'%s' does not exist!" % path)
            raise RuntimeError()
        
        if not os.path.isdir(path):
            self.images = [path]
        else:
            self.images = []
            for path, dirs, files in os.walk(path):
                self.images += [os.path.join(path, f) for f in files] 
            
            self.images.sort()
        
        # setup the key handler
        def _on_key_press(widget, event):
            if event.keyval == gtk.keysyms.Left:
                if self.idx > 0:
                    with self.condition:
                        self.idx -= 1
                        self.idx_increment = -1
                        self.condition.notify()
            elif event.keyval == gtk.keysyms.Right:
                if self.idx < len(self.images):
                    with self.condition:
                        self.idx += 1
                        self.idx_increment = 1
                        self.condition.notify()
            elif event.keyval == gtk.keysyms.Escape:
                gtk.main_quit()
            
            # return True otherwise we might lose focus
            return True
        
        def _on_button_pressed(widget, event):
            widget.grab_focus()
        
        # must be able to get focus to receive keyboard events
        self.camera_widget.set_can_focus(True)
        self.camera_widget.add_events(gtk.gdk.BUTTON_PRESS_MASK)
        
        self.camera_widget.grab_focus()
        self.camera_widget.connect('key-press-event', _on_key_press)
        self.camera_widget.connect('button-press-event', _on_button_pressed)
        

    @logutil.exception_decorator(logger)
    def _static_processing(self):
        
        logger.info("Static processing thread starting")
        idx = -1
        
        # resume processing with the last image the user looked at
        last_img = settings.get('processing/last_img', None)
        for i, image_name in enumerate(self.images):
            if image_name == last_img:
                self.idx = i
                break 
        
        while True:
        
            with self.condition:
                
                # wait until the user hits a key
                while idx == self.idx and not self.do_stop and not self.do_refresh:
                    self.condition.wait()
                
                if self.do_stop:
                    break
                
                idx = self.idx
                self.do_refresh = False
                    
            # if the index is valid, then process an image
            if idx < len(self.images) and idx >= 0:
                
                image_name = self.images[idx]
                
                logger.info("Opening %s" % image_name)
                
                img = cv2.imread(image_name)
                if img is None:
                    logger.error("Error opening %s: could not read file" % (image_name))
                    self.idx += self.idx_increment
                    continue
                
                try:
                    target_data = self.detector.processImage(img)
                except:
                    logutil.log_exception(logger, 'error processing image')
                else:
                    settings.set('processing/last_img', image_name)
                    settings.save()
                    
                    logger.info('Finished processing')
                
                    # note that you cannot typically interact with the UI
                    # from another thread -- but this function is special
                    self.camera_widget.set_target_data(target_data)
            
        logger.info("Static processing thread exiting")

        
    def _initialize_live(self):
        vc = cv2.VideoCapture()
        
        vc.set(cv2.cv.CV_CAP_PROP_FPS, 1)
        
        if self.use_webcam is None:
            logger.info('Connecting to %s' % self.camera_ip)
            if not vc.open('http://%s/mjpg/video.mjpg' % self.camera_ip):
                logger.error("Could not connect")
                return
        else:
            logger.info('Connecting to webcam %s' % self.use_webcam)
            if not vc.open(self.use_webcam):
                logger.error("Could not connect")
                return
        
        logger.info('Connected!')
        return vc
            

    @logutil.exception_decorator(logger)
    def _live_processing(self):
        
        logger.info("Live processing thread starting")
        
        while True:
            
            # check for exit condition
            with self.lock:
                if self.do_stop:
                    break
            
            # open the video capture device
            vc = self._initialize_live()
            
            if vc is None:
                continue
        
            last_log = 0
            exception_occurred = False
            
            # allocate a buffer for reading
            h = vc.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)
            w = vc.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)
            
            capture_buffer = np.empty(shape=(h, w, 3), dtype=np.uint8)
            
            while True:
            
                # check for exit condition
                with self.lock:
                    if self.do_stop:
                        break
                    
                    image_log_enabled = self.image_log_enabled
                
                #
                # Read the video frame
                #
                
                retval, img = vc.read(capture_buffer)
                
                if retval:
                    
                    # log images to directory
                    if self.img_logger is not None:
                        tm = time.time()
                        diff = tm - last_log
                        if diff >= 1:
                            if image_log_enabled:
                                self.img_logger.log_image(img)
                            
                            # adjust for possible drift
                            if diff > 1.5:
                                last_log = tm
                            else:
                                last_log += 1
                
                    #
                    # Process the image
                    #
                    
                    try:
                        target_data = self.detector.processImage(img)
                    except:
                        # if it happened once, it'll probably happen again. Don't flood
                        # the logfiles... 
                        if not exception_occurred:
                            logutil.log_exception(logger, 'error processing image')
                            exception_occurred = True
                        self.camera_widget.set_error(img)
                        
                    else:
                        if exception_occurred:
                            logger.info("Processing resumed, no more errors.")
                            exception_occurred = False
                        
                        # note that you cannot typically interact with the UI
                        # from another thread -- but this function is special
                        self.camera_widget.set_target_data(target_data)
                                        
                else:
                    if last_log == 0: 
                        logger.error("Not able to connect to camera, retrying")
                    else:
                        logger.error("Camera disconnected, retrying")
                        
                    self.camera_widget.set_error()
                    break
            
        logger.info("Static processing thread exiting")


