
try:
    import wpilib
except ImportError:
    from pyfrc import wpilib
    
# import components here
<<<<<<< Updated upstream
'''
try:
    from src import components
except ImportError:
    from src import components'''
#from components import drive, intake, catapult
=======
#from components import drive, intake, catapult


>>>>>>> Stashed changes

class MyRobot(wpilib.SimpleRobot):
    DEFAULT = True
    def __init__ (self, components):
        super().__init__()
        self.drive = components['drive']
        self.robot = robot['robot']
        self.intake = components['intake']
        print("Team 1418 autonomous code for 2014")
        
        #################################################################
        # THIS CODE IS SHARED BETWEEN THE MAIN ROBOT AND THE ELECTRICAL #
        # TEST CODE. WHEN CHANGING IT, CHANGE BOTH PLACES!              #
        #################################################################
        
        wpilib.SmartDashboard.init()
        self.update(time_elapsed)
        

    def on_enable(self):
        time = wpilib.Timer()
        timer.Start()
        update (self, timer)
    def on_disable(self):
         '''This function is called when autonomous mode is disabled'''
         pass

    def update(self, time_elapsed):
        '''self.Compressor.Start()
         self.intake.armDown()
         self.catapult.pulldown()
         self.robot.winch_motor.Set(0)
         self.drive.move(self,0,-1,0)
         if self.robot.ultrasonic_sensor!=2:
         self.catapult.launch()
         self.catapult.pulldown()
         self.robot.winch_motor.Set(0)
         if self.robot.ball_sensor!=.4:
             self.intake.wheels()
             self.intake.armNeutral()
             self.drive.move(self,0,1,0)
         elif self.robot.ball_sensor==.4:
             self.drive.move(self,0,-1,0)
             self.catapult.launch()    '''
             
             
        state = 1    
        self.Compressor.Start()
        if state==1:
            self.intake.armDown()
            self.catapult.pulldown()
            self.robot.winch_motor.Set(0)
            self.drive.move(self,0,-1,0)
            if self.robot.ultrasonic_sensor==2:
                 state = 2
            else:
             pass 
        else:
             pass 
        if state==2:
            self.catapult.launch()
            self.catapult.pulldown()
            self.robot.winch_motor.Set(0)
            self.intake.wheels()
            self.intake.armNeutral()
            self.drive.move(self,0,1,0)
            if self.robot.ball_sensor==.4:
               state = 3
            else:
                pass
        else:
                pass 
        if state == 3:
            self.drive.move(self,0,-1,0)
            if self.robot.ultrasonic_sensor==.4:
                self.catapult.launch()  
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
         
            