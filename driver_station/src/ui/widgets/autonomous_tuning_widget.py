
import gtk

import network_tables
from .. import util

class AutonomousTuningWidget(gtk.VBox):
    
    AUTON_MAX = 15.0
    
    ui_filename = 'autonomous_tuning_widget.ui'
    
    ui_widgets = [
        'auto_chooser',
        'settings_vbox',
        'timing_settings_vbox',
        'widget'
    ]
    
    ui_signals = [
        'on_auto_chooser_changed'
    ]
    
    def __init__(self, table):
        gtk.VBox.__init__(self)
        util.initialize_from_xml(self)
        
        self.pack_start(self.widget, True, True)
        
        self.table = table
        self.tracked_keys = {}
        
        # setup attachments to things
        
        # listen to all keys
        network_tables.attach_fn(self.table, None, self.on_networktables_updated, self)
        
        # attach the chooser too
        # -> there's probably a race here. 
        network_tables.attach_chooser_combo(table, 'Autonomous Mode', self.auto_chooser)
      
    def __parse_name(self, name):
        
        vmin, vmax = -1.0, 1.0
        
        # parse the min/max value if it exists
        parsed_name = name.rsplit('|', 2)
        if len(parsed_name) == 3:
            name, vmin, vmax = parsed_name
            
        return name, float(vmin), float(vmax)
    
    def __create_widget(self, name, key, vmin, vmax):
        '''
            Creates a widget connected to a NetworkTables value
            
            TODO: Could use this elsewhere to dynamically create appropriate
                  widgets for NetworkTables values... 
        '''
        
        value = self.table.GetValue(key)
        
        needs_hbox = True
        
        if isinstance(value, bool):
        
            needs_hbox = False
            
            widget = gtk.CheckButton(label=name)
            widget.set_active(value)
            
            h_id = widget.connect('toggled', lambda w: self.table.PutBoolean(key, widget.get_active()))
        
            def update_fn(v):
                widget.handler_block(h_id)
                widget.set_active(v)
                widget.handler_unblock(h_id)
        
        elif isinstance(value, float):
            
            # TODO: set increments should be calculated
            widget = gtk.SpinButton(digits=2)
            widget.set_range(vmin, vmax)
            widget.set_increments(0.1, 1)
            widget.set_value(value)
        
            h_id = widget.connect('value-changed', lambda w: self.table.PutNumber(key, widget.get_value()))
            
            def update_fn(v):
                widget.handler_block(h_id)
                widget.set_value(v)
                widget.handler_unblock(h_id)
            
        elif isinstance(value, str):
        
            widget = gtk.Entry(max=80)
            widget.set_text(value)
    
            h_id = widget.connect('changed', lambda w: self.table.PutString(key, widget.get_text()))
            
            def update_fn(v):
                widget.handler_block(h_id)
                widget.set_text(v)
                widget.handler_unblock(h_id)
        else:
            return None
        
        self.tracked_keys[key] = update_fn
        
        # each object is its own thing
        if needs_hbox:
            hbox = gtk.HBox()
            hbox.set_spacing(5)
            
            hbox.pack_start(widget, False, False)
            hbox.pack_start(gtk.Label(name), False, False)
            
            return hbox
        
        return widget
        
    
    def clear(self):
        '''Clear out all of the things'''
        
        self.tracked_keys.clear()
        
        for c in self.settings_vbox.get_children():
            self.settings_vbox.remove(c)
            c.destroy()
            
        for c in self.timing_settings_vbox.get_children():
            self.timing_settings_vbox.remove(c)
            c.destroy()
            
        self.settings_vbox.hide()
        self.timing_settings_vbox.hide()
    
    
    def update_autonomous_tunables(self, mode_name):
        
        self.clear()
        
        # nothing else needs to happen here
        if mode_name == 'None':
            return
        
        # put new things in
        # -> TODO: There's some kind of bug with updating network tables array
        #          values. Most unfortunate. It seems to work most of the time
        #          however, so good enough for now
        
        # find the ordering of duration items
        try:
            durations = network_tables.get_array_value(self.table, mode_name + '_durations')
        except:
            durations = []
        
        for duration_name in durations:
            
            key = '%s\\%s_duration' % (mode_name, duration_name)
            
            widget = self.__create_widget(duration_name, key, 0, self.AUTON_MAX)
            
            if widget is None:
                continue
            
            try:
                description = self.table.GetString('%s\\%s_description' % (mode_name, duration_name))
            except:
                description = None
                
            if description is not None:
                widget.set_tooltip_text(description)
            
            self.timing_settings_vbox.pack_start(widget, False, True)
    
        if len(durations) > 0:
            self.timing_settings_vbox.show_all()
        
        # now setup the tunables
        try:
            tunables = network_tables.get_array_value(self.table, mode_name + '_tunables')
        except:
            tunables = []
        
        for tunable_name in tunables:
            
            tunable_name, vmin, vmax = self.__parse_name(tunable_name)
            key = '%s\\%s' % (mode_name, tunable_name)
            
            widget = self.__create_widget(tunable_name, key, vmin, vmax)
            
            if widget is None:
                continue
        
            self.settings_vbox.pack_start(widget, False, True)
        
        if len(tunables) > 0:
            self.settings_vbox.show_all()
            
        # setup update functions
        def updated_vars(v):
            self.update_autonomous_tunables(mode_name)
        
        self.tracked_keys[mode_name + '_durations'] = updated_vars
        self.tracked_keys[mode_name + '_tunables'] = updated_vars
    
    def on_auto_chooser_changed(self, widget):
      
        active = widget.get_active_iter()
        if not active:
            return 
            
        mode_name = widget.get_model()[active][0]
        self.update_autonomous_tunables(mode_name)
    
        
    def on_networktables_updated(self, key, value):
        '''
            Called when NetworkTables keys are updated
        '''
        
        # if the value is None, assume it is a StringArray
        if value is None:
            try:
                value = network_tables.get_array_value(self.table, key)
            except:
                pass
        
        # if there's a value we're displaying, then change its
        # contents based on this. or something. 
        
        update_fn = self.tracked_keys.get(key)
        if update_fn is not None:
            print "Autonomous tuner update:", key, value
            # .. beware of loop?
            update_fn(value)
        
    