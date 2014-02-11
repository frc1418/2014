
try:
    import wpilib
except ImportError:
    from pyfrc import wpilib
    
NOTHING = 0
WINCH = 1
LAUNCH = 2
LAUNCHSENSOR =3
LAUNCH_TIMER = 4

class Catapult (object):
    ''' runs the robot catapult components'''
    #This is matt's catapult code. don't make fun of it.
    def __init__ (self, winch, activateSolenoid,passSolenoid, potentiometer, analog_channel, timer, joystick):
        '''initialize'''
        #im assuming that the potentiometer max is 1 and the potentiometer min is 0 --- Matt, the potentiometer is whatever we set it to, so you should talk to Shayne about how to do that
        self.Ballsensor = analog_channel
        self.passSolenoid=passSolenoid
        self.joystick1 = joystick
        
        self.potentiometer = potentiometer 
        self.winch=winch
        self.activateSolenoid=activateSolenoid
        self.timer = timer
        self.launchTimer = wpilib.Timer()

        
        self.tempwinch=0
        self.tempsolenoid1=False
        self.tempsolenoid2=False
        self.ballready = False
        self.passSolenoidval=False
        self.time = False
        self.cState= NOTHING
        #i am assuming launchangle will be defined by the smart-dashboard-ish thing dusitin wants to make, for now it is 0
        self.launchangle=0
        
        self.launcherup=True
        
        self.do_autowinch = False

    def autoWinch(self):
        '''Enables autowinch mode'''
        self.do_autowinch = True

    def pulldown(self):
        '''lowers the winch'''
        
        self._set_cState(WINCH)
        
    def pulldownNoSensor(self):
        '''lowers the winch, but without getting a reading from pot'''
        self._set_cState(WINCH)
        
    def launch(self):
        '''releases the dog'''
        self._set_cState(LAUNCHSENSOR)
        
    def launchNoSensor(self):  
        '''releases the dog without getting a reading from ballSensor'''            #no sensors
        self._set_cState(LAUNCH)
    
    def check_ready(self):
        '''returns true if there is a ball, false if there isn't'''
        if self.Ballsensor.GetVoltage() <.6 and self.Ballsensor.GetVoltage() >.4:
            return True
        else:
            return False
        
    def _set_cState(self, state):
        if self.cState != LAUNCH_TIMER:
            self.cState = state
        

    def doit(self):
        '''actually does things'''
        #could be any port?
        #print(self.tempsolenoid1,self.tempsolenoid2)
        
        def _dog_in():
            self.activateSolenoid.Set(wpilib.DoubleSolenoid.kReverse)
        
        def _dog_out():
            self.activateSolenoid.Set(wpilib.DoubleSolenoid.kForward)
        
        winch = False
        
        if self.do_autowinch:
            winch = True


        if self.cState==WINCH:
            _dog_in()     
            winch = True
                
        elif self.cState==LAUNCH:
            _dog_out()
            winch = False
            
            self.launchTimer.Start()
            
            self.cState = LAUNCH_TIMER
                
        
        elif self.cState==LAUNCHSENSOR:
            if self.check_ready():
                _dog_out()
            else:
                _dog_in()
                
            winch = False

            self.launchTimer.Start()
            
        elif self.cState==LAUNCH_TIMER:
            
            _dog_out()
            winch = False
            
            if self.launchTimer.HasPeriodPassed(2.5):
                self.cState = NOTHING
                self.launchTimer.Stop()
 
        elif self.cState==NOTHING:
            
            _dog_in()
            
        else: 
            raise RuntimeError("This shouldn't happen")
        
        
        if winch:
            self.winch.Set(1)
        else:
            self.winch.Set(0)

        # reset things
        self.do_autowinch = False
        self._set_cState(NOTHING)


