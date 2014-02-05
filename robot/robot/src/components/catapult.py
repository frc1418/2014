class Catapult (object):
    #This is matt's catapult code. don't make fun of it.
    def __init__ (self, winch, activatesolenoid, potentiometer, analog_channel, timer):
        #im assuming that the potentiometer max is 1 and the potentiometer min is 0 --- Matt, the potentiometer is whatever we set it to, so you should talk to Shayne about how to do that
        self.opticalsensor = analog_channel

        self.potentiometer = potentiometer 
        self.winch=winch
        self.activatesolenoid=activatesolenoid
        self.timer = timer
        
        self.tempwinch=0
        self.tempsolenoid1=False
        self.tempsolenoid2=False
        self.ballready = False
        self.solenoidlock = False
        #i am assuming launchangle will be defined by the smart-dashboard-ish thing dusitin wants to make, for now it is 0
        self.launchangle=0
        
        self.launcherup=True
        
    def pulldown(self, Potentiometer):
        if self.timer.HasPeriodPassed(1) == True:
            print("timer active")
            self.solenoidlock = False 
            #self.timer.Reset()
            #self.timer.Stop()

        self.launcherup=True
        if Potentiometer > 0 and self.solenoidlock is False:
            self.tempwinch=1
        elif self.winch.GetForwardLimitOK():
            self.tempwinch=0
            self.launcherup=False
            #Matt, this section doesn't make sense. -S & L
    def prepare(self):
        if self.launcherup == False and self.solenoidlock == False and self.ballready==True:
            self.tempsolenoid2=True
            self.launcherup=False
            self.solenoidlock=True

    def launch(self):
        if self.solenoidlock == False and self.ballready == True:
            '''remember to take off the pound on ballready'''
            self.tempsolenoid2=False
            self.tempsolenoid1=True
            self.launcherup=True
            self.solenoidlock = True
            #self.timer.Reset()
            self.timer.Start()
            print("Has Launched")
        else:
            self.tempsolenoid1=False
    
    def check_ready(self, analog_channel):
        if analog_channel >= 1:
            self.ballready = True
        else:
            self.ballready = False
            
    def check_up(self):
        return self.launcherup
    def doit(self):
        #could be any port?
        print(self.tempsolenoid1,self.tempsolenoid2)
        self.winch.Set(self.tempwinch)
        self.activatesolenoid.Set(self.tempsolenoid1,self.tempsolenoid2)
 



