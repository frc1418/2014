import gtk
import pygtk
import util
import glib
import time
import math


from widgets import (
    autonomous_tuning_widget,
    camera_widget,
    target_widget,
    image_button,
    network_tables,
    detector_tuning_widget,
    robot_angle_widget,
    toggle_button,
    robot_widget,
)

import logging
logger = logging.getLogger(__name__)


class SingleCameraUI(object):
    # Reference Links:
    #    Dropdown: http://www.pygtk.org/pygtk2tutorial/sec-ComboBoxAndComboboxEntry.html#comboboxbasicfig
    # glade file to load
    ui_filename = "SingleCameraUI.ui"
    
    # widgets to load from the glade file. Each one of these is added to 'self' after
    # you call 'initialize_from_xml'
    ui_widgets = [
        "window",
       
        "BackCameraImage",
        "tuning_widget"
    ]
    
    # these are functions that are called when an event happens.
    # -- the events can be setup in the 'signals' property in glade. A list of each signal
    #    and its associated functions can be found for each widget in the PyGTK docs.
    #    For example, the button pressed signal is documented at
    #    http://www.pygtk.org/docs/pygtk/class-gtkbutton.html#signal-gtkbutton--pressed
    ui_signals = [
    ]
    
    # keep in sync with robot
    MODE_DISABLED       = 0
    MODE_AUTONOMOUS     = 1
    MODE_TELEOPERATED   = 2
    
    
    def __init__(self, NetworkTable, frontProcessor, backProcessor):
        
        self.netTable = NetworkTable
        util.initialize_from_xml(self)
        
        #  ----- Begin Cameras -----
        self.BackCameraImage = util.replace_widget(self.BackCameraImage, target_widget.TargetWidget((320,240), self.netTable))
        #  ----- End Cameras -----
        
        backProcessor.set_camera_widget(self.BackCameraImage)
            
        self.imageProcessors = [backProcessor]
        
        self.tuning_widget = util.replace_widget(self.tuning_widget, detector_tuning_widget.DetectorTuningWidget(backProcessor))
        self.tuning_widget.initialize()
        
        # get notified when the robot switches modes
        network_tables.attach_fn(self.netTable, 'RobotMode', self.on_robot_mode_update, self.window)
        
        # show the window AND all of its child widgets. If you don't call show_all, the
        # children may not show up
        self.window.show_all()
        
        # make sure the UI kills itself when the UI window exits
        self.window.connect('destroy', self.on_destroy)
                
    def initialize_image_processing(self):
        network_tables.attach_connection_listener(self.netTable, self.on_connection_connect, self.on_connection_disconnect, self.window)
            
    def on_connection_connect(self, remote):
        # minutes = math.floor(seconds/60) secodnds = seconds%60
        # this doesn't seem to actually tell the difference
        if remote.IsServer():
            logger.info("NetworkTables connection to robot detected")
        else:
            logger.info("NetworkTables connection to client detected")
         
        for processor in self.imageProcessors:
            processor.start()
        
        self.BackCameraImage.start()
        
        
    def on_connection_disconnect(self, remote):
        if remote.IsServer():
            logger.info("NetworkTables disconnected from robot")
        else:
            logger.info("NetworkTables disconnected from client")
            
    def on_robot_mode_update(self, key, value):
        '''This is called when the robot switches modes'''
        
        if value == self.MODE_AUTONOMOUS:
            for processor in self.imageProcessors:
                processor.enable_image_logging()

        elif value == self.MODE_TELEOPERATED:
            
            for processor in self.imageProcessors:
                processor.enable_image_logging()
            
            logger.info("Robot switched into teleoperated mode")
           
        else:
            # don't waste disk space while the robot isn't enabled
            for processor in self.imageProcessors:
                processor.disable_image_logging()

            logger.info("Robot switched into disabled mode")
            
    def on_destroy(self, window):
        gtk.main_quit()
