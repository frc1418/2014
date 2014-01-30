    p0class Catapult (object):
    #This is matt's catapult code. don't make fun of it.
    def __init__ (winch, solenoid):
        #im assuming that the potentiometer max is 1 and the potentiometer min is 0 --- Matt, the potentiometer is whatever we set it to, so you should talk to Shayne about how to do that
        angle=potentiometer.Get()
        self.winch=winch
        self.solenoid=solenoid
        #i am assuming launchangle will be defined by the smart-dashboard-ish thing dusitin wants to make, for now it is 1
        launchangle=0
    
    def pulldown(self):
        if Potentiometer.Get() <= 0 :
            self.winch.Set(1)
        if self.winch.GetForwardLimitOK():
            self.winch.Set(0)
        
    def launch(self):
        if Potentiometer.Get() <= launchangle:
            self.solenoid=True
        elif Potentiometer.Get() >= launchangle:
            self.solenoid=False
    def doit(self):
        #could be any port?
        winch.Set(self.winch)
        solenoid.Set(self.solenoid)
        self.winch=0
        self.solenoid=false
