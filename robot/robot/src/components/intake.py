'''
Created on Jan 25, 2014

@author: Owner
'''

class Intake(object):
    def __init__ (self,solenoid,jaguar,solenoidTimer):
        
        self.solenoid =solenoid         #components
        self.jaguar=jaguar
        self.solenoidval=False          #temp variables
        self.jaguarval=0
        self.solenoidTimer=solenoidTimer
    #wheels function pulls in the ball and also spits the the ball out
    def wheels(self,direction,launcherup):
        #0 for stop, 1 for forward, -1 for backwards
        if launcherup==False:
            if direction >1 or direction < -1:
                self.jaguarval=0
            else:
                self.jaguarval=direction
    #arm controls the arm on the robot; trigger makes arm fall
    def arm(self, active):
        if active is True:
            self.solenoidval = True    
        else:
            self.solenoidval = False 
    
    def doit(self):
        if self.solenoidval==True:
            self.jaguar.Set(jaguarval)
        self.solenoid.Set(solenoidval)
        
        
        
        
