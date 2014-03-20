try:
    import wpilib
except ImportError:
    from pyfrc import wpilib
from common.autonomous_helper import StatefulAutonomous, timed_state

class TwoBall(StatefulAutonomous):
    
    MODE_NAME = 'Two balls'
    DEFAULT = False
    
    def __init__(self, components):
        super().__init__(components)
        
        self.register_sd_var('SecondBallDriveTime',1.5);
        self.register_sd_var('SecondBallShoot',1.5);
        self.register_sd_var('GetSecondBallTime',0.7);
        self.register_sd_var('DriveRotateTime2',0.1);
        self.register_sd_var('DriveRotateTime3',0.1);
        self.decided = False
        
    def update(self, tm):
        if tm > 0.3:
            self.catapult.pulldown()
        if not self.decided:
            self.hotLeft = wpilib.SmartDashboard.GetBoolean("IsHotLeft")
            self.hotRight = wpilib.SmartDashboard.GetBoolean("IsHotRight")
            
            if (self.hotLeft or self.hotRight) and not (self.hotLeft and self.hotRight):
                self.decided = True
                
                if self.hotLeft:
                    RotateLeft()
                    #print ("hot Left")
                else:
                    RotateRight()
                    #print ('hot right')
            else:
                RotateLeft()
        super().update(tm)
        
    
    

    def rotateRight(self):
        self.drive_rotate_speed = self.drive_rotate_speed_right
    def RotateLeft(self):
        self.drive_rotate_speed = self.drive_rotate_speed_left\

    
    #
    #I have no idea how the timing is supposed to work from states 'nextball1' to 'launch2'.
    #For the moment I'm just going to add one second to each state.    
    #
    #Please contact Timmy and get him to explain the timngs on his old TwoBall class
    
    @timed_state(time=7.5, next_state='launch2')    
    def launch2(self):
        
            # Finally, fire and keep firing for 1 seconds
            self.catapult.launchNoSensor()
            self.intake.ballIn()
    
    @timed_state(time=6.5, next_state='next_ball2')        
    def next_ball2(self):
                    
            self.drive.move(0, self.drive_speed, 0)
            self.intake.ballIn()
    
    @timed_state(time=5.5, next_state='next_ball1')        
    def next_ball1(self):
            self.drive.move(0, -1*self.drive_speed, 0)
            self.intake.ballIn()
    
    @timed_state(time=1, next_state='drive_wait', first=True)
    def drive_wait(self, tm, state_tm):
        self.intake.armDown
    
    @timed_state(time=2,next_state='drive_start')
    def drive_start(self):
         self.drive.move(0, self.drive_speed, 0)
         self.intake.armDown()
    
    @timed_state(time=4,next_state='try_shoot')
    def try_shoot(self,tm,state_tm):
        launch(tm)
    
    def pre_drive(self, tm):
        pass
    
    @timed_state(time=1.4, next_state='launch')
    def drive(self, tm, state_tm):
        self.drive.move(0, self.drive_speed, 0)
    @timed_state(time=1,next_state='drive')
    def rotate_move(self,tm,state_tm):
        pass
    
    @timed_state(time=7.0)
    def launch(self, tm):
        self.catapult.launchNoSensor()

