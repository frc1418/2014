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


import math
import os

import gtk

from .. import util

class RobotAngleWidget(gtk.DrawingArea):
    '''
        When the robot reports the angle of the platform, draw the
        platform on the UI at that particular angle. 
        
        Additionally, show frisbees on the platform, and move them with
        it. In practice, operators rarely use this widget. However, its
        a great visual aid for demonstrations, or for debugging the 
        robot. 
    
            TODO: Make this more general, we hardcoded everything here
    '''
    
    def __init__(self):
        gtk.DrawingArea.__init__(self)

        self.angle = 0
        self.size = 150
        
        #self.background = util.pixbuf_from_file("robotAngleWidgetBG.png")
        #self.indicator = util.pixbuf_from_file("robotAngleWidgetFG.png")
    
    
    '''def connect(self, table, key):
        import network_tables
        network_tables.attach_fn(table, key, self.update, self)'''
    
    def update(self, key, value):
        self.set_angle(value)
    
    def set_angle(self, angle):
        angle = angle % 360
        
        if angle != self.angle:
            self.angle = angle
            self.queue_draw()
        
    def on_expose(self, widget, event):
        
        # background
        event.window.draw_pixbuf(None, self.background, 0, 0, 150, 150)
        event.window.draw_pixbuf(None, self.indicator, 0, 0, 150, 150)
        
        cxt = event.window.cairo_create()
        
        # angle text
        cxt.move_to(75, 75)
        cxt.set_line_width(3)
        cxt.set_source_rgb(0,0,0)
        
        # the math
        x = math.cos(self.angle)
        y = math.sin(self.angle)
        l = math.sqrt(x^2+y^2)
        
        cxt.line_to(x*l+75,y*l+75)
        
        cxt.set_font_size(20)
        cxt.show_text('%.2f' % self.angle)
        
        cxt.set_source_rgb(0,0,0)
        cxt.fill_preserve()
        cxt.stroke()

