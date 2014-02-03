class Catapult (object):
    #This is matt's catapult code. don't make fun of it.
    def __init__ (self, winch, solenoid, potentiometer, analog_channel, timer):
        #im assuming that the potentiometer max is 1 and the potentiometer min is 0 --- Matt, the potentiometer is whatever we set it to, so you should talk to Shayne about how to do that
        self.opticalsensor = analog_channel

        self.potentiometer = potentiometer 
        self.winch=winch
        self.solenoid=solenoid
        self.timer = timer
        
        self.tempwinch=0
        self.tempsolenoid=False
        self.ballready = False
        self.solenoidlock = False
        #i am assuming launchangle will be defined by the smart-dashboard-ish thing dusitin wants to make, for now it is 0
        self.launchangle=0
        
        
    def pulldown(self, Potentiometer):
        if self.timer.hasPeriodPassed(1) == True:
            self.solenoidlock = False 
            self.timer.reset()
            self.timer.stop() 
        if Potentiometer <= 0 :
            self.tempwinch=1
        if self.winch.GetForwardLimitOK():
            self.tempwinch=0
            #Matt, this section doesn't make sense. -S & L 
        
    def launch(self, Potentiometerval):
        if Potentiometerval <= self.launchangle and self.solenoidlock == False and self.ballready == True:
            self.tempsolenoid=True 
            self.solenoidlock = True
            self.timer.reset()
        elif Potentiometerval > self.launchangle:
            self.tempsolenoid=False
    
    def check_ready(self, analog_channel):
        if analog_channel >= 1:
            self.ballready = True
        else:
            self.ballready = False
            
        
    def doit(self):
        #could be any port?
        self.winch.Set(self.tempwinch)
        self.solenoid.Set(self.tempsolenoid)
        self.winch=0
        self.solenoid=false

