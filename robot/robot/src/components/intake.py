'''
Created on Jan 25, 2014

@author: Owner
'''

ARM_STATE_UP = 1
ARM_STATE_DOWN = 2
ARM_STATE_FLOATING = 3


class Intake(object):
    def __init__ (self, vent_up_solenoid, fill_up_solenoid, fill_down_solenoid, vent_down_solenoid, jaguar, solenoidTimer):
        
        self.vent_up_solenoid = vent_up_solenoid  # 1 activates 2 makes neutral
        self.fill_up_solenoid = fill_up_solenoid
        self.fill_down_solenoid = fill_down_solenoid  # 1 activates 2 makes neutral
        self.vent_down_solenoid = vent_down_solenoid
        self.jaguar = jaguar          
       
        self.jaguarval = 0
        self.solenoidTimer = solenoidTimer
        self.dotimer = True
        self.armState=ARM_STATE_FLOATING
    # wheels function pulls in the ball and also spits the the ball out

    def wheelDoNothing(self):
        '''stops the wheel from doing anything'''
        self.jaguarval = 0
    def ballIn(self):
        '''spins the wheels to suck the ball in '''
        # 0 for stop, 1 for forward, -1 for backwards
        self.jaguarval = -1
    # arm controls the arm on the robot; trigger makes arm fall
    def ballOut(self):
        ''' spins the wheels to spit the ball out      '''       
        self.jaguarval = 1
    def armUp(self):
        ''' the pistons raise up the arm '''
        self.armState = ARM_STATE_UP
        self.solenoidTimer.Reset()
            
    def armDown(self):
        ''' the pistons bring the arm down'''
        self.armState = ARM_STATE_DOWN
        
    def armNeutral(self):
        ''' the arm is in default mode/ does nothing just '''
        self.armState = ARM_STATE_FLOATING
        
    def doit(self):
        ''' Makes everything work '''
        if self.armState==ARM_STATE_UP:
            u1solenoidval = False
            u2solenoidval = False
            d1solenoidval = True
            d2solenoidval = False
        elif self.armState==ARM_STATE_DOWN:
            u1solenoidval = True
            u2solenoidval = False
            d1solenoidval = True
            d2solenoidval = False
        elif self.armState==ARM_STATE_FLOATING:
            u1solenoidval = True  # bouncing
            u2solenoidval = False
            d1solenoidval = False
            d2solenoidval = True
        
        if self.solenoidTimer.HasPeriodPassed(.2):
            u2solenoidval = True
            self.solenoidTimer.Reset()
            self.solenoidTimer.stop()
        
        if d1solenoidval == True:
            self.jaguar.Set(self.jaguarval)
        else:
            self.jaguar.Set(0)
            self.vent_up_solenoid.Set(u1solenoidval)
            self.fill_up_solenoid.Set(u2solenoidval)
            self.fill_down_solenoid.Set(d1solenoidval)
            self.vent_down_solenoid.Set(d2solenoidval)
        self.jaguarval = 0
        
        
        
