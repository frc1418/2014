'''
Created on Jan 25, 2014

@author: Owner
'''

class Intake(object):
    def __init__ (self,up_solenoid,down_solenoid,jaguar,solenoidTimer):
        
        self.up_solenoid =up_solenoid         #1 activates 2 makes neutral
        self.down_solenoid =down_solenoid
        self.jaguar=jaguar          
        self.u1solenoidval =False         #temp variables
        self.u2solenoidval =False
        self.d1solenoidval =False
        self.d2solenoidval =False
        self.jaguarval=0
        self.solenoidTimer=solenoidTimer
    #wheels function pulls in the ball and also spits the the ball out
    def wheels(self,direction,launcherup):
        #0 for stop, 1 for forward, -1 for backwards
            if direction >1 or direction < -1:
                self.jaguarval=0
            else:
                self.jaguarval=direction
    #arm controls the arm on the robot; trigger makes arm fall
    def arm(self,direction):
        #direction 0 or else=null,1=up,2=down
        if direction is 1:
            self.u1solenoidval =True
            self.u2solenoidval =False
            self.d1solenoidval =False
            self.d2solenoidval =False
        elif direction is 2:
            self.u1solenoidval =False
            self.u2solenoidval =False
            self.d1solenoidval =True
            self.d2solenoidval =False
        else:
            self.u1solenoidval =False
            self.u2solenoidval =True
            self.d1solenoidval =False
            self.d2solenoidval =True
    
    def doit(self):
        if self.d1solenoidval==True:
            self.jaguar.Set(self.jaguarval)
        else:
            self.jaguar.Set(0)
        self.up_solenoid.Set(self.u1solenoidval,self.u2solenoidval)
        self.down_solenoid.Set(self.d1solenoidval,self.d2solenoidval)
        
        
        
        
