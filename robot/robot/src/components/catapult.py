
try:
    import wpilib
except ImportError:
    from pyfrc import wpilib
class Catapult (object):
    #This is matt's catapult code. don't make fun of it.
    def __init__ (self, winch, activatesolenoid,passSolenoid, potentiometer, analog_channel, timer):
        #im assuming that the potentiometer max is 1 and the potentiometer min is 0 --- Matt, the potentiometer is whatever we set it to, so you should talk to Shayne about how to do that
        self.opticalsensor = analog_channel
        self.shootTimer=wpilib.Timer()
        self.pushTimer=wpilib.Timer()
        self.passSolenoid=passSolenoid
        
        self.potentiometer = potentiometer 
        self.winch=winch
        self.activatesolenoid=activatesolenoid
        self.timer = timer
        
        self.tempwinch=0
        self.tempsolenoid1=False
        self.tempsolenoid2=False
        self.ballready = False
        self.passSolenoidval=False
        #i am assuming launchangle will be defined by the smart-dashboard-ish thing dusitin wants to make, for now it is 0
        self.launchangle=0
        
        self.launcherup=True
        
    def pulldown(self, Potentiometer):

        self.launcherup=True
        if Potentiometer > 0:
            self.tempwinch=1
        elif self.winch.GetForwardLimitOK():
            self.tempwinch=0
            self.launcherup=False
    def pulldownNoSensor(self):
        

        self.launcherup=True
        self.tempwinch=1
        if self.winch.GetForwardLimitOK():
            self.tempwinch=0
            self.launcherup=False
    def launch(self):
        print("testing")
        if  self.ballready == True:
            print("Lauching")
            self.tempsolenoid2=False
            self.tempsolenoid1=True
            self.launcherup=True
            #self.timer.Reset()
            self.timer.Start()
        else:
            self.tempsolenoid1=False
    def launchNoSensor(self):              #no sensors
            self.tempsolenoid2=False
            self.tempsolenoid1=True
            #self.timer.Reset()
            self.timer.Start()
    def passBall(self):
        self.passSolenoidval=True
    def check_ready(self):
        if self.opticalsensor.GetVoltage() <.6 and self.opticalsensor.GetVoltage() >.4:
            self.ballready = True
        else:
            self.ballready = False
            
    def check_up(self):
        return self.launcherup
    def doit(self):
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



