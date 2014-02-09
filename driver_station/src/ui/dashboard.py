import util

from widgets import toggle_button

class Dashboard():

    # glade file to load
    ui_filename = "DashboardMain.ui"
    
    # widgets to load from the glade file. Each one of these is added to 'self' after
    # you call 'initialize_from_xml'
    ui_widgets = [
        "shootPowerBar",
        "toggleButton",
        "window1",
    ]
    
    # these are functions that are called when an event happens.
    # -- the events can be setup in the 'signals' property in glade. A list of each signal
    #    and its associated functions can be found for each widget in the PyGTK docs.
    #    For example, the button pressed signal is documented at
    #    http://www.pygtk.org/docs/pygtk/class-gtkbutton.html#signal-gtkbutton--pressed
    ui_signals = [
        'on_PowerSelectButton5_pressed',
    ]
    
    def __init__(self):
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
        
        
        # show the window AND all of its child widgets. If you don't call show_all, the
        # children may not show up
        self.window1.show_all()
        
        
    def on_PowerSelectButton5_pressed(self, widget):
        '''
            demo: Called when the '5' button is clicked. This signal was configured
                  using glade
        '''
        
        print("Button 5 was pressed")
        
        # demo: change the value of the shoot power bar
        self.shootPowerBar.set_value(75)
        
    def on_toggleButton_toggled(self, widget):
        '''This signal was configured at runtime, and not specified in glade'''
        print("Button was toggled")
    
        