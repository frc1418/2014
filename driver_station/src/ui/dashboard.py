#
#    This file is part of Team 1418 Dashboard
#
#    Team 1418 Dashboard is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, version 3.
#
#    Team 1418 Dashboard is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Team 1418 Dashboard.  If not, see <http://www.gnu.org/licenses/>.
#



import gtk
import pygtk
import util
import glib
import time
import math
import graphwindow


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


class Dashboard(object):
    # Reference Links:
    #    Dropdown: http://www.pygtk.org/pygtk2tutorial/sec-ComboBoxAndComboboxEntry.html#comboboxbasicfig
    # glade file to load
    ui_filename = "DashboardMain.ui"
    
    # widgets to load from the glade file. Each one of these is added to 'self' after
    # you call 'initialize_from_xml'
    ui_widgets = [
        "window",
        "FireButton",
        "armStateButtonLockDown",
        "armStateButtonUnlock",
        "armStateButtonLockUp",
        "distanceBar",
        "RobotStateImage",
        "BackCameraImage",
        "autoWinchToggle",
        "timer",
        "RobotAngleWidget",
        "autonomous_tuner",
        "tuning_widget",
        "notebook1",
        "compressoronoff",
        "PowerBarSlider",
    ]
    
    # these are functions that are called when an event happens.
    # -- the events can be setup in the 'signals' property in glade. A list of each signal
    #    and its associated functions can be found for each widget in the PyGTK docs.
    #    For example, the button pressed signal is documented at
    #    http://www.pygtk.org/docs/pygtk/class-gtkbutton.html#signal-gtkbutton--pressed
    ui_signals = [
    'on_PowerBarSlider_change_value',
    'on_open_graph_clicked',
                  ]
    
    # keep in sync with robot
    MODE_DISABLED       = 0
    MODE_AUTONOMOUS     = 1
    MODE_TELEOPERATED   = 2
    
    
    def __init__(self, NetworkTable, frontProcessor, backProcessor, competition):
        
        self.netTable = NetworkTable
        util.initialize_from_xml(self)
        
        
        
        self.shootPower = [10, 30, 50, 70, 90]
        self.currentShootPower = 4
        
        #starts the timer
        self.starttime = None
        
        #self.window.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse('#aaaaaa'))        
        
        import pango
        
        self.font = pango.FontDescription("bold 18")
        
        self.fontMono = pango.FontDescription("Monospace 14")
        
        self.fontDistanceBig = pango.FontDescription("bold 100")
        
        
        #from wpilib import DriverStation
        
        #DriverStation.GetInstance()
        
        '''# demo: load the images into pixbufs so that Gtk can use them
        active = util.pixbuf_from_file('toggle-on.png')
        inactive = util.pixbuf_from_file('toggle-off.png')
        
        # demo: create a ToggleButton widget. There are lots of widgets you can create
        real_widget = toggle_button.ToggleButton(active, inactive, clickable=True)
        
        # demo: replace a fake widget in the glade file with a 'real' widget
        util.replace_widget(self.toggleButton, real_widget)
        
        # demo: connect to the toggled event of the real widget, so that our
        #       function gets called when the button state is changed
        real_widget.connect('toggled', self.on_toggleButton_toggled)
        '''
        #  ----- Begin Position Set -----  
        self.netTable.PutNumber('position', 0)
        #  ----- End Position Set-----  
        
        #  ----- Begin Fire Button -----
        self.netTable.PutBoolean("BallLoaded",False)
        self.FireButton = self.image_button('fire_good.png','fire_bad.png',False,self.FireButton,'clicked', self.on_fire_clicked)
        
        network_tables.attach_fn(self.netTable, "BallLoaded", self.on_ball_loaded, self.FireButton)
        #  ----- End Fire Button -----
        
        #------ Begin Compressor Label -----
        network_tables.attach_fn(self.netTable, "Compressor", self.update_compressor_image, self.compressoronoff)
        self.on = util.pixbuf_from_file('compressoron.jpg')
        self.off = util.pixbuf_from_file('compressoroff.jpg')        
        #------ End Compressor Label -----
        
        #----- Begin AutoWinch Toggle -----
        active = util.pixbuf_from_file('booleanT.png')
        inactive = util.pixbuf_from_file('booleanF.png')
        
        real_widget = toggle_button.ToggleButton(active, inactive, clickable=True)
        
        util.replace_widget(self.autoWinchToggle, real_widget)
        
        real_widget.connect('toggled', self.on_autoWinch_toggled)
        
        #  ----- End AutoWinch Toggle -----
        
        #  ----- Begin Cameras -----
        self.BackCameraImage = util.replace_widget(self.BackCameraImage, target_widget.TargetWidget((320,240), self.netTable))
        #  ----- End Cameras -----
        
        #  ----- Begin Distance Bar -----
        
        self.distanceBar.modify_font(self.fontMono)
        
        self.distanceBar.configure(2.5,0,2.5)
        
        self.netTable.PutNumber("Distance",0)
        
        self.update_distance(None,0)
        network_tables.attach_fn(self.netTable, "Distance", self.update_distance, self.distanceBar)
        #  ----- End Distance Bar -----
        
        #  ----- Begin Arm -----
        
        self.netTable.PutNumber("ArmSet",0)
        self.netTable.PutNumber("ArmState",0)
        
        self.armStateButtonLockDown = self.image_button('armDownSel.png','armDown.png',False,self.armStateButtonLockDown,'clicked',self.on_ArmStateLockedDown_pressed)
        self.armStateButtonUnlock = self.image_button('armUnlockedSel.png','armUnlocked.png',False,self.armStateButtonUnlock,'clicked',self.on_ArmStateUnlocked_pressed)
        self.armStateButtonLockUp = self.image_button('armUpSel.png','armUp.png',False,self.armStateButtonLockUp,'clicked',self.on_ArmStateLockedUp_pressed)
        
        network_tables.attach_fn(self.netTable, "ArmState", self.update_arm_indicator, self.armStateButtonLockDown)
        
        #  ----- End Arm -----
        
        #  ----- Begin Timer ----- 
        self.timer.modify_font(self.font)
        self.on_timer()
        #  ----- Begin Timer -----
        
            
        #  ----- Begin Robot State Image -----
        self.netTable.PutBoolean("BallLoaded",False)
        self.RobotStateImage = util.replace_widget(self.RobotStateImage,robot_widget.RobotStateImage())
        network_tables.attach_fn(self.netTable, "ArmState", self.RobotStateImage.updatearm, self.RobotStateImage)
        network_tables.attach_fn(self.netTable, "BallLoaded", self.RobotStateImage.updateball, self.RobotStateImage)
        #this is for whatever the catapult's angle is.
        network_tables.attach_fn(self.netTable, "ShootAngle", self.RobotStateImage.updatecatapult, self.RobotStateImage)
        #self.update_robot_state_image(None,None)    
        #  ----- End Robot State Image -----
        
        #  ----- Begin Robot Angle Widget -----
        self.RobotAngleWidget = util.replace_widget(self.RobotAngleWidget,robot_angle_widget.RobotAngleWidget())
        self.netTable.PutNumber("GyroAngle",0)
        # robot angle widget sending the variable to itself
        network_tables.attach_fn(self.netTable, 'GyroAngle', self.RobotAngleWidget.update, self.window)
        network_tables.attach_fn(self.netTable, 'GyroEnabled', self.on_gyro_enabled, self.window)
        
        self.RobotAngleWidget.connect('angle-enabled-changed', lambda w: self.netTable.PutBoolean('GyroEnabled', w.angle_enabled))
        
        #  ----- End Robot Angle Widget -----
        
        # ------ Begin Power Bar Slider -----
        powerslider=self.PowerBarSlider.get_value()
        
        # ------ End Power Bar Slider -------
        
        # ------ Begin Graph Window -----
        self.GraphOpener=graphwindow.GraphOpener(self.netTable)
        #self.GraphPlot=graphwindow.GraphPlot(self.netTable)
        
        # ------ End Graph Window -------
        
        '''
        code starts here code starts here code starts here code starts here code starts here code starts here code starts here 
        code starts here code starts here code starts here code starts here code starts here code starts here code starts here 
        code starts here code starts here code starts here code starts here code starts here code starts here code starts here 
        code starts here code starts here code starts here code starts here code starts here code starts here code starts here 
        code starts here code starts here code starts here code starts here code starts here code starts here code starts here 
        code starts here code starts here code starts here code starts here code starts here code starts here code starts here 
        this is to help Matt navigate the code, and he apologizes.
        '''

        if competition:
            self.window.move(0,0)
            self.window.resize(1356, 525)
        
        
        backProcessor.set_camera_widget(self.BackCameraImage)
            
        self.imageProcessors = [backProcessor]
        
        self.tuning_widget = util.replace_widget(self.tuning_widget, detector_tuning_widget.DetectorTuningWidget(backProcessor))
        self.tuning_widget.initialize()
        
        # get notified when the robot switches modes
        network_tables.attach_fn(self.netTable, 'RobotMode', self.on_robot_mode_update, self.window)
        
        
        # setup the autonomous chooser
        self.autonomous_tuner = util.replace_widget(self.autonomous_tuner, autonomous_tuning_widget.AutonomousTuningWidget(self.netTable))
        
        # show the window AND all of its child widgets. If you don't call show_all, the
        # children may not show up
        self.window.show_all()
        self.setup_background()
        
        # make sure the UI kills itself when the UI window exits
        self.window.connect('destroy', self.on_destroy)
        
    def setup_background(self):
        
        bg = util.pixbuf_from_file('background.png')
        pixmap, mask = bg.render_pixmap_and_mask()
        
        # called after the window is shown
        style = self.window.get_style().copy()
        style.bg_pixmap[0] = pixmap
        
        self.window.set_style(style)
        
        #self.window.connect('expose-event', self.on_window_expose)
        
    def on_window_expose(self, widget, event):
        cxt = event.window.cairo_create()
        cxt.set_source_surface(self.imageBG)
        cxt.paint()
        
    def initialize_image_processing(self):
        network_tables.attach_connection_listener(self.netTable, self.on_connection_connect, self.on_connection_disconnect, self.window)
            
    def update_compressor_image(self, key, value):
        if value==0:
            self.compressoronoff.set_from_pixbuf(self.off)
        if value==1:
            self.compressoronoff.set_from_pixbuf(self.on)
    
    def update_arm_indicator(self, key, value):
        value = int(value)
        print("update arm "+str(value))
        if value==1:
            print("1")
            self.armStateButtonLockDown.set_from_pixbuf(self.armStateButtonLockDown.active)
            self.armStateButtonUnlock.set_from_pixbuf(self.armStateButtonUnlock.inactive)
            self.armStateButtonLockUp.set_from_pixbuf(self.armStateButtonLockUp.inactive)
        elif value==2:
            print("2")
            self.armStateButtonLockDown.set_from_pixbuf(self.armStateButtonLockDown.inactive)
            self.armStateButtonUnlock.set_from_pixbuf(self.armStateButtonUnlock.active)
            self.armStateButtonLockUp.set_from_pixbuf(self.armStateButtonLockUp.inactive)
        elif value==3:
            print("3")
            self.armStateButtonLockDown.set_from_pixbuf(self.armStateButtonLockDown.inactive)
            self.armStateButtonUnlock.set_from_pixbuf(self.armStateButtonUnlock.inactive)
            self.armStateButtonLockUp.set_from_pixbuf(self.armStateButtonLockUp.active)
        
    #def update_battery(self, key, value):
    #    self.batteryBar.set_value(value)
        
    def update_distance(self, key, value):
        self.distanceBar.set_value(value)
        distStr = "{:.2f}".format(value)
        self.distanceBar.set_text(distStr)
    
    def on_ArmStateLockedDown_pressed(self, widget):
        print("Arm Locked Down was pressed")
        self.netTable.PutNumber('ArmSet',1)
        
    def on_ArmStateUnlocked_pressed(self, widget):
        print("Arm Unlocked was pressed")
        self.netTable.PutNumber('ArmSet',2)
        
    def on_ArmStateLockedUp_pressed(self, widget):
        print("Arm Locked Up was pressed")
        self.netTable.PutNumber('ArmSet',3)
        
    def on_fire_clicked(self, widget):
        print("Fire!")
        self.netTable.PutBoolean('Fire',True)
                
    def on_ball_loaded(self, key, value):
        if value:
            self.FireButton.set_from_pixbuf(self.FireButton.active)
        else:
            self.FireButton.set_from_pixbuf(self.FireButton.inactive)
        
    def on_toggleButton_toggled(self, widget):
        '''This signal was configured at runtime, and not specified in glade'''
        print("Button was toggled")
    
    def on_shootAdjustInput_value_changed(self, widget):
        '''this is probably correct'''
        print(self.shootAdjustInput.getvalue())
    
    def image_button(self, active, inactive, state, replaceMe, actionType, connectionFunction):
        
        tempButton = self.make_image_button(active, inactive, state)
        
        tempButton.connect(actionType,connectionFunction)
        
        return util.replace_widget(replaceMe,tempButton)
    
    def make_image_button(self, active, inactive, state):
        active = util.pixbuf_from_file(active)
        inactive = util.pixbuf_from_file(inactive)
        
        if state:
            tempButton = image_button.ImageButton(active)
        else:
            tempButton = image_button.ImageButton(inactive)
        
        # save these for later
        tempButton.active = active
        tempButton.inactive = inactive
        
        return tempButton
        
    def on_autoWinch_toggled(self, widget):
        print("Toggle auto winch")
        self.netTable.PutBoolean("AutoWinch",widget.get_active())
        
    def on_timer(self):
        
        currenttime=time.time()
        if self.starttime is None:
            self.timer.set_markup('<span foreground="white">ROBOT DISABLED</span>')
        else:
            temptime =(int(currenttime-self.starttime))
            min = int(math.floor(temptime/60))
            sec = temptime%60
            timeStr = "Timer: "+str(min) + ':'
            if sec<10:
                timeStr += "0"
            timeStr +=  str(sec)
            self.timer.set_markup('<span foreground="white">%s</span>' % timeStr)
        
        glib.timeout_add_seconds(1, self.on_timer)
        
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
        self.starttime=time.time()
        value = int(value)
        
        if value == self.MODE_AUTONOMOUS:
            self.notebook1.set_current_page(0)
            for processor in self.imageProcessors:
                processor.enable_image_logging()
            
            
            
            logger.info("Robot switched into autonomous mode")
            logger.info("-> Current mode is: %s", self.autonomous_tuner.get_current_mode())
        

        elif value == self.MODE_TELEOPERATED:
            self.notebook1.set_current_page(0)
            
            for processor in self.imageProcessors:
                processor.enable_image_logging()
            
            logger.info("Robot switched into teleoperated mode")
           
        else:
            # don't waste disk space while the robot isn't enabled
            for processor in self.imageProcessors:
                processor.disable_image_logging()

            self.notebook1.set_current_page(1)
            
            logger.info("Robot switched into disabled mode")
            
            self.starttime = None
            
        print 'value', value
        
    def on_gyro_enabled(self, key, value):
        print("received change", value)
        if value != self.RobotAngleWidget.angle_enabled:
            self.netTable.PutBoolean(key, self.RobotAngleWidget.angle_enabled)
        
    def on_destroy(self, window):
        gtk.main_quit()

    def on_PowerBarSlider_change_value(self, a,b,value):
        self.netTable.PutNumber('FirePower',value)
    
    def on_open_graph_clicked(self, widget):
        self.GraphOpener.show()