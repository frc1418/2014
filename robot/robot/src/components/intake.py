'''
Created on Jan 25, 2014

@author: Owner
'''


class Intake(object):
    def __init__ (self,vent_up_solenoid,fill_up_solenoid,fill_down_solenoid,vent_down_solenoid,jaguar,solenoidTimer):
        
        self.vent_up_solenoid =vent_up_solenoid         #1 activates 2 makes neutral
        self.fill_up_solenoid =fill_up_solenoid
        self.fill_down_solenoid =fill_down_solenoid         #1 activates 2 makes neutral
        self.vent_down_solenoid =vent_down_solenoid
        self.jaguar=jaguar          
        self.u1solenoidval =False         #temp variables
        self.u2solenoidval =False
        self.d1solenoidval =False
        self.d2solenoidval =False
        self.jaguarval=0
        self.solenoidTimer=solenoidTimer
        self.dotimer=True
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
        if self.solenoidTimer.HasPeriodPassed(.2):
            self.u2solenoidval=True
            self.solenoidTimer.Reset()
            self.solenoidTimer.stop()
        
        if direction is 1:              #up
            self.u1solenoidval =False   
            self.u2solenoidval =False       #set this to True 200 seconds from active
            self.d1solenoidval =False
            self.d2solenoidval =True
            self.solenoidTimer.Reset()
            
        elif direction is 2:            #down
            self.u1solenoidval =True
            self.u2solenoidval =False
            self.d1solenoidval =True
            self.d2solenoidval =False
        else:
            self.u1solenoidval =True  #bouncing
            self.u2solenoidval =False
            self.d1solenoidval =False
            self.d2solenoidval =True
    
    def doit(self):
        if self.d1solenoidval==True:
            self.jaguar.Set(self.jaguarval)
        else:
            self.jaguar.Set(0)
        self.vent_up_solenoid.Set(self.u1solenoidval)
        self.fill_up_solenoid.Set(self.u2solenoidval)
        self.fill_down_solenoid.Set(self.d1solenoidval)
        self.vent_down_solenoid.Set(self.d2solenoidval)
        
        
        
        
