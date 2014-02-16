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


import traceback
from functools import wraps

import logging
import logging.handlers
import os
import Queue

from loghandler_33 import QueueHandler, QueueListener

# TODO: Make these configurable
log_datefmt = "%H:%M:%S"
log_format = "%(asctime)s:%(msecs)03d %(levelname)-8s: %(name)-20s: %(message)s"
log_level = logging.DEBUG


def configure_logging(log_dir):
    '''
        Configures the logger for the program. All logging will go over to
        a separate thread, which will then write the log to disk. This way 
        we can avoid blocking any of our processing threads.
    
        Do not import anything that requires the logger until we have setup 
        the logger.
        
        This returns a queue listener object. You should call stop() on it
        before exiting the program, or queued messages may be lost. 
    '''
        
    # get the root logger
    root = logging.getLogger("")
        
    # console logging
    logging.basicConfig(format=log_format, level=log_level, datefmt=log_datefmt)
           
    # log to a file
    log_file = os.path.join(log_dir, 'log')
    
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
        
    log_exists = os.path.exists(log_file)
    
    file_logger = logging.handlers.RotatingFileHandler(log_file, mode='a', backupCount=10)
    
    if log_exists:
        file_logger.doRollover()
        
    file_logger.setFormatter(logging.Formatter(log_format, log_datefmt))
    
    # initialize the queues
    # -> the QueueListener starts a new thread
    q = Queue.Queue(-1)    
    ql = QueueListener(q, file_logger)
    
    qh = QueueHandler(q)
    root.addHandler(qh)
    
    ql.start()
    
    return ql


def log_exception(logger, msg):
    '''Convenience function to log an exception with'''
    logger.error('Exception: %s\n%s', msg, traceback.format_exc())
    
class exception_decorator(object):
    '''
        This decorator catches any exceptions that may occur in a function, 
        and logs them so we know about it later.  
        
        Mostly intended for use in threads.
        
        Example usage:
        
            @exception_decorator(logger)
            def some_function(arg):
                .. 
                # some exception gets thrown in here, it will be caught
    '''
    
    def __init__(self, logger=None):
        self.logger = logger
        
    def __call__(self, f, *args, **kwargs):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if self.logger is None:
                if hasattr(args[0], 'logger'):
                    self.logger = getattr(args[0], 'logger')
                if self.logger is None:
                    raise RuntimeError("No configured logger!")
            try:
                f(*args, **kwargs)
            except:
                log_exception(self.logger, 'Uncaught exception in %s' % f.__name__)
        return wrapper 

