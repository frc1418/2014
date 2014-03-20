try:
    import wpilib
except ImportError:
    from pyfrc import wpilib
from common.autonomous_helper import StatefulAutonomous, timed_state

class TwoBall(StatefulAutonomous):
    
    MODE_NAME = 'Two Balls Hot'
    DEFAULT = True
    
    def __init__(self, components):
        super().__init__(components)
        self.drive_speed=1;
        '''#self.register_sd_var('SecondBallDriveTime',1.5);
        self.register_sd_var('SecondBallShoot',1.5);
        #self.register_sd_var('GetSecondBallTime',0.7);
        self.register_sd_var('DriveRotateTime2',0.1);
        self.register_sd_var('DriveRotateTime3',0.1);'''
        self.register_sd_var('hotLeft',False)
        self.register_sd_var("hotRight",False)
        #please change the drive rotate speeds, I'm really 
        #just guessing about the values
        self.register_sd_var('drive_rotate_speed_left',1)
        self.register_sd_var('drive_rotate_speed_right',-1)
        
        wpilib.SmartDashboard.PutBoolean('IsHotLeft', False)
        wpilib.SmartDashboard.PutBoolean('IsHotRight', False)
        self.decided = False
    #def on_enable(self):
        '''This function is called when autonomous mode is enabled'''
        #super().on_enable()
        
        '''#self.drive_time_getSecondBall = wpilib.SmartDashboard.GetNumber("SecondBallDriveTime")
        #self.drive_time_reverse = wpilib.SmartDashboard.GetNumber("GetSecondBallTime")
        #self.drive_time_shoot2 = wpilib.SmartDashboard.GetNumber("SecondBallShoot")
        self.drive_rotate_time2 = wpilib.SmartDashboard.GetNumber('DriveRotateTime2')
        self.drive_rotate_time3 = wpilib.SmartDashboard.GetNumber('DriveRotateTime3')'''
        
    def update(self, tm):
        if tm > 0.3:
            self.catapult.pulldown()
            
        if not self.decided:
            self.hotLeft = wpilib.SmartDashboard.GetBoolean("IsHotLeft")
            self.hotRight = wpilib.SmartDashboard.GetBoolean("IsHotRight")
            
            if (self.hotLeft or self.hotRight) and not (self.hotLeft and self.hotRight):
                self.decided = True
                
                if self.hotLeft:
                    self.RotateLeft()
                    #print ("hot Left")
                else:
                    self.RotateRight()
                    #print ('hot right')
            else:
                self.RotateLeft()
        super().update(tm)
    def RotateRight(self):
        self.drive_rotate_speed = self.drive_rotate_speed_right
        print('hot left')

    def RotateLeft(self):
        self.drive_rotate_speed = self.drive_rotate_speed_left
        print('hot right')

    
    #
    #I have no idea how the timing is supposed to work from states 'nextball1' to 'launch2'.
    #For the moment I'm just going to add one second to each state.    
    #
    #Please contact Timmy and get him to explain the timngs on his old TwoBall class
    @timed_state(duration=.5, next_state='drive_rotate', first=True)
    def drive_wait(self, tm, state_tm):
        self.intake.armDown
        print("drive_wait'", tm)
    
    @timed_state(duration=1,next_state='drive_start')
    def drive_rotate(self, tm, state_tm):
        self.drive.move(0,0,self.drive_rotate_speed)
        print("drive_rotate", tm)
    @timed_state(duration=1,next_state='launch')
    def drive_start(self, tm, state_tm):
         self.drive.move(0, self.drive_speed, 0)
         print("screwleondrive_start", tm)
    @timed_state(duration=1,next_state='next_ball1')
    def launch(self, tm, state_tm):
        self.catapult.launchNoSensor()     
        print("launch", tm)
         
    @timed_state(duration=1, next_state='next_ball1_rotate')        
    def next_ball1(self,tm, state_tm):
            self.drive.move(0, -1*self.drive_speed, 0)
            self.intake.ballIn()    
            print("next_ball1", tm)
    @timed_state(duration=1, next_state='next_ball2')        
    def next_ball1_rotate(self,tm, state_tm):
            self.drive.move(0, 0, -1*self.drive_rotate_speed)
            self.intake.ballIn()  
            print("next_ball1_rotate", tm)
    @timed_state(duration=1, next_state='rotate2')        
    def next_ball2(self,tm, state_tm):
            self.drive.move(0, self.drive_speed, 0)
            self.intake.ballIn()
            print("next_ball2", tm)
    @timed_state(duration=1,next_state='launch2')
    def rotate2(self,tm, state_tm):
        self.drive.move(0,self.drive_speed,0)
        self.intake.ballIn()
        
    @timed_state(duration=1, next_state='finished_shoot')    
    def launch2(self,tm, state_tm):
            # Finally, fire and keep firing for 1 seconds
            self.catapult.launchNoSensor()
    @timed_state(duration=1000)
    def finished_shoot(self,tm,state_tm):
        pass
    