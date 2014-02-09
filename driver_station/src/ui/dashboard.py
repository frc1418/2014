import util

from widgets import toggle_button, image_button, network_tables

class Dashboard():

    # glade file to load
    ui_filename = "DashboardMain.ui"
    
    # widgets to load from the glade file. Each one of these is added to 'self' after
    # you call 'initialize_from_xml'
    ui_widgets = [
        "shootPowerBar",
        "toggleButton",
        "window1",
        "FireButton",
        "batteryBar",
        "armIndicator",
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
        'on_ArmStateLockedDown_pressed',
        'on_ArmStateUnlocked_pressed',
        'on_ArmStateLockedUp_pressed',
    ]
    
    def __init__(self, NetworkTable):
        self.netTable = NetworkTable
        util.initialize_from_xml(self)
        
        # demo: load the images into pixbufs so that Gtk can use them
        active = util.pixbuf_from_file('toggle-on.png')
        inactive = util.pixbuf_from_file('toggle-off.png')
        
        # demo: create a ToggleButton widget. There are lots of widgets you can create
        real_widget = toggle_button.ToggleButton(active, inactive, clickable=True)
        
        # demo: replace a fake widget in the glade file with a 'real' widget
        util.replace_widget(self.toggleButton, real_widget)
        
        # demo: connect to the toggled event of the real widget, so that our
        #       function gets called when the button state is changed
        real_widget.connect('toggled', self.on_toggleButton_toggled)
        
        #  ----- Begin Fire Button -----
        active = util.pixbuf_from_file('Fire-Good-Compress.png')
        inactive = util.pixbuf_from_file('Fire-Bad-Compress.png')
        self.FireButton = util.replace_widget(self.FireButton, image_button.ImageButton(inactive))
        self.FireButton.connect('clicked', self.on_fire_clicked)
        
        # save these for later
        self.FireButton.active_pixbuf = active
        self.FireButton.inactive_pixbuf = inactive
        #  ----- End Fire Button -----
        
        #  ----- Begin Battery Bar -----
        self.netTable.PutNumber("Battery",0)
        
        self.update_battery(None,0)
        network_tables.attach_fn(self.netTable, "Battery", self.update_battery, self.batteryBar)
        #  ----- End Battery Bar -----
        
        #  ----- Begin Arm -----
        self.netTable.PutNumber("ArmSet",0)
        self.netTable.PutNumber("ArmState",0)
        
        network_tables.attach_fn(self.netTable, "ArmState", self.update_arm_indicator, self.armIndicator)
        
        #  ----- End Arm -----
        
        # show the window AND all of its child widgets. If you don't call show_all, the
        # children may not show up
        self.window1.show_all()
        
    def update_arm_indicator(self, key, value):
        self.armIndicator.set_text(str(value))
        
    def update_battery(self, key, value):
        self.batteryBar.set_value(value)
        
    def on_ArmStateLockedDown_pressed(self, widget):
        print("Arm Locked Down was pressed")
        self.netTable.PutNumber('ArmState',1)
        
    def on_ArmStateUnlocked_pressed(self, widget):
        print("Arm Unlocked was pressed")
        self.netTable.PutNumber('ArmState',2)
        
    def on_ArmStateLockedUp_pressed(self, widget):
        print("Arm Locked Up was pressed")
        self.netTable.PutNumber('ArmState',3)
        
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
        
    def on_toggleButton_toggled(self, widget):
        '''This signal was configured at runtime, and not specified in glade'''
        print("Button was toggled")
    
        