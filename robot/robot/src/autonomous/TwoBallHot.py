
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
        wpilib.SmartDashboard.PutNumber("SecondBallDriveTime", 1.4 )
        wpilib.SmartDashboard.PutNumber("SecondBallShoot", 1.4)
        wpilib.SmartDashboard.PutNumber("GetSecondBallTime", .5)

    def on_enable(self):
        '''This function is called when autonomous mode is enabled'''
        super().on_enable()
        self.drive_wait = wpilib.SmartDashboard.GetNumber('DriveWaitTime')
        self.drive_time = wpilib.SmartDashboard.GetNumber('AutoDriveTime')
        self.drive_speed = wpilib.SmartDashboard.GetNumber('AutoDriveSpeed')
        self.drive_time_getSecondBall = wpilib.SmartDashboard.GetNumber("SecondBallDriveTime")
        self.drive_time_shoot2 = wpilib.SmartDashboard.GetNumber("SecondBallShoot")
        self.drive_time_reverse = wpilib.SmartDashboard.GetNumber("GetSecondBallTime")
        

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
                    print ("hot Left")
                else:
                    self.drive_rotate_speed = self.drive_rotate_speed_right
                    print ('hot right')
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
            print("arm down")
        elif time_elapsed < self.drive_wait + self.drive_rotate_time:
            self.drive.move(0,0,self.drive_rotate_speed)
            print("rotate ")

        elif time_elapsed <self.drive_wait + self.drive_rotate_time + self.drive_time:
            # Start the launch sequence! Drive slowly forward for N seconds
            self.drive.move(0, self.drive_speed, 0)
            self.intake.armDown()
            print("driving")
            
            
        elif time_elapsed < self.drive_wait + self.drive_rotate_time + self.drive_time + 1.0:
            # Finally, fire and keep firing for 1 seconds
            self.catapult.launchNoSensor()
            print ('launching')
            
            
        elif time_elapsed < self.drive_wait + self.drive_rotate_time + self.drive_time + 1.0 + self.drive_time_getSecondBall:# + 1.5:
            self.drive.move(0, -1*self.drive_speed, 0)
            self.intake.ballIn()
            print('reversing')
        
        elif time_elapsed <self.drive_wait + self.drive_rotate_time + self.drive_time + 1.0 + self.drive_time_getSecondBall + self.drive_rotate_time:
            self.drive.move(0,0,-1*self.drive_rotate_speed)
            print ('reverse rotating')
            
        elif time_elapsed < self.drive_wait + self.drive_rotate_time + self.drive_time + 1.0 + self.drive_time_getSecondBall + self.drive_rotate_time + self.drive_time_reverse:            
            self.decided = False
            self.drive.move(0,-1*self.drive_speed, 0)
            print('going for second ball')
            
        
        elif time_elapsed < self.drive_wait + self.drive_rotate_time + self.drive_time + 1.0 + self.drive_time_getSecondBall + \
                           self.drive_rotate_time + self.drive_time_reverse + self.drive_rotate_time:
            self.drive.move(0,0,self.drive_rotate_speed)    
            if self.hotLeft:
                print("rotating 2 left") 
            elif self.hotRight:
                print("rotating 2 right")
            
        elif time_elapsed <self.drive_wait + self.drive_rotate_time + self.drive_time + 1.0 + self.drive_time_getSecondBall + \
                           self.drive_rotate_time + self.drive_time_reverse + self.drive_rotate_time + self.drive_time_shoot2:
            
            self.drive.move(0, self.drive_speed, 0)
            self.intake.ballIn()
            print("driving 2")
            
        elif time_elapsed < self.drive_wait + self.drive_rotate_time + self.drive_time + 1.0 + self.drive_time_getSecondBall + \
                           self.drive_rotate_time + self.drive_time_reverse + self.drive_rotate_time + self.drive_time_shoot2 + 1.0:
            
            # Finally, fire and keep firing for 1 seconds
            self.catapult.launchNoSensor()
            self.intake.ballIn()
            print('Launching')
            
            
            
            
      