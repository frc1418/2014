'''
Created on Jan 25, 2014

@author: Owner
'''

ARM_STATE_UP = 3
ARM_STATE_DOWN = 1
ARM_STATE_FLOATING = 2
ARM_STATE_NONE = 0


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
        self.armState = ARM_STATE_NONE
        self.timerStarted = False
        self.timerTriggered = False
        
    def ballIn(self):
        '''spins the wheels to suck the ball in '''
        # 0 for stop, 1 for forward, -1 for backwards
        self.jaguarval = -1
        
    # arm controls the arm on the robot; trigger makes arm fall
    def ballOut(self):
        ''' spins the wheels to spit the ball out      '''       
        self.jaguarval = 1
        
    def GetMode(self):
        '''Return the arm mode'''
        return self.armState
      
    def SetMode(self, mode):
        '''Set the arm mode'''

        if mode==ARM_STATE_DOWN:
            self.armDown()
        #elif mode==ARM_STATE_FLOATING:
        #    self.armNeutral()
        elif mode==ARM_STATE_UP:
            self.armUp()
        
    def armUp(self):
        ''' the pistons raise up the arm '''
        self.armState = ARM_STATE_UP
            
    def armDown(self):
        ''' the pistons bring the arm down'''
        self.armState = ARM_STATE_DOWN
        
    def doit(self):
        ''' Makes everything work ''' 
        
        # default it all off
        vent_up = False
        vent_down = False
        fill_up = False
        fill_down = False
        
        
        if self.armState==ARM_STATE_UP:
            vent_up = True
            
            if not self.timerStarted:
                self.solenoidTimer.Start()
                self.timerStarted = True
                self.timerTriggered = False
            
            if self.timerTriggered:
                fill_down = True
                        
        elif self.armState==ARM_STATE_DOWN:
            fill_up = True
            vent_down = True
            
            self.timerStarted = False
            self.armState = ARM_STATE_FLOATING
        
        elif self.armState==ARM_STATE_FLOATING:
            vent_up = True 
            vent_down = True
            
            self.timerStarted = False
        
        if self.solenoidTimer.HasPeriodPassed(0.2):
            fill_down = True
            self.solenoidTimer.Reset()
            self.solenoidTimer.Stop()
            
            self.timerTriggered = True
            self.armState = ARM_STATE_NONE
            
        self.jaguar.Set(self.jaguarval)
        
        self.vent_up_solenoid.Set(vent_up)
        self.fill_up_solenoid.Set(fill_up)
        self.fill_down_solenoid.Set(fill_down)
        self.vent_down_solenoid.Set(vent_down)
        self.jaguarval = 0
        
        
        
