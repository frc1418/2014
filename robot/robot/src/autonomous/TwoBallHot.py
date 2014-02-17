
try:
    import wpilib
except ImportError:
    from pyfrc import wpilib
    
import timed_shoot
import hot_aim_shoot

class TwoBallHot(hot_aim_shoot.HotShootAutonomous):
    ''' sample autonomous program'''
    
    DEFAULT = False
    MODE_NAME = "Two-Ball-Hot Autonomous"
    
    def __init__(self, components):
        '''Assume that any components needed will be passed in as a parameter. Store them so you can use them'''
        super().__init__(components)
        

    def on_enable(self):
        '''This function is called when autonomous mode is enabled'''
        super().on_enable()
        self.drive_wait = wpilib.SmartDashboard.GetNumber('DriveWaitTime')
        self.drive_time = wpilib.SmartDashboard.GetNumber('AutoDriveTime')
        self.drive_speed = wpilib.SmartDashboard.GetNumber('AutoDriveSpeed')
        

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
                else:
                    self.drive_rotate_speed = self.drive_rotate_speed_right
        
        
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
            
            
        elif time_elapsed < self.drive_wait + self.drive_rotate_time + self.drive_time + 1.0 + self.drive_time:# + 1.5:
            self.drive.move(0, -1*self.drive_speed, 0)
            self.intake.ballIn()
            print('reversing')
        
        elif time_elapsed <self.drive_wait + self.drive_rotate_time + self.drive_time + 1.0 + self.drive_time + self.drive_rotate_time:
            self.drive.move(0,0,-1*self.drive_rotate_speed)
            self.decided = False
            print ('reverse rotating')
            
        elif time_elapsed < self.drive_wait + self.drive_rotate_time + self.drive_time + 1.0 + self.drive_time + self.drive_rotate_time + 1.5:
            self.drive.move(0,-1*self.drive_speed, 0)
            print('going for second ball')
            
        
        elif time_elapsed < self.drive_wait + self.drive_rotate_time + self.drive_time + 1.0 + self.drive_time + \
                           self.drive_rotate_time + 1.5 + self.drive_rotate_time:
            self.drive.move(0,0,self.drive_rotate_speed)    
            print("rotating 2") 
            
            
        elif time_elapsed <self.drive_wait + self.drive_rotate_time + self.drive_time + 1.0 + self.drive_time + \
                           self.drive_rotate_time + 1.5 + self.drive_rotate_time + self.drive_time:
            
            self.drive.move(0, self.drive_speed, 0)
            self.intake.ballIn()
            print("driving 2")
            
        elif time_elapsed < self.drive_wait + self.drive_rotate_time + self.drive_time + 1.0 + self.drive_time + \
                           self.drive_rotate_time + 1.5 + self.drive_rotate_time + self.drive_time + 1.0:
            
            # Finally, fire and keep firing for 1 seconds
            self.catapult.launchNoSensor()
            self.intake.ballIn()
            print('Launching')
            
            
            
            
      