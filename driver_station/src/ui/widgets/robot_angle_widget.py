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
    
    def __init__(self, NetworkTable):
        self.netTable = NetworkTable
        
        gtk.DrawingArea.__init__(self)
        self.imageBG = util.surface_from_png('robotAngleWidgetBG.png')
        self.imageFG = util.surface_from_png('robotAngleWidgetFG.png')
        

        self.angle = 0
        self.set_size_request(150,150)
        
        self.connect('expose-event', self.on_expose)
    
    '''def connect(self, table, key):
        import network_tables
        network_tables.attach_fn(table, key, self.update, self)'''
    
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
        x=self.netTable.GetNumber('GyroAngle')
        print (self.netTable.GetNumber('GyroAngle'), math.radians(self.netTable.GetNumber('GyroAngle')))
        cxt.translate(75,75)
        cxt.rotate(math.radians(x))
        cxt.translate(-75,-75)

        cxt.set_source_surface(self.imageFG)
        '''# the math
        x = math.cos(self.angle)
        y = math.sin(self.angle)
        l = math.sqrt(x^2+y^2)
        
        cxt.set_font_size(20)
        cxt.show_text('%.2f' % self.angle)
        cxt.stroke()
        '''
        
        
        cxt.paint()