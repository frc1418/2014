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

import gtk

import ui.util

class FrisbeeWidget(gtk.DrawingArea):
    '''
        While this does work, this is superceded by the robot widget
        and isn't actually used by the dashboard anymore.
    '''
    
    def __init__(self, table):
        gtk.DrawingArea.__init__(self)
        
        self.table = table
    
        # TODO: set up a listener or something.. 
        
        # load the frisbee pngs
        
        self.gray_frisbee = gtk.gdk.pixbuf_new_from_file(os.path.join(ui.util.data_dir, 'gray_frisbee.png'))
        self.red_frisbee = gtk.gdk.pixbuf_new_from_file(os.path.join(ui.util.data_dir, 'red_frisbee.png'))
        
        # set the
        self.count = 1
        self.max_frisbees = 4
        
        self.set_size_request(self.gray_frisbee.get_width(), self.gray_frisbee.get_height()* self.max_frisbees)
        
        self.connect('expose-event', self.on_expose)
        
    def set_frisbee_count(self, count):
        self.count = count
        self.queue_draw()
        
    def on_expose(self, widget, event):
        
        h = self.gray_frisbee.get_height()
        
        for i in xrange(self.max_frisbees):
            if i < self.count:
                # draw full frisbee
                event.window.draw_pixbuf(None, self.red_frisbee, 0, 0, 0, h*(self.max_frisbees-i))
            else:
                # draw empty frisbee
                event.window.draw_pixbuf(None, self.gray_frisbee, 0, 0, 0, h*(self.max_frisbees-i))
                
        
