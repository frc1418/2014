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


class Dashboard(object):
    # Reference Links:
    #    Dropdown: http://www.pygtk.org/pygtk2tutorial/sec-ComboBoxAndComboboxEntry.html#comboboxbasicfig
    # glade file to load
    ui_filename = "DashboardMain.ui"
    
    # widgets to load from the glade file. Each one of these is added to 'self' after
    # you call 'initialize_from_xml'
    ui_widgets = [
        "shootPowerBar",
        "window",
        "tableArm",
        "tableShoot",
        "FireButton",
        "armStateButtonLockDown",
        "armStateButtonUnlock",
        "armStateButtonLockUp",
        "shootPowerDown",
        "shootPowerUp",
        #"batteryBar",
        "distanceBar",
        "RobotStateImage",
        "BackCameraImage",
        "autoWinchToggle",
        "timer",
        "armLabel",
        "shootLabel",
        "distanceMeter",
        "autoWinchLabel",
        "RobotAngleWidget",
        
        "autonomous_tuner",
        
        "tuning_widget",
        "distanceLabel",
    ]
    
    # these are functions that are called when an event happens.
    # -- the events can be setup in the 'signals' property in glade. A list of each signal
    #    and its associated functions can be found for each widget in the PyGTK docs.
    #    For example, the button pressed signal is documented at
    #    http://www.pygtk.org/docs/pygtk/class-gtkbutton.html#signal-gtkbutton--pressed
    ui_signals = [
        'on_RoughAdjustFirePower1_pressed',
        'on_RoughAdjustFirePower2_pressed',
        'on_RoughAdjustFirePower3_pressed',
        'on_RoughAdjustFirePower4_pressed',
        'on_RoughAdjustFirePower5_pressed',
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
        self.shootLabel.set_property("angle", 90)
        self.shootLabel.modify_font(self.font)
        
        self.netTable.PutBoolean("BallLoaded",False)
        self.FireButton = self.image_button('Fire-Good-Compress.png','Fire-Bad-Compress.png',False,self.FireButton,'clicked', self.on_fire_clicked)
        
        network_tables.attach_fn(self.netTable, "BallLoaded", self.on_ball_loaded, self.FireButton)

        #  ----- End Fire Button -----
        
        #  ----- End Rough Adjustment Buttons -----
        
        #  ----- End Rough Adjustment Buttons -----
        
        
        #  ----- Begin Fine Adjustment ----
        self.shootPowerDown = self.image_button("powerDown.png","powerDown.png",True,self.shootPowerDown,'clicked', self.on_shoot_power_down_pressed)
        self.shootPowerUp = self.image_button("powerUp.png","powerUp.png",True,self.shootPowerUp,'clicked', self.on_shoot_power_up_pressed)
        
        #  ----- End Fine Adjustment ----
        
        ##  ----- Begin Battery Bar -----
        #self.netTable.PutNumber("Battery",0)
        #
        #self.update_battery(None,0)
        #network_tables.attach_fn(self.netTable, "Battery", self.update_battery, self.batteryBar)
        ##  ----- End Battery Bar -----
        
        #  ----- Begin AutoWinch Toggle -----
        self.autoWinchLabel.modify_font(self.font)
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
        self.distanceLabel.set_property("angle", 90)
        self.distanceLabel.modify_font(self.font)
        
        self.distanceBar.modify_font(self.fontMono)
        self.distanceMeter.modify_font(self.fontDistanceBig)
        
        self.distanceBar.configure(2.5,0,2.5)
        
        self.netTable.PutNumber("Distance",0)
        
        self.update_distance(None,0)
        network_tables.attach_fn(self.netTable, "Distance", self.update_distance, self.distanceBar)
        #  ----- End Battery Bar -----
        
        #  ----- Begin Arm -----
        self.armLabel.modify_font(self.font)
        
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
        #network_tables.attach_fn(self.netTable, "BallLoaded", self.update_robot_state_image, self.RobotStateImage)
        #this is for whatever the catapult's angle is.
        network_tables.attach_fn(self.netTable, "FirePower", self.RobotStateImage.updatecatapult, self.RobotStateImage)
        
        #self.update_robot_state_image(None,None)
            
        #  ----- End Robot State Image -----
    
    
        
        #  ----- Begin Robot Angle Widget -----
        self.RobotAngleWidget = util.replace_widget(self.RobotAngleWidget,robot_angle_widget.RobotAngleWidget())
        self.netTable.PutNumber("GyroAngle",0)
        # robot angle widget sending the variable to itself
        network_tables.attach_fn(self.netTable, 'GyroAngle', self.RobotAngleWidget.update, self.window)
        #  ----- End Robot Angle Widget -----
        
        
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
        util.replace_widget(self.autonomous_tuner, autonomous_tuning_widget.AutonomousTuningWidget(self.netTable))
        
        #network_tables.attach_chooser_combo(self.netTable, 'Autonomous Mode', self.autoCombo)
        
        # show the window AND all of its child widgets. If you don't call show_all, the
        # children may not show up
        self.window.show_all()
        
        # make sure the UI kills itself when the UI window exits
        self.window.connect('destroy', self.on_destroy)
        
    def initialize_image_processing(self):
        
        network_tables.attach_connection_listener(self.netTable, self.on_connection_connect, self.on_connection_disconnect, self.window)
        
        
    def update_power_indicators(self):
        self.shootPower[self.currentShootPower]
        self.shootPower[self.currentShootPower]
        self.shootPower[self.currentShootPower]
        self.shootPower[self.currentShootPower]
        self.shootPower[self.currentShootPower]
        
    def update_shooter_power_bar(self,value):
        self.shootPowerBar.set_value(value)
        self.shootPowerBar.set_text(str(value))
        
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
        self.distanceMeter.set_text(distStr)
    
    def on_ArmStateLockedDown_pressed(self, widget):
        print("Arm Locked Down was pressed")
        self.netTable.PutNumber('ArmSet',1)
        
    def on_ArmStateUnlocked_pressed(self, widget):
        print("Arm Unlocked was pressed")
        self.netTable.PutNumber('ArmSet',2)
        
    def on_ArmStateLockedUp_pressed(self, widget):
        print("Arm Locked Up was pressed")
        self.netTable.PutNumber('ArmSet',3)
        
    def on_RoughAdjustFirePower1_pressed(self, widget):
        print("Button 1 was pressed")
        self.currentShootPower = 0;
        value = self.shootPower[self.currentShootPower]
        self.shootPowerBar.set_value(value)
        self.netTable.PutNumber('FirePower',value)
        self.update_shooter_power_bar(value)
        
    def on_RoughAdjustFirePower2_pressed(self, widget):
        print("Button 2 was pressed")
        self.currentShootPower = 1;
        value = self.shootPower[self.currentShootPower]
        self.shootPowerBar.set_value(value)
        self.netTable.PutNumber('FirePower',value)
        self.update_shooter_power_bar(value)
        
    def on_RoughAdjustFirePower3_pressed(self, widget):
        print("Button 3 was pressed")
        self.currentShootPower = 2;
        value = self.shootPower[self.currentShootPower]
        self.shootPowerBar.set_value(value)
        self.netTable.PutNumber('FirePower',value)
        self.update_shooter_power_bar(value)
        
    def on_RoughAdjustFirePower4_pressed(self, widget):
        print("Button 4 was pressed")
        self.currentShootPower = 3;
        value = self.shootPower[self.currentShootPower]
        self.shootPowerBar.set_value(value)
        self.netTable.PutNumber('FirePower',value)
        self.update_shooter_power_bar(value)

    def on_RoughAdjustFirePower5_pressed(self, widget):
        print("Button 5 was pressed")
        self.currentShootPower = 4;
        value = self.shootPower[self.currentShootPower]
        self.shootPowerBar.set_value(value)
        self.netTable.PutNumber('FirePower',value)
        self.update_shooter_power_bar(value)
        
    def on_fire_clicked(self, widget):
        print("Fire!")
        self.netTable.PutBoolean('Fire',True)
        
    def on_shoot_power_down_pressed(self, widget):
        print("Reduce shoot power")
        power = self.shootPower[self.currentShootPower]
        min = self.currentShootPower*20
        max = (self.currentShootPower+1)*20
        print(str(power)+":"+str(min)+":"+str(max))
        if(min<power):
            power = power - 2
            self.shootPower[self.currentShootPower]=power
            self.update_shooter_power_bar(power)
            self.update_power_indicators()
        
    def on_shoot_power_up_pressed(self, widget):
        print("Increase shoot power")
        power = self.shootPower[self.currentShootPower]
        min = self.currentShootPower*20
        max = (self.currentShootPower+1)*20
        print(str(power)+":"+str(min)+":"+str(max))
        if(power<max):
            power = power + 2
            self.shootPower[self.currentShootPower]=power
            self.update_shooter_power_bar(power)
            self.update_power_indicators()
            
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
            self.timer.set_text('robot is disabled')
        else:
            temptime =(int(currenttime-self.starttime))
            min = int(math.floor(temptime/60))
            sec = temptime%60
            timeStr = "Timer: "+str(min) + ':'
            if sec<10:
                timeStr += "0"
            timeStr +=  str(sec)
            self.timer.set_text(timeStr)
        
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
            
            for processor in self.imageProcessors:
                processor.enable_image_logging()
            
            current_mode = None
            active = self.autoCombo.get_active_iter()
            if active:
                current_mode = self.autoCombo.get_model()[active][0]
            
            logger.info("Robot switched into autonomous mode")
            logger.info("-> Current mode is: %s", current_mode)
        

        elif value == self.MODE_TELEOPERATED:
            
            
            for processor in self.imageProcessors:
                processor.enable_image_logging()
            
            logger.info("Robot switched into teleoperated mode")
           
        else:
            # don't waste disk space while the robot isn't enabled
            for processor in self.imageProcessors:
                processor.disable_image_logging()
            
            logger.info("Robot switched into disabled mode")
            
            self.starttime = None
            
        print 'value', value
        
    def on_destroy(self, window):
        gtk.main_quit()
