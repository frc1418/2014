
try:
    import wpilib
except ImportError:
    from pyfrc import wpilib

import timed_shoot

class HotShootAutonomous(timed_shoot.TimedShootAutonomous):
    '''
        Based on the TimedShootAutonomous mode. Modified to allow
        shooting based on whether the hot goal is enabled or not.
    '''
    
    DEFAULT = False
    MODE_NAME = "Hot Aim shoot old"

    def __init__(self, components):
        super().__init__(components)
        
        wpilib.SmartDashboard.PutNumber('DriveRotateSpeedLeft', -0.5)
        wpilib.SmartDashboard.PutNumber('DriveRotateSpeedRight', 0.55)
        wpilib.SmartDashboard.PutNumber('DriveRotateTime', 0.1)
        wpilib.SmartDashboard.PutBoolean('IsHotLeft', False)
        wpilib.SmartDashboard.PutBoolean('IsHotRight', False)

    def on_enable(self):
        '''these are called when autonomous starts'''
        
        super().on_enable()
        
        self.drive_rotate_speed_left = wpilib.SmartDashboard.GetNumber('DriveRotateSpeedLeft')
        self.drive_rotate_speed_right = wpilib.SmartDashboard.GetNumber('DriveRotateSpeedRight')
        self.drive_rotate_time = wpilib.SmartDashboard.GetNumber('DriveRotateTime')
        
        print("-> Drive rotate spd L:", self.drive_rotate_speed_left)
        print("-> Drive rotate spd R:", self.drive_rotate_speed_right)
        print("-> Drive rotate tm:", self.drive_rotate_time)
        
        self.decided = False
        self.start_time = None
    
    def on_disable(self):
         '''This function is called when autonomous mode is disabled'''
         pass

    def update(self, time_elapsed):   
        '''The actual autonomous program'''     
       
       
        # decide if it's hot or not
        if not self.decided:
            self.hotLeft = wpilib.SmartDashboard.GetBoolean("IsHotLeft")
            self.hotRight = wpilib.SmartDashboard.GetBoolean("IsHotRight")
            
            if (self.hotLeft or self.hotRight) and not (self.hotLeft and self.hotRight):
                self.decided = True
                
                if self.hotLeft:
                    self.drive_rotate_speed = self.drive_rotate_speed_left
                else:
                    self.drive_rotate_speed = self.drive_rotate_speed_right
                
            elif time_elapsed > 6:
                # at 6 seconds, give up and shoot anyways
                self.decided = True
                
                # default to the left
                self.drive_rotate_speed = self.drive_rotate_speed_left
       
       
        # always keep the arm down
        self.intake.armDown()
        
        # wait a split second for the arm to come down, then
        # keep bringing the catapult down so we're ready to go
        if time_elapsed > 0.3:
            self.catapult.pulldown()
        
                
        # wait some period before we start driving
        if time_elapsed < self.drive_wait:
            pass
        
        else:
                         
            if self.decided:
                
                # only set this once, so we can calculate time from this
                # point on 
                if self.start_time is None:
                    self.start_time = time_elapsed
                
                
                time_elapsed = time_elapsed - self.start_time
                
                if time_elapsed < self.drive_rotate_time:
                    # rotate
                    self.drive.move(0, 0, self.drive_rotate_speed)
                
                elif time_elapsed < self.drive_rotate_time + self.drive_time:
                    # Drive slowly forward for N seconds
                    self.drive.move(0, self.drive_speed, 0)
                    
                    
                elif time_elapsed < self.drive_rotate_time + self.drive_time + 1.0:
                    # Finally, fire and keep firing for 1 seconds
                    self.catapult.launchNoSensor()
