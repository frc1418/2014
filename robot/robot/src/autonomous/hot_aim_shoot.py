try:
    import wpilib
except ImportError:
    from pyfrc import wpilib
from common.autonomous_helper import StatefulAutonomous, timed_state

class hot_aim_shoot(StatefulAutonomous):
    
    MODE_NAME = 'hot_aim_shoot'
    DEFAULT = False
    
    def __init__(self, components):
        super().__init__(components)
        
        self.register_sd_var('drive_speed', 0.5)
        self.register_sd_var('DriveRotateSpeedLeft',-0.5)
        self.register_sd_var('DriveRotateSpeedRight', 0.55)
        self.register_sd_var('DriveRotateTime', 0.1)
        self.register_sd_var('IsHotLeft', False, add_prefix=False)
        self.register_sd_var('IsHotRight', False, add_prefix=False)
    
    def update(self, tm):
        if tm > 0.3:
            self.catapult.pulldown()
            
            if not self.decided:
                self.IsHotLeft = wpilib.SmartDashboard.GetBoolean("IsHotLeft")
                self.IsHotRight = wpilib.SmartDashboard.GetBoolean("IsHotRight")
            
                if (self.hotLeft or self.hotRight) and not (self.hotLeft and self.hotRight):
                    self.decided = True
                
                    if self.hotLeft:
                        self.drive_rotate_speed = self.drive_rotate_speed_left
                    else:
                        self.drive_rotate_speed = self.drive_rotate_speed_right
        super().update(tm)
        
    
    @timed_state(time=1, next_state='drive_wait', first=True)
    #@timed_state(time=6, next_state='try_shoot')
    def drive_wait(self, tm, state_tm):
        pass
    def try_shoot(self,tm,state_tm):
        self.decided=True
        self.drive_rotate_speed = self.drive_rotate_speed_left
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

