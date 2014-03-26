
try:
    import wpilib
except ImportError:
    from pyfrc import wpilib
    
# catapult states
NOTHING = 0
WINCH = 1
LAUNCH = 2
LAUNCHSENSOR =3
LAUNCH_TIMER = 4

class Catapult (object):
    ''' runs the robot catapult components'''
    
    def __init__ (self, winch, activateSolenoid,passSolenoid, potentiometer, analog_channel, timer):
        '''initialize'''

        self.ballSensor = analog_channel
        self.passSolenoid = passSolenoid
        
        self.arrayOfMotorValues = [0]*119
        self.sendArray=False
        
        self.potentiometer = potentiometer 
        self.winch = winch
        self.activateSolenoid = activateSolenoid
        self.timer = timer
        self.i = 0
        #wpilib.SmartDashboard.PutValue('CatapultValues', self.arrayOfMotorValues)
        
        # timer is always running, but we reset it before using it so we're
        # guaranteed that the time is zero when we use it
        self.launchTimer = wpilib.Timer()
        self.launchTimer.Start()

        self.cState = NOTHING        
        self.do_autowinch = False
        
        # 100 is max, 0 is min
        self.winchLocation = 100


    def autoWinch(self):
        '''Enables autowinch mode'''
        self.do_autowinch = True
        
    def setWinchLocation(self, power):
        self.winchLocation = max(0, min(100, power))

    def pulldown(self):
        '''lowers the winch'''
        
        self._set_cState(WINCH)
        
    def pulldownNoSensor(self):
        '''lowers the winch, but without getting a reading from pot'''
        self._set_cState(WINCH)
        
    def launch(self):
        '''releases the dog'''
        if self.check_ready():
            self._set_cState(LAUNCHSENSOR)
        
    def launchNoSensor(self):  
        '''releases the dog without getting a reading from ballSensor'''            #no sensors
        self._set_cState(LAUNCH)
    
    def check_ready(self):
        '''returns true if there is a ball, false if there isn't'''
        if self.ballSensor.GetVoltage() >.4:
            return True
        else:
            return False
        
    def _set_cState(self, state):
        if self.cState != LAUNCH_TIMER:
            self.cState = state
    
    def getCatapultLocation(self):
        '''
            Returns a value between 0-100 to indicate location of catapult.
            0 is at the top, 100 is at the bottom
        '''
        xMin = 2.5 
        xMax = 4.1
        outMin = 0
        outMax = 100
        potentiom = self.potentiometer.GetAverageVoltage()
        value = ((potentiom-xMin)*(outMax-outMin)/(xMax-xMin)+outMin)
        return max(outMin, min(outMax, value))

    def doit(self):
        '''actually does things'''
        
        def _dog_in():
            self.activateSolenoid.Set(wpilib.DoubleSolenoid.kReverse)
        
        def _dog_out():
            self.activateSolenoid.Set(wpilib.DoubleSolenoid.kForward)
        
        winch = False
        
        if self.do_autowinch:
            winch = True

        #
        # Catapult launch state machine
        #

        if self.cState==WINCH:
            _dog_in()     
            winch = True
            
            
        elif self.cState==LAUNCH:
            _dog_out()
            winch = False
            
            # call reset to put the timer back to zero
            self.launchTimer.Reset()
            
            self.cState = LAUNCH_TIMER

        elif self.cState==LAUNCHSENSOR:
            if self.check_ready():
                _dog_out()
            else:
                _dog_in()
                
            winch = False

            # call reset to put the timer back to zero
            self.launchTimer.Reset()
            
            self.cState = LAUNCH_TIMER
            
        elif self.cState==LAUNCH_TIMER:
            
            _dog_out()
            winch = False
            
            if self.launchTimer.HasPeriodPassed(1.25):
                self.cState = NOTHING
 
        elif self.cState==NOTHING:
            
            _dog_in()
            
        else: 
            raise RuntimeError("This shouldn't happen")
        
        # allows us to bring the catapult down only part of the way
        if self.winchLocation != 100 and self.winchLocation < self.getCatapultLocation():
            winch = False
        
        # use winchPower to determine how far to bring the winch down
        # -> 100 is a special value, it means 'always run'
        # -> not super accurate, but good enough
        
        if winch:
            self.winch.Set(1)
        else:
            self.winch.Set(0)



        if winch and self.winch.GetForwardLimitOK():
            self.sendArray = True        
            if self.i < len(self.arrayOfMotorValues):    
                self.arrayOfMotorValues[self.i]= (self.winch.GetOutputVoltage()*self.winch.GetOutputCurrent())
                self.i=self.i+1
        else:
            if self.sendArray:
                newArray = wpilib.NumberArray()
                print(self.arrayOfMotorValues)
                self.sendArray = False
                for a in self.arrayOfMotorValues:
                    newArray.add(a)
                wpilib.SmartDashboard.PutValue('Catapult Values', newArray)
                self.i = 0
                self.arrayOfMotorValues = [0]*119
                
            

        # reset things
        self.do_autowinch = False
        self._set_cState(NOTHING)


