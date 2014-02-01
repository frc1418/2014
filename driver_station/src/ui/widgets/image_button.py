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

import gtk
import gobject

class ImageButton(gtk.EventBox):
    '''
        Not sure why this doesn't exist in GTK. You can sort of do this.. 
        but not really.  
    '''
    
    __gsignals__ = {
        'clicked': (gobject.SIGNAL_ACTION, gobject.TYPE_NONE, ()), 
    }
    
    def __init__(self, default_pixbuf=None):
        gtk.EventBox.__init__(self)
        
        self.image = gtk.Image()
        self.add(self.image)
        
        self.add_events(gtk.gdk.BUTTON_PRESS_MASK)
        self.connect('button-press-event', self.on_button_press)
        
        if default_pixbuf is not None:
            self.set_from_pixbuf(default_pixbuf)
        
    def on_button_press(self, widget, event):
        if event.button == 1 and event.type == gtk.gdk.BUTTON_PRESS:
            self.emit('clicked')
        
    def set_from_pixbuf(self, pixbuf):
        self.image.set_from_pixbuf(pixbuf)
        
gobject.type_register(ImageButton)
