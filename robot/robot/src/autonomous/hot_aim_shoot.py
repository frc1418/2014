try:
    import wpilib
except ImportError:
    from pyfrc import wpilib
from common.autonomous_helper import StatefulAutonomous, timed_state

class hot_aim_shoot(StatefulAutonomous):
    
    MODE_NAME = 'Hot Aim shoot'
    DEFAULT = False
    
    def __init__(self, components):
        super().__init__(components)
        
        self.register_sd_var('drive_speed', 0.5)
        self.register_sd_var('DriveRotateSpeedLeft',-0.5)
        self.register_sd_var('DriveRotateSpeedRight', 0.55)
        self.register_sd_var('DriveRotateTime', 0.1)
        self.register_sd_var('IsHotLeft', False, add_prefix=False)
        self.register_sd_var('IsHotRight', False, add_prefix=False)
    
    def on_enable(self):
        super().on_enable()
        self.decided = False
    
    def update(self, tm):
        
        self.intake.armDown()
        if tm > 0.3:
            self.catapult.pulldown()
            
        if not self.decided:
            self.IsHotLeft = wpilib.SmartDashboard.GetBoolean("IsHotLeft")
            self.IsHotRight = wpilib.SmartDashboard.GetBoolean("IsHotRight")
        
            if (self.IsHotLeft or self.IsHotRight) and not (self.IsHotLeft and self.IsHotRight):
                self.decided = True
            
                if self.IsHotLeft:
                    self.drive_rotate_speed = self.DriveRotateSpeedLeft
                else:
                    self.drive_rotate_speed = self.DriveRotateSpeedRight
                
            elif tm > 6:
                self.decided=True
                self.drive_rotate_speed = self.DriveRotateSpeedLeft
         
        super().update(tm)
        
        
    @timed_state(duration=1.2, next_state='wait_for_decision', first=True)
    def drive_wait(self):
        '''wait some period before we start driving'''
        pass
    
    @timed_state(duration=100)   
    def wait_for_decision(self):
        '''Only begin shooting once a decision has been made
           TODO: is there a better way to express this state?'''
        if self.decided:
            self.next_state('rotate')
            self.rotate()
    
    @timed_state(duration=0.07, next_state='drive')
    def rotate(self):
        '''Rotate the robot slightly'''
        self.drive.move(0, 0, self.drive_rotate_speed)
        
    @timed_state(duration=1.4, next_state='fire')
    def drive(self):
        '''Drive slowly forward for N seconds'''
        self.drive.move(0, self.drive_speed, 0)
        
    @timed_state(duration=1)
    def fire(self):
        '''Finally, fire and keep firing for 1 seconds'''
        self.catapult.launchNoSensor()
        
    
