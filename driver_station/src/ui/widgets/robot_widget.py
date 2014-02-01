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

import ui.util

class RobotWidget(gtk.DrawingArea):
    '''
        When the robot reports the angle of the platform, draw the
        platform on the UI at that particular angle. 
        
        Additionally, show frisbees on the platform, and move them with
        it. In practice, operators rarely use this widget. However, its 
        a great visual aid for demonstrations, or for debugging the 
        robot. 
    
        TODO: Make this more general, we hardcoded everything here
    '''
    
    def __init__(self, table):
        gtk.DrawingArea.__init__(self)
        
        self.table = table
        self.angle = 0
    
        # TODO: set up a listener or something.. 
        
        # load the frisbee pngs
        
        self.robot = ui.util.pixbuf_from_file('robot.png')
        self.gray_frisbee = ui.util.surface_from_png('gray_frisbee.png')
        self.red_frisbee = ui.util.surface_from_png('red_frisbee.png')
        
        # setup the frisbee data
        # -> TODO
        self.count = 0
        self.max_frisbees = 4
        
        # size request
        self.set_size_request(self.robot.get_width(), self.robot.get_height())
        
        self.connect('expose-event', self.on_expose)
        
    def set_frisbee_count(self, count):
        if count < 0:
            count = 0
        elif count > self.max_frisbees:
            count = self.max_frisbees
            
        if self.count != count:
            self.count = count
            self.queue_draw()
        
    def set_angle(self, angle):
        if angle < 0:
            angle = 0.0
        elif angle > 50.0:
            angle = 50.0
        
        if angle != self.angle:
            self.angle = angle
            self.queue_draw()
        
    def on_expose(self, widget, event):
        
        # background
        event.window.draw_pixbuf(None, self.robot, 0, 0, 0, 0)
        
        cxt = event.window.cairo_create()
        
        # angle text
        cxt.move_to(220, 100)
        cxt.set_font_size(20)
        cxt.show_text('%.2f' % self.angle)
        
        cxt.set_source_rgb(0,0,0)
        cxt.fill_preserve()
        cxt.stroke()
        
        # platform angle thing
        cxt.translate(166,62)
        cxt.rotate(math.radians(-self.angle))
        cxt.translate(-166,-62)
        
        cxt.set_line_width(3)
        cxt.set_source_rgb(0,0,0)
        
        cxt.line_to(73,61)
        cxt.line_to(240,61)
        cxt.stroke()
        
        cxt.line_to(85,61)
        cxt.line_to(85,17)
        cxt.line_to(148,17)
        cxt.line_to(148,61)
        cxt.stroke()
        
        # draw the frisbees
        w = self.gray_frisbee.get_height()
        h = self.gray_frisbee.get_height()
        
        for i in xrange(self.max_frisbees):
            if i < self.count:
                cxt.set_source_surface(self.red_frisbee, 86, h*(self.max_frisbees-i) + 8)
            else:
                cxt.set_source_surface(self.gray_frisbee, 86, h*(self.max_frisbees-i) + 8)
                
            cxt.rectangle(0, 0, w, h)
            cxt.paint()

