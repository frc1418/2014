
try:
    import wpilib
except ImportError:
    from pyfrc import wpilib
    
NOTHING = 0
WINCH = 1
LAUNCH = 2
LAUNCHSENSOR =3
HOLD = 4

class Catapult (object):
    ''' runs the robot catapult components'''
    #This is matt's catapult code. don't make fun of it.
    def __init__ (self, winch, activateSolenoid,passSolenoid, potentiometer, analog_channel, timer, joystick):
        '''initialize'''
        #im assuming that the potentiometer max is 1 and the potentiometer min is 0 --- Matt, the potentiometer is whatever we set it to, so you should talk to Shayne about how to do that
        self.Ballsensor = analog_channel
        self.shootTimer=wpilib.Timer()
        self.pushTimer=wpilib.Timer()
        self.passSolenoid=passSolenoid
        self.joystick1 = joystick
        
        self.potentiometer = potentiometer 
        self.winch=winch
        self.activateSolenoid=activateSolenoid
        self.timer = timer
        
        self.tempwinch=0
        self.tempsolenoid1=False
        self.tempsolenoid2=False
        self.ballready = False
        self.passSolenoidval=False
        self.cState= NOTHING
        #i am assuming launchangle will be defined by the smart-dashboard-ish thing dusitin wants to make, for now it is 0
        self.launchangle=0
        
        self.launcherup=True

    def stop(self):
        '''stops all activity'''
        self.cState=NOTHING
    
    def pulldown(self):
        '''lowers the winch'''
        
        self.cState=WINCH
    def pulldownNoSensor(self):
        '''lowers the winch, but without getting a reading from pot'''
        self.cState=WINCH
    def launch(self):
        '''releases the dog'''
        self.cState=LAUNCHSENSOR
        
    def launchNoSensor(self):  
        '''releases the dog without getting a reading from ballSensor'''            #no sensors
        self.cState=LAUNCH
    def passBall(self):
        '''pushes the ball out with the center piston'''
        self.cState=HOLD
    def check_ready(self):
        '''returns true if there is a ball, false if there isn't'''
        if self.Ballsensor.GetVoltage() <.6 and self.Ballsensor.GetVoltage() >.4:
            return True
        else:
            return False
            
    def doit(self):
        '''actually does things'''
        #could be any port?
        #print(self.tempsolenoid1,self.tempsolenoid2)
        if self.cState==WINCH:
            self.winch.Set(1)
        elif self.winch.GetForwardLimitOK():
            self.winch.Set(0)
        else:
            pass
        
        if self.cState==LAUNCH:
            self.activateSolenoid.Set(wpilib.DoubleSolenoid.kReverse)
            time = False
            if not time:
                self.shootTimer.Start()
                time=True
            if self.shootTimer.HasPeriodPassed(1):
                self.activateSolenoid.Set(wpilib.DoubleSolenoid.kOff)
                self.shootTimer.Stop()
                self.shootTimer.Reset()
                
        
        elif self.cState==LAUNCHSENSOR:
            if self.check_ready():
                self.activateSolenoid.Set(wpilib.DoubleSolenoid.kReverse)
            else:
                self.activateSolenoid.Set(wpilib.DoubleSolenoid.kOff)
        
        elif self.cState==HOLD:
            self.passSolenoid.Set(True)
        else:
            self.passSolenoid.Set(False)
        
        if self.cState==NOTHING:
            self.activateSolenoid.Set(wpilib.DoubleSolenoid.kOff)
            self.passSolenoid.Set(False)
            self.shootTimer.Stop()
            self.pushTimer.Stop()
            self.winch.Set(0)
        print (self.shootTimer.Get())
        '''self.winch.Set(self.tempwinch)
        if self.pushTimer.HasPeriodPassed(.5):
           self.pushTimer.Stop()
           self.pushTimer.Reset()
           self.passSolenoid.Set(False)
        if self.shootTimer.HasPeriodPassed(1):
            self.tempsolenoid1=False
            self.shootTimer.Reset()
            self.shootTimer.Stop()
        if self.tempsolenoid1 is True:
            self.shootTimer.Start()
            self.activateSolenoid.Set(wpilib.DoubleSolenoid.kForward)
        else:
            self.activateolenoid.Set(wpilib.DoubleSolenoid.kOff)
        if self.passSolenoidval is True:
            self.passSolenoid.Set(True)
            self.pushTimer.Start()
        self.tempwinch=0'''


