'''
Created on Jan 25, 2014

@author: Owner
'''

class intake(object):
    def __init__ (self,solenoid,jaguar):
        
        self.solenoid =solenoid         #components
        self.jaguar=jaguar
        self.solenoidval=false          #temp variables
        self.jaguarval=0
    #wheels function pulls in the ball and also spits the the ball out
    def wheels(self,direction):
        #0 for stop, 1 for foreward, -1 for backwards
        if direction >1 or direction < -1:
            direction=0
        else:
            self.jaguarval=direction
    #arm controls the arm on the robot; trigger makes arm fall
    def arm(self, active):
        if active is True:
            self.solenoidval = True    
        else:
            self.solenoidval = False 
    
    def doit(self):
         self.jaguar.Set(jaguarval)
         self.solenoid.Set(solenoidval)