
try:
    import wpilib
except ImportError:
    from pyfrc import wpilib
    
NOTHING = 0
WINCH = 1
LAUNCH = 2
HOLD = 4

class Catapult (object):
    #This is matt's catapult code. don't make fun of it.
    def __init__ (self, winch, dogSolenoid,passSolenoid, potentiometer, analog_channel, timer):
        #im assuming that the potentiometer max is 1 and the potentiometer min is 0 --- Matt, the potentiometer is whatever we set it to, so you should talk to Shayne about how to do that
        self.Ballsensor = analog_channel
        self.shootTimer=wpilib.Timer()
        self.pushTimer=wpilib.Timer()
        self.passSolenoid=passSolenoid
        
        self.potentiometer = potentiometer 
        self.winch=winch
        self.dogsolenoid=dogsolenoid
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

    def pulldown(self, Potentiometer):
        '''lowers the winch'''
        
        self.cState = WINCH
        self.launcherup=True
        if Potentiometer > 0:
            self.tempwinch=1
        elif self.winch.GetForwardLimitOK():
            self.tempwinch=0
            self.launcherup=False
        else:
            pass
    def pulldownNoSensor(self):
        '''lowers the winch, but without getting a reading from pot'''
        self.launcherup=True
        self.tempwinch=1
        if self.winch.GetForwardLimitOK():
            self.tempwinch=0
            self.launcherup=False
        else:
            pass
    def launch(self):
        '''releases the dog'''
        print("testing")
        if self.check_ready() == True:
            print("Lauching")
            self.tempsolenoid2=False
            self.tempsolenoid1=True
            self.launcherup=True
            #self.timer.Reset()
            self.timer.Start()
        else:
            self.tempsolenoid1=False
    def launchNoSensor(self):  
        '''releases the dog without getting a reading from ballSensor'''            #no sensors
        self.tempsolenoid2=False
        self.tempsolenoid1=True
        #self.timer.Reset()
        self.timer.Start()
    def passBall(self):
        '''pushes the ball out with the center piston'''
        self.passSolenoidval=True
    def check_ready(self):
        '''returns true if there is a ball, false if there isn't'''
        if self.opticalsensor.GetVoltage() <.6 and self.opticalsensor.GetVoltage() >.4:
            return True
        else:
            return False
            
    def doit(self):
        '''actually does things'''
        #could be any port?
        #print(self.tempsolenoid1,self.tempsolenoid2)
        self.winch.Set(self.tempwinch)
        if self.pushTimer.HasPeriodPassed(.5):
            self.pushTimer.Reset()
            self.pushTimer.Stop()
            self.passSolenoid.Set(False)
        if self.shootTimer.HasPeriodPassed(1):
            self.tempsolenoid1=False
            self.shootTimer.Reset()
            self.shootTimer.Stop()
        if self.tempsolenoid1 is True:
            self.shootTimer.Start()
            self.activatesolenoid.Set(wpilib.DoubleSolenoid.kForward)
        else:
            self.activatesolenoid.Set(wpilib.DoubleSolenoid.kOff)
        if self.passSolenoidval is True:
            self.passSolenoid.Set(True)
            self.pushTimer.Start()
        #self.winch.Set(0)


