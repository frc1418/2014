import gtk
import pygtk
import util

from widgets import toggle_button, image_button, network_tables

class Dashboard():
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
    
    def __init__(self, NetworkTable):
        self.netTable = NetworkTable
        util.initialize_from_xml(self)
        fire=True
        
        self.shootPower = [10, 30, 50, 70, 90]
        self.currentShootPower = 4
        
        self.window.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse('#aaaaaa'))        
        
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
        
        #  ----- Begin Distance Bar -----
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
        
        # show the window AND all of its child widgets. If you don't call show_all, the
        # children may not show up
        self.window.show_all()
        
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
        self.shootPowerBar.set_value(20)
        self.netTable.PutNumber('FirePower',20)
        
    def on_RoughAdjustFirePower2_pressed(self, widget):
        print("Button 2 was pressed")
        self.shootPowerBar.set_value(40)
        self.netTable.PutNumber('FirePower',40)
        
    def on_RoughAdjustFirePower3_pressed(self, widget):
        print("Button 3 was pressed")
        self.shootPowerBar.set_value(60)
        self.netTable.PutNumber('FirePower',60)
        
    def on_RoughAdjustFirePower4_pressed(self, widget):
        print("Button 4 was pressed")
        self.shootPowerBar.set_value(80)
        self.netTable.PutNumber('FirePower',80) 

    def on_RoughAdjustFirePower5_pressed(self, widget):
        print("Button 5 was pressed")
        self.shootPowerBar.set_value(100)
        self.netTable.PutNumber('FirePower',100)
        
    def on_fire_clicked(self, widget):
        print("Fire!")
        
    def on_shoot_power_down_pressed(self, widget):
        print("Reduce shoot power")
        power = self.shootPower[self.currentShootPower]
        min = self.currentShootPower*20
        max = (self.currentShootPower+1)*20
        print(str(power)+":"+str(min)+":"+str(max))
        if(min<power):
            power = power - 2
            self.shootPower[self.currentShootPower]=power
            self.shootPowerBar.set_value(power)
            self.shootPowerBar.set_text(str(power))
        
    def on_shoot_power_up_pressed(self, widget):
        print("Increase shoot power")
        power = self.shootPower[self.currentShootPower]
        min = self.currentShootPower*20
        max = (self.currentShootPower+1)*20
        print(str(power)+":"+str(min)+":"+str(max))
        if(power<max):
            power = power + 2
            self.shootPower[self.currentShootPower]=power
            self.shootPowerBar.set_value(power)
            self.shootPowerBar.set_text(str(power))
            
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
        