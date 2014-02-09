
try:
    import wpilib
except ImportError:
    from pyfrc import wpilib
    
# import components here

'''
try:
    from src import components
except ImportError:
    from src import components'''
#from components import drive, intake, catapult

#from components import drive, intake, catapult




class MyRobot(wpilib.SimpleRobot):
    DEFAULT = True
    MODE_NAME = "Tim's Mode"
    def __init__ (self, components):
        super().__init__()
        self.drive = components['drive']
        #self.robot = src['robot']
        self.intake = components['intake']
        self.catapult = components['catapult']
        print("Team 1418 autonomous code for 2014")
        self.state = 1
        
        #################################################################
        # THIS CODE IS SHARED BETWEEN THE MAIN ROBOT AND THE ELECTRICAL #
        # TEST CODE. WHEN CHANGING IT, CHANGE BOTH PLACES!              #
        #################################################################
        
        wpilib.SmartDashboard.init()
        #self.update()
        

    def on_enable(self):
        timer = wpilib.Timer()
        timer.Start()
        
        pass
    def on_disable(self):
         '''This function is called when autonomous mode is disabled'''
         pass

    def update(self, time_elapsed):

        '''self.Compressor.Start()
         self.intake.armDown()
         self.catapult.pulldown()
         self.catapult.winch_motor.Set(0)
         self.drive.move(self,0,-1,0)
         if self.robot.ultrasonic_sensor!=2:
         self.catapult.launch()
         self.catapult.pulldown()
         self.catapu.winch_motor.Set(0)
         if self.robot.ball_sensor!=.4:
             self.intake.wheels()
             self.intake.armNeutral()
             self.drive.move(self,0,1,0)
         elif self.robot.ball_sensor==.4:
             self.drive.move(self,0,-1,0)
             self.catapult.launch()    '''
             
             
            
        if self.state==1:
            self.intake.armDown()
            print ('a')
            self.catapult.pulldownNoSensor()
            print ('b')
            #self.catapult.winch_motor.Set(0)
            if self.drive.ultraSensor()<=.9 and self.drive.ultraSensor()>=.6: 
                self.drive.move(0,0,0)
                self.state = 2
                print ('d')
            else:
                self.drive.move(0,1,0)
                print ('c')
              
        else:
             pass 
        if self.state==2:
            self.catapult.check_ready()
            print ('e')
            self.catapult.launch()
            print ('f')
            self.catapult.pulldownNoSensor()
            print ('g')
            #self.catapult.winch_motor.Set(0)
            self.intake.ballIn()
            print ('h')
            self.intake.armNeutral()
            print ('i')
            self.drive.move(0,1,0)
            print ('j')
            self.catapult.check_ready()
            print ('k')
            if self.catapult.ballready:
               self.state = 3
               print ('l')
            else:
                pass
        else:
                pass 
        if self.state == 3:
            self.drive.move(0,-1,0)
            print ('m')
            if self.drive.ultraSensor()<=.9 and self.drive.ultraSensor()>=.6:
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
         
            