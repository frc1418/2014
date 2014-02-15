import gtk
import pygtk
import util
import glib

from widgets import toggle_button, image_button, network_tables, camera_widget

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
        "CameraImage",
        "BackCameraImage",
        "autoWinchToggle",
        "timer",
        "armLabel",
        "shootLabel",
        "distanceLabel"
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
    
    def __init__(self, NetworkTable, imageProcessors, competition):
        self.netTable = NetworkTable
        util.initialize_from_xml(self)
        
        self.imageProcessors = imageProcessors
        
        self.shootPower = [10, 30, 50, 70, 90]
        self.currentShootPower = 4
        
        #self.window.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse('#aaaaaa'))        
        
        import pango
        
        self.font = pango.FontDescription("bold 18")
        
        self.armLabel.modify_font(self.font)
        self.shootLabel.set_property("angle", 90)
        self.shootLabel.modify_font(self.font)
        self.distanceLabel.set_property("angle", 90)
        self.distanceLabel.modify_font(self.font)
        
        #self.window.set_font_description(self.font)
        
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
        #  ----- Begin Fire Button -----
        self.netTable.PutBoolean("BallLoaded",False)
        self.FireButton = self.image_button('Fire-Good-Compress.png','Fire-Bad-Compress.png',False,self.FireButton,'clicked', self.on_fire_clicked)
        
        network_tables.attach_fn(self.netTable, "BallLoaded", self.on_ball_loaded, self.FireButton)

        #  ----- End Fire Button -----
        
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
        active = util.pixbuf_from_file('booleanT.png')
        inactive = util.pixbuf_from_file('booleanF.png')
        
        real_widget = toggle_button.ToggleButton(active, inactive, clickable=True)
        
        util.replace_widget(self.autoWinchToggle, real_widget)
        
        real_widget.connect('toggled', self.on_autoWinch_toggled)
        
        #  ----- End AutoWinch Toggle -----
        
        #  ----- Begin Cameras -----
        self.CameraImage = util.replace_widget(self.CameraImage, camera_widget.CameraWidget((320,240)))
        self.BackCameraImage = util.replace_widget(self.BackCameraImage, camera_widget.CameraWidget((320,240)))
        #  ----- End Cameras -----
        
        #  ----- Begin Distance Bar -----.
        self.netTable.PutNumber("Distance",0)
        
        self.update_distance(None,0)
        network_tables.attach_fn(self.netTable, "Distance", self.update_distance, self.distanceBar)
        #  ----- End Battery Bar -----
        
        #  ----- Begin Arm -----
        self.netTable.PutNumber("ArmSet",0)
        self.netTable.PutNumber("ArmState",0)
        
        self.armStateButtonLockDown = self.image_button('armDownSel.png','armDown.png',False,self.armStateButtonLockDown,'clicked',self.on_ArmStateLockedDown_pressed)
        self.armStateButtonUnlock = self.image_button('armUnlockedSel.png','armUnlocked.png',False,self.armStateButtonUnlock,'clicked',self.on_ArmStateUnlocked_pressed)
        self.armStateButtonLockUp = self.image_button('armUpSel.png','armUp.png',False,self.armStateButtonLockUp,'clicked',self.on_ArmStateLockedUp_pressed)
        
        network_tables.attach_fn(self.netTable, "ArmState", self.update_arm_indicator, self.armStateButtonLockDown)
        
        #  ----- End Arm -----
        
        #  ----- Begin Timer -----
        glib.timeout_add_seconds(1, self.on_timer)
        #  ----- Begin Timer -----
        
        '''    
        #  ----- Begin Robot State Image -----
        self.netTable.PutBoolean("BallLoaded",False)
        active = util.pixbuf_from_file('RobotStateDownNoBall.png')
        inactive = util.pixbuf_from_file('toggle-off.png')
        #armstate one is down, two is disengaged, three is up
        if self.netTable.GetBoolean("BallLoaded")==False:
            if self.netTable.GetNumber("ArmState")==1 :
                x="RobotStateDownNoBall.png"
            elif self.netTable.GetNumber("ArmState")==2 :
                x="RobotStateUnlockedNoBall.png"
            elif self.netTable.GetNumber("ArmState")==3 :
                x="RobotStateUpNoBall.png"
        if self.netTable.GetBoolean("BallLoaded")==True:
            if self.netTable.GetNumber("ArmState")==1 :
                x="RobotStateDownYesBall.png"
            elif self.netTable.GetNumber("ArmState")==2 :
                x="RobotStateUnlockedYesBall.png"
            elif self.netTable.GetNumber("ArmState")==3 :
                x="RobotStateUpYesBall.png"
        
        stateimage = util.pixbuf_from_file(x)
        
        self.RobotStateImage = util.replace_widget(self.RobotStateImage, stateimage)
        #  ----- End Robot State Image -----
        '''
        
        if competition:
            self.window.move(0,0)
            self.window.resize(1356, 525)
            
        network_tables.attach_connection_listener(self.netTable, self.on_connection_connect, self.on_connection_disconnect, self.window)
        
        
        # show the window AND all of its child widgets. If you don't call show_all, the
        # children may not show up
        self.window.show_all()
        
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
        self.distanceBar.set_text(str(value)+" units")
    
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
        #self.timer.SetText('something')
        pass

    def on_connection_connect(self, remote):
        
        # this doesn't seem to actually tell the difference
        if remote.IsServer():
            logger.info("NetworkTables connection to robot detected")
        else:
            logger.info("NetworkTables connection to client detected")
         
        for processor in self.imageProcessors:   
            processor.start()
        #self.camera_widget.start()
        
    def on_connection_disconnect(self, remote):
        if remote.IsServer():
            logger.info("NetworkTables disconnected from robot")
        else:
            logger.info("NetworkTables disconnected from client")