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

class RobotStateImage(gtk.DrawingArea):
    '''
        When the robot reports the angle of the platform, draw the
        platform on the UI at that particular angle. 
        
        Additionally, show frisbees on the platform, and move them with
        it. In practice, operators rarely use this widget. However, its 
        a great visual aid for demonstrations, or for debugging the 
        robot. 
    
    '''
    def __init__(self):
        gtk.DrawingArea.__init__(self)
        
        self.imageBG = util.surface_from_png('framebase.png')
        self.imageFG = util.surface_from_png('robotarm.png')
        self.imagecatapultarm = util.surface_from_png('Catapultarm.png')
        self.imageball= util.surface_from_png('ballpicture.png')
        
        w = self.imageBG.get_width()
        h = self.imageBG.get_height()
        
        self.armangle = 0
        self.catapultangle = 0
        self.ballangle = 0
        self.set_size_request(w, h)
        self.isthere=True
        
        self.connect('expose-event', self.on_expose)
                
    def updatearm(self, key, value):
        self.set_arm_angle(value)
    
    def updatecatapult(self, key, value):
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
    
    def set_ball_angle(self, ballangle1):
        if ballangle1 != self.ballangle:
            self.ballangle = ballangle1
            self.queue_draw()
    
        
    
        
    def on_expose(self, widget, event):
        cxt = event.window.cairo_create()
        #-------------the background------------
        cxt.set_source_surface(self.imageBG)
        cxt.paint()
        #-------------the background------------
        #-------------the catapult-------------------
        cxt.save()
        cxt.translate(125,125)
        #--this translates the angle from raw 100-0 into 100=0, 0=90 using the function Y=.9X+90
        fixedcatapult=(-0.9*self.catapultangle)+90
        cxt.rotate(math.radians(-fixedcatapult))
        cxt.translate(-125,-125)
        cxt.set_source_surface(self.imagecatapultarm)
        cxt.paint()
        cxt.restore()
        #-------------the catapult-------------------
        #-------------the arm------------------------
        cxt.save()
        cxt.translate(125,125)
        #--this turns arm state 1 to no rotation, 2 to small upwords 3 to -90 degrees
        fixedarm=0
        if self.armangle==1:
            fixedarm=0
        if self.armangle==2:
            fixedarm=-10
        if self.armangle==3:
            fixedarm=-90
        cxt.rotate(math.radians(fixedarm))
        cxt.translate(-125,-125)
        cxt.set_source_surface(self.imageFG)
        cxt.paint()
        cxt.restore()
        #-------------the arm------------------------
        #-------------the ball------------------------
        cxt.save()
        if self.isthere==True:
            ###so the ball has the same rotations as the catapult, just copied the code
            cxt.translate(125,125)
            #--this translates the angle from raw 100-0 into 100=0, 0=90 using the function Y=.9X+90
            fixedball=(-0.9*self.ballangle)+90
            cxt.rotate(math.radians(-fixedball))
            cxt.translate(-125,-125)        
            cxt.set_source_surface(self.imageball)
            cxt.paint()
            cxt.restore()
        #-------------the ball------------------------
        