
try:
    import wpilib
except ImportError:
    from pyfrc import wpilib
    
import timed_shoot
import hot_aim_shoot

class TwoBallHot(hot_aim_shoot.HotShootAutonomous):
    ''' sample autonomous program'''
    
    DEFAULT = False
    MODE_NAME = "Extreme Epicness"
    
    def __init__(self, components):
        '''Assume that any components needed will be passed in as a parameter. Store them so you can use them'''
        super().__init__(components)
        wpilib.SmartDashboard.PutNumber("SecondBallDriveTime", 1.5 )
        wpilib.SmartDashboard.PutNumber("SecondBallShoot", 1.5)
        wpilib.SmartDashboard.PutNumber("GetSecondBallTime", 0.7)
        
        wpilib.SmartDashboard.PutNumber('DriveRotateTime2', 0.1)
        wpilib.SmartDashboard.PutNumber('DriveRotateTime3', 0.1)

    def on_enable(self):
        '''This function is called when autonomous mode is enabled'''
        super().on_enable()
        self.drive_time_getSecondBall = wpilib.SmartDashboard.GetNumber("SecondBallDriveTime")
        self.drive_time_reverse = wpilib.SmartDashboard.GetNumber("GetSecondBallTime")
        self.drive_time_shoot2 = wpilib.SmartDashboard.GetNumber("SecondBallShoot")
        self.drive_rotate_time2 = wpilib.SmartDashboard.GetNumber('DriveRotateTime2')
        self.drive_rotate_time3 = wpilib.SmartDashboard.GetNumber('DriveRotateTime3')
        
        self.launch1 = False
        
        print("-> Second ball", self.drive_time_getSecondBall)
        print("-> Drive time shoot2", self.drive_time_shoot2)
        print("-> Drive time reverse", self.drive_time_reverse)
        print("-> Rotate 2", self.drive_rotate_time2)
        print("-> Rotate 3", self.drive_rotate_time3)
        
        
        

    def on_disable(self):
        '''This function is called when autonomous mode is disabled'''
        pass 

    def update(self, time_elapsed):
        # decides if hot goal is left or right
        if not self.decided:
            self.hotLeft = wpilib.SmartDashboard.GetBoolean("IsHotLeft")
            self.hotRight = wpilib.SmartDashboard.GetBoolean("IsHotRight")
            
            if (self.hotLeft or self.hotRight) and not (self.hotLeft and self.hotRight):
                self.decided = True
                
                if self.hotLeft:
                    self.drive_rotate_speed = self.drive_rotate_speed_left
                    #print ("hot Left")
                else:
                    self.drive_rotate_speed = self.drive_rotate_speed_right
                    #print ('hot right')
            else:
                self.drive_rotate_speed = self.drive_rotate_speed_left
        
        
        # always keep the arm down
        
        # wait a split second for the arm to come down, then
        # keep bringing the catapult down so we're ready to go
        if time_elapsed > 0.3:
            self.catapult.pulldown()
            
       
        # wait some period before we start driving
        if time_elapsed < self.drive_wait:
            self.intake.armDown()
            
        elif time_elapsed < self.drive_wait + self.drive_rotate_time:
            self.drive.move(0,0,self.drive_rotate_speed)

        elif time_elapsed <self.drive_wait + self.drive_rotate_time + self.drive_time:
            # Start the launch sequence! Drive slowly forward for N seconds
            self.drive.move(0, self.drive_speed, 0)
            
            
        elif time_elapsed < self.drive_wait + self.drive_rotate_time + self.drive_time + 1.0:
            # Finally, fire and keep firing for 1 seconds
            
            if not self.launch1:
                self.catapult.launchNoSensor()
                self.launch1 = True
            
            
        elif time_elapsed < self.drive_wait + self.drive_rotate_time + self.drive_time + 1.0 + self.drive_time_getSecondBall:
            
            # back
            self.drive.move(0, -1*self.drive_speed, 0)
            self.intake.ballIn()
            
        
        elif time_elapsed <self.drive_wait + self.drive_rotate_time + self.drive_time + 1.0 + self.drive_time_getSecondBall + \
                           self.drive_rotate_time2:
            
            # rotate
            self.drive.move(0,0,-1*self.drive_rotate_speed)
            self.intake.ballIn()
            
            
        elif time_elapsed < self.drive_wait + self.drive_rotate_time + self.drive_time + 1.0 + self.drive_time_getSecondBall + \
                            self.drive_rotate_time2 + self.drive_time_reverse:
            
            # back a short bit            
            self.decided = False
            self.drive.move(0,-1*self.drive_speed, 0)
            self.intake.ballIn()
            
        elif time_elapsed <self.drive_wait + self.drive_rotate_time + self.drive_time + 1.0 + self.drive_time_getSecondBall + \
                           self.drive_rotate_time2 + self.drive_time_reverse + self.drive_time_reverse:
            
            self.drive.move(0, self.drive_speed, 0)
            self.intake.ballIn()
            
        
        elif time_elapsed < self.drive_wait + self.drive_rotate_time + self.drive_time + 1.0 + self.drive_time_getSecondBall + \
                            self.drive_rotate_time2 + self.drive_time_reverse + self.drive_time_reverse + self.drive_rotate_time3:
            
            # rotate more
            self.drive.move(0,0,self.drive_rotate_speed)
            self.intake.ballIn()
            
        elif time_elapsed <self.drive_wait + self.drive_rotate_time + self.drive_time + 1.0 + self.drive_time_getSecondBall + \
                           self.drive_rotate_time2 + self.drive_time_reverse + self.drive_time_reverse +  self.drive_rotate_time3 + self.drive_time_shoot2:
            
            self.drive.move(0, self.drive_speed, 0)
            self.intake.ballIn()
            
        elif time_elapsed < self.drive_wait + self.drive_rotate_time + self.drive_time + 1.0 + self.drive_time_getSecondBall + \
                           self.drive_rotate_time2 + self.drive_time_reverse + self.drive_time_reverse +  self.drive_rotate_time3 + self.drive_time_shoot2 + 1.0:
            
            # Finally, fire and keep firing for 1 seconds
            self.catapult.launchNoSensor()
            
            
            
      