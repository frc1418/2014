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

import os

import cairo
import gtk
import glib

data_dir = os.path.join(os.path.dirname(__file__), 'data')

def initialize_from_xml(this, other=None):
    '''
        Initializes the widgets and signals from a GtkBuilder XML file. Looks 
        for the following attributes in the instance you pass:
        
        ui_filename = builder filename
        ui_widgets = [list of widget names]
        ui_signals = [list of function names to connect to a signal]
        
        For each widget in ui_widgets, it will be retrieved from the builder
        object and 
        
        other is a list of widgets to also initialize with the same file
        
        Returns the builder object when done
    '''
    builder = gtk.Builder()
    builder.add_from_file(os.path.join(data_dir, this.ui_filename))
    
    objects = [this]
    if other is not None:
        objects.extend(other)
    
    for obj in objects:
        if hasattr(obj, 'ui_widgets') and obj.ui_widgets is not None:
            for widget_name in obj.ui_widgets:
                widget = builder.get_object(widget_name)
                if widget is None:
                    raise RuntimeError("Widget '%s' is not present in '%s'" % (widget_name, this.ui_filename))
                setattr(obj, widget_name, widget)
    
    signals = None
    
    for obj in objects:
        if hasattr(obj, 'ui_signals') and obj.ui_signals is not None:
            if signals is None:
                signals = {}
            for signal_name in obj.ui_signals:
                if not hasattr(obj, signal_name):
                    raise RuntimeError("Function '%s' is not present in '%s'" % (signal_name, obj))
                signals[signal_name] = getattr(obj, signal_name)
            
    if signals is not None:
        missing = builder.connect_signals(signals, None)
        if missing is not None:
            err = 'The following signals were found in %s but have no assigned handler: %s' % (this.ui_filename, str(missing))
            raise RuntimeError(err)
    
    return builder


def replace_widget(old_widget, new_widget):
    
    # TODO: This could be better
    
    parent = old_widget.get_parent()                                                                                                                                                                                                           
    packing = None                                                                                                                                                                                                                             
    position = None                                                                                                                                                                                                                            
                                                                                                                                                                                                                                               
    try:                                                                                                                                                                                                                                       
        position = parent.child_get_property(old_widget, 'position')                                                                                                                                                                           
    except:                                                                                                                                                                                                                                    
        pass                                                                                                                                                                                                                                   
                                                                                                                                                                                                                                               
    try:                                                                                                                                                                                                                                       
        packing = parent.query_child_packing(old_widget)                                                                                                                                                                                       
    except:                                                                                                                                                                                                                                    
        pass
    
    table_options = {}
    
    try:
        # save/restore table options
        for prop in ['bottom-attach', 'left-attach', 'right-attach', 'top-attach', 'x-options', 'x-padding', 'y-options', 'y-padding']:
            table_options[prop] = parent.child_get_property(old_widget, prop)
    except:
        pass                                                                                                                                                                                                                              
                                                                                                                                                                                                                                               
    parent.remove(old_widget)                                                                                                                                                                                                                  
    new_widget.unparent()                                                                                                                                                                                                                      
    parent.add(new_widget)                                                                                                                                                                                                                     
    
    if len(table_options) != 0:
        for k, v in table_options.iteritems():  
            parent.child_set_property(new_widget, k, v)
                                                                                                                                                                                                                                               
    if position is not None:                                                                                                                                                                                                                   
        parent.child_set_property(new_widget, 'position', position)                                                                                                                                                                            
                                                                                                                                                                                                                                               
    if packing is not None:                                                                                                                                                                                                                    
        parent.set_child_packing(new_widget, *packing)  
        
    
        
    return new_widget

def pixbuf_from_stock(stock_id, stock_size):
    render_widget = gtk.Button()
    return render_widget.render_icon(stock_id, stock_size)

def pixbuf_from_file(filename):
    return gtk.gdk.pixbuf_new_from_file(os.path.join(data_dir, filename))

def surface_from_png(filename):
    return cairo.ImageSurface.create_from_png(os.path.join(data_dir, filename))

def get_directory(default=None):
    dialog = gtk.FileChooserDialog("Open directory", action=gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER,
                                                     buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK))
    
    if default is not None:
        dialog.set_current_folder(default)
    
    response = dialog.run()
    
    if response != gtk.RESPONSE_OK:
        return None
    
    ret = dialog.get_filename()
    dialog.destroy()
    
    return ret

def get_text(parent, message, default='', validator=None):
    """
    Display a dialog with a text entry.
    Returns the text, or None if canceled.
    
    Modified from http://stackoverflow.com/questions/8290740/
    """
    d = gtk.MessageDialog(parent,
                          gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                          gtk.MESSAGE_QUESTION,
                          gtk.BUTTONS_OK_CANCEL,
                          message)
    entry = gtk.Entry()
    entry.set_text(default)
    entry.show()
    d.vbox.pack_end(entry)
    entry.connect('activate', lambda _: d.response(gtk.RESPONSE_OK))
    d.set_default_response(gtk.RESPONSE_OK)

    while True:
        r = d.run()
        text = entry.get_text()
    
        if r != gtk.RESPONSE_OK:
            text = None
            break
    
        if validator is not None:
            response = validator(text)
            if response is not True:
                d.format_secondary_markup('<b>ERROR</b>: <span foreground="red">%s</span>' % 
                                          glib.markup_escape_text(response))
                entry.grab_focus()
                continue
        break
            
    
    d.destroy()
    return text

def show_error(parent, message):
    '''Shows an error message to the user'''
    dialog = gtk.MessageDialog(parent, type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_CLOSE)
    dialog.set_property('text',message)
    dialog.run()
    dialog.destroy()
    
def yesno(parent, message):
    '''Gets a Yes/No response from a user'''
    dlg = gtk.MessageDialog(parent=parent, type=gtk.MESSAGE_QUESTION, buttons=gtk.BUTTONS_YES_NO, message_format=message)
    response = dlg.run() 
    dlg.destroy()
    return response
