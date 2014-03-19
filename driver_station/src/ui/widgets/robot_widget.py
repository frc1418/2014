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
        
        w = self.imageBG.get_width()
        h = self.imageBG.get_height()
        
        self.armangle = 0
        self.catapultangle = 0
        self.set_size_request(w, h)
        
        self.connect('expose-event', self.on_expose)
                
    def updatearm(self, key, value):
        self.set_arm_angle(value)
    
    def updatecatapult(self, key, value):
        self.set_catapult_angle(value)
    
    def set_catapult_angle(self, catapultangle1):
        if catapultangle1 != self.catapultangle:
            self.catapultangle = catapultangle1
            self.queue_draw()
    
    def set_arm_angle(self, armangle1):
        if armangle1 != self.armangle :
            self.armangle = armangle1
            self.queue_draw()
    
        
    def on_expose(self, widget, event):
        cxt = event.window.cairo_create()
        #-------------the background------------
        cxt.set_source_surface(self.imageBG)
        cxt.paint()
        #-------------the background------------
        #-------------the catapult-------------------
        cxt.translate(125,125)
        cxt.rotate(math.radians(self.catapultangle))
        cxt.translate(-125,-125)
        cxt.set_source_surface(self.imagecatapultarm)
        cxt.paint()
        #-------------the catapult-------------------
        #-------------the arm------------------------
        cxt.translate(125,125)
        cxt.rotate(math.radians(self.armangle))
        cxt.translate(-125,-125)
        cxt.set_source_surface(self.imageFG)
        cxt.paint()
        #-------------the arm------------------------
        
