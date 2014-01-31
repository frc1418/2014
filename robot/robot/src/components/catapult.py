class Catapult (object):
    #This is matt's catapult code. don't make fun of it.
    def __init__ (self, winch, solenoid):
        #im assuming that the potentiometer max is 1 and the potentiometer min is 0 --- Matt, the potentiometer is whatever we set it to, so you should talk to Shayne about how to do that
        angle=potentiometer.Get()
        self.winch=winch
        self.solenoid=solenoid
        tempwinch=0
        tempssolenoid=False
        #i am assuming launchangle will be defined by the smart-dashboard-ish thing dusitin wants to make, for now it is 1
        launchangle=0
    
    def pulldown(self):
        if Potentiometer.Get() <= 0 :
            tempwinch=1
        if self.winch.GetForwardLimitOK():
            tempwinch=0
        
    def launch(self):
        if Potentiometer.Get() <= launchangle:
            tempsolenoid=True
        elif Potentiometer.Get() >= launchangle:
            tempsolenoid=False
    def doit(self):
        #could be any port?
        self.winch.Set(tempwinch)
        self.solenoid.Set(tempsolenoid)
        self.winch=0
        self.solenoid=false
