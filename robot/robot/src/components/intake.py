'''
Created on Jan 25, 2014

@author: Owner
'''

ARM_STATE_UP = 1
ARM_STATE_DOWN = 3
ARM_STATE_FLOATING = 2


class Intake(object):
    '''This class makes the arm do things'''
    def __init__ (self, vent_up_solenoid, fill_up_solenoid, fill_down_solenoid, vent_down_solenoid, jaguar, solenoidTimer):

        '''Constructor'''
        
        self.vent_up_solenoid = vent_up_solenoid  # 1 activates 2 makes neutral
        self.fill_up_solenoid = fill_up_solenoid
        self.fill_down_solenoid = fill_down_solenoid  # 1 activates 2 makes neutral
        self.vent_down_solenoid = vent_down_solenoid
        self.jaguar = jaguar          
       
        self.jaguarval = 0
        self.solenoidTimer = solenoidTimer
        self.dotimer = True
        self.armState=ARM_STATE_FLOATING
        self.timerStarted = False
        self.timerTriggered = False
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
            
    def armDown(self):
        ''' the pistons bring the arm down'''
        self.armState = ARM_STATE_DOWN
        
    def armNeutral(self):
        ''' the arm is in default mode/ does nothing just '''
        self.armState = ARM_STATE_FLOATING
        
    def doit(self):
        ''' Makes everything work '''
        if self.armState==ARM_STATE_UP:
            vent_top = True
            vent_down = False
            fill_up = False
            
            if not self.timerStarted:
                self.solenoidTimer.Start()
                self.timerStarted = True
                self.timerTriggered = False
            
            if self.timerTriggered:
                fill_bottom = True
            else:
                fill_bottom = False
                        
        elif self.armState==ARM_STATE_DOWN:
            vent_top = False
            fill_up = True
            fill_bottom = False
            vent_down = True
            self.timerStarted = False
        
        elif self.armState==ARM_STATE_FLOATING:
            vent_top = True  # bouncing
            fill_up = False
            fill_bottom = False
            vent_down = True
            self.timerStarted = False
        
        if self.solenoidTimer.HasPeriodPassed(0.2):
            fill_bottom = True
            self.solenoidTimer.Reset()
            self.solenoidTimer.Stop()
            
            self.timerTriggered = True
            
        if fill_bottom == True:
            self.jaguar.Set(self.jaguarval)
        else:
            self.jaguar.Set(0)
        
        #print("fill bottom", fill_bottom)
        
        self.vent_up_solenoid.Set(vent_top)
        self.fill_up_solenoid.Set(fill_up)
        self.fill_down_solenoid.Set(fill_bottom)
        self.vent_down_solenoid.Set(vent_down)
        self.jaguarval = 0
        
        
        
