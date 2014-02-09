
try:
    import wpilib
except ImportError:
    from pyfrc import wpilib





class main(object):
    DEFAULT = True
    MODE_NAME = "Tim's Mode"
    def __init__ (self, components):
        super().__init__()
        self.drive = components['drive']
        self.intake = components['intake']
        self.catapult = components['catapult']
        
        
        

        
        
        

    def on_enable(self):
        '''these are called when autonomous starts'''
        timer = wpilib.Timer()
        timer.Start()
        self.state = 1
        print("Team 1418 autonomous code for 2014")
    
    def on_disable(self):
         '''This function is called when autonomous mode is disabled'''
         pass

    def update(self, time_elapsed):   
        '''The actual autonomous program'''     
        if self.state==1:
            self.intake.armDown()
            print ('a')
            self.catapult.pulldownNoSensor()
            print ('b')
            self.catapult.cState=NOTHNG
            if self.drive.closePosition(): 
                self.drive.move(0,0,0)
                self.state = 2
                print ('d')
            else:
                self.drive.move(0,1,0)
                print ('c')
              
        else:
             pass 
        if self.state==2:
            self.drive.move(0,0,0)
            print ('123')
            self.catapult.launch()
            print ('f')
            if self.catapult.potentiometer.GetVoltage()>0:
                self.state=3
        if self.state==3:
            self.catapult.pulldownNoSensor()
            print ('g')
            self.catapult.turnOffJag()
            self.intake.ballIn()
            print ('h')
            self.intake.armNeutral()
            print ('i')
            self.drive.move(0,1,0)
            print ('j')
            self.catapult.check_ready()
            print ('k')
            if self.catapult.check_ready():
               self.state = 4
               print ('l')
            else:
                pass
        else:
                pass 
        if self.state == 4:
            self.drive.move(0,-1,0)
            print ('m')
            if self.drive.closePosition():
                self.drive.move(0,0,0)
                self.catapult.launch()  
                print ('n')
            else:
                pass  
        else:
            pass
        
         
         
        '''Do not implement your own loop for autonomous mode. Instead,
            assume that
            this function is called over and over and over again during
            autonomous
            mode if this mode is active

            time_elapsed is a number that tells you how many seconds
            autonomous mode has
            been running so far.
         '''
         
            