#
#    This file is part of Team 1418 Dashboard
#
#    Team 1418 Dashboard is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, version 3.
#
#    Team 1418 Dashboard is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Team 1418 Dashboard.  If not, see <http://www.gnu.org/licenses/>.
#


import math
import os

import gtk
import gobject

import cairo

from .. import util

class RobotAngleWidget(gtk.EventBox):
    '''
        When the robot reports the angle of the platform, draw the
        platform on the UI at that particular angle. 
        
            TODO: Make this more general, we hardcoded everything here
    '''
    
    __gsignals__ = {
        'angle-enabled-changed': (gobject.SIGNAL_ACTION, gobject.TYPE_NONE, ()), 
    }
    
    def __init__(self):
        gtk.EventBox.__init__(self)
        
        self.drawingArea = gtk.DrawingArea()
        self.add(self.drawingArea)
        
        self.imageBG = util.surface_from_png('robotAngleWidgetBG.png')
        self.imageFG = util.surface_from_png('robotAngleWidgetFG.png')
        self.disabledImage = util.surface_from_png('robotAngleDisabled.png')
        
        w = self.imageBG.get_width()
        h = self.imageBG.get_height()
        
        self.angle_enabled = True
        self.angle = 0
        self.set_size_request(w, h)
        
        self.connect('button-press-event', self.on_button_press_event)
        self.drawingArea.connect('expose-event', self.on_expose)
    
    def update(self, key, value):
        self.set_angle(value)
    
    def set_angle(self, angle):
        if angle != self.angle:
            self.angle = angle
            self.queue_draw()
            
    def set_angle_enabled(self, value):
        self.angle_enabled = value
        self.queue_draw()
        
        self.emit('angle-enabled-changed')
            
    def on_button_press_event(self, widget, event):
        self.set_angle_enabled(not self.angle_enabled)
        
    def on_expose(self, widget, event):
        cxt = event.window.cairo_create()
        
        cxt.set_source_surface(self.imageBG)
        cxt.paint()
        
        cxt.save()
        cxt.translate(54,54)
        cxt.rotate(math.radians(self.angle))
        cxt.translate(-54,-54)

        cxt.set_source_surface(self.imageFG)
        
        cxt.paint()
        cxt.restore()
        
        if not self.angle_enabled:
            cxt.set_source_surface(self.disabledImage)
            cxt.paint()

gobject.type_register(RobotAngleWidget)
