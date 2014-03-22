import math
import os

import gtk

import cairo

from .. import util

class RobotAngleWidget(gtk.DrawingArea):
    '''
        When the robot reports the angle of the platform, draw the
        platform on the UI at that particular angle. 
        
            TODO: Make this more general, we hardcoded everything here
    '''
    
    def __init__(self):
        gtk.DrawingArea.__init__(self)
        
        self.imageBG = util.surface_from_png('robotAngleWidgetBG.png')
        self.imageFG = util.surface_from_png('robotAngleWidgetFG.png')
        
        w = self.imageBG.get_width()
        h = self.imageBG.get_height()
        
        self.angle = 0
        self.set_size_request(w, h)
        
        self.connect('expose-event', self.on_expose)
    
    def update(self, key, value):
        self.set_angle(value)
    
    def set_angle(self, angle):
        if angle != self.angle:
            self.angle = angle
            self.queue_draw()
        
    def on_expose(self, widget, event):
        cxt = event.window.cairo_create()
        
        cxt.set_source_surface(self.imageBG)
        cxt.paint()
        
        cxt.translate(54,54)
        cxt.rotate(math.radians(self.angle))
        cxt.translate(-54,-54)

        cxt.set_source_surface(self.imageFG)
        
        cxt.paint()
