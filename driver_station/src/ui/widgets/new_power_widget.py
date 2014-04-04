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

import cairo

from .. import util

class NewPowerWidget(gtk.DrawingArea):
    '''
        When the robot reports the angle of the platform, draw the
        platform on the UI at that particular angle. 
        
            TODO: Make this more general, we hardcoded everything here
    '''
    
    def __init__(self):
        gtk.DrawingArea.__init__(self)
        
        self.imageFG = util.surface_from_png('newPowerWidgetFront.png')
        
        self.size = self.imageFG.get_width()
        self.hypot = math.sqrt(2*math.pow(self.size,2))
        self.touch = False
        
        self.imageBG2 = util.surface_from_png('robotAngleWidgetBG.png')
        self.imageFG2 = util.surface_from_png('robotAngleWidgetFG.png')
        self.angle = 0
        
        self.power = 50
        self.precalc = 2*self.hypot*((100.0-self.power)/100.0)
        self.set_size_request(self.size, self.size)
        
        self.connect('expose-event', self.on_expose)
        
        self.add_events(gtk.gdk.POINTER_MOTION_MASK |
            gtk.gdk.BUTTON_PRESS_MASK |
            gtk.gdk.BUTTON_RELEASE_MASK)
        
        self.connect('button-press-event', self.press)
        self.connect('button-release-event', self.release)
        self.connect('motion-notify-event', self.motion)
    
    def update(self, key, value):
        self.set_power(value)
    
    def calcRun(self, x, y):
        #Formula to translate x,y into power
        Xc = 200
        Yc = 100
        #Xm = 0     XM = Xc
        #Ym = Yc    YM = 300
        raw = 0.0
        x2 = self.map((x-Xc),0.0,Xc,0.0,1.0)
        y2 = self.map((y-Yc),0.0,self.size,0.0,1.0)
        try:
            raw = math.atan(x2/y2)
        except:
            print("hi")
        #TODO Debug math, this is a quick hack to get 1 to 0
        processed = math.degrees(raw)
        print("X:"+str(x2)+"  Y:"+str(y2)+"  Raw:"+str(raw)+"  Pro:"+str(processed))
        return 0
    
    def motion(self, widget, event):
        if(self.touch):
            print("Potato, x:"+str(event.x)+"  y:"+str(event.y))
            self.calcRun(event.x,event.y)
    
    def press(self, widget, event):
        self.touch = True
        self.calcRun(event.x,event.y)
        
    def release(self, widget, event):
        self.touch = False
    
    def map(self, x, in_min, in_max, out_min, out_max):
        calced = (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
        return calced
    
    def set_power(self, power):
        if power != self.power:
            self.power = power
            self.precalc = self.hypot*((100.0-self.power)/100.0)
            self.queue_draw()
            
    #-----copied from the robot_widget
        def updatearm(self, key, value):
        self.set_arm_angle(value)
    
    def updatecatapult
    
    (self, key, value):
        self.set_catapult_angle(value)
        self.set_ball_angle(value)
        
    def updateball(self, key, value):
        self.set_ball_location(value)
    
    def set_catapult_angle(self, catapultangle1):
        if catapultangle1 != self.catapultangle:
            self.catapultangle = catapultangle1
            self.queue_draw()
    
    def set_arm_angle(self, armangle1):
        if armangle1==0:
            pass
        elif armangle1 != self.armangle :
            self.armangle = armangle1
            self.queue_draw()
        
    def set_ball_location(self, isthere):
        if isthere==True:
            self.isthere=True
        if isthere==False:
            self.isthere=False
    
        self.queue_draw()
    
    def set_ball_angle(self, ballangle1):
        if ballangle1 != self.ballangle:
            self.ballangle = ballangle1
            self.queue_draw()
    #---- so yea -----------------------------
        
    def on_expose(self, widget, event):
        cxt = event.window.cairo_create()
        cxt.save()
        cxt.save()
        # ----- Begin Gradient -----
        grd = cairo.LinearGradient(0.0, 0.0, self.size, self.size)
        
        #add_color_stop_rgba(percent[0.0-1.0],r,g,b,a)
        grd.add_color_stop_rgba(0.0, 1.0, 1.0, 0.0, 1.0)    
        grd.add_color_stop_rgba(1.0, 1.0, 0.0, 0.0, 1.0)

        cxt.rectangle(0, 0, self.size, self.size);
        cxt.set_source(grd)
        cxt.fill()
        
        cxt.paint()
        # ----- End Gradient -----
        cxt.restore()
        
        cxt.save()
        # ----- Begin Cover Rectangle -----
        calc = self.power*self.size
        print("I'm a potato:"+str(self.precalc))
        cxt.rotate(math.radians(45))
        cxt.translate(0-(self.precalc/2),0-(self.precalc/2))
        cxt.rectangle(0,0,self.precalc,self.precalc)
        cxt.set_source_rgb(0.0,0.0,0.0)
        
        cxt.clip()
        cxt.paint()
        # ----- End Cover Rectangle -----
        cxt.restore()
        
        # ----- Begin Faceplate -----
        cxt.set_source_surface(self.imageFG)
        # ----- End Faceplate -----
        
        cxt.paint()