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

import datetime
import os.path
import threading

import cv2

import logging
from common import logutil
logger = logging.getLogger(__name__)


class ImageLogger(object):

    def __init__(self, prefix, logdir):
        self.prefix = prefix
        self.logdir = logdir
        self.has_image = False
        self.do_stop = False
        
        self.condition = threading.Condition()
        self.thread = threading.Thread(target=self._log_thread)
        
    def log_image(self, image):
        h, w = image.shape[:2]
        datestr = datetime.datetime.now().strftime('%Y-%m-%d %H%M-%S-%f')
        filename = '%s%s@%sx%s.png' % (self.prefix, datestr, w, h)
        filename = os.path.join(self.logdir, filename)
        
        with self.condition:
            self.has_image = True
            
            # TODO: does making a copy here matter?
            self.img = image.copy()
            self.img_filename = filename
            
            self.condition.notify()
            
    def start(self):
        if not self.thread.is_alive():
            logger.info("Starting %s image logger to %s" % (self.prefix, self.logdir))
            self.thread.start()
        
    def stop(self):
        with self.condition:
            self.do_stop = True
            self.condition.notify()
            
        if self.thread.is_alive():
            self.thread.join()
        
    @logutil.exception_decorator(logger)
    def _log_thread(self):
        
        while True:
            with self.condition:
                
                if self.do_stop:
                    break
                
                while not self.has_image and not self.do_stop:
                    self.condition.wait()
                    
                # if there's an image queued up, then we want to
                # write it out before exiting
                if not self.has_image:
                    continue
                
                img = self.img
                img_filename = self.img_filename
                self.has_image = False
                
            logger.debug('Writing image to %s' % img_filename)
            cv2.imwrite(img_filename, img)
