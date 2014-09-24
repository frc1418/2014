try:
    import wpilib
except ImportError:
    from pyfrc import wpilib

from common.autonomous_helper import StatefulAutonomous, timed_state

class TwoBall(StatefulAutonomous):
    
    MODE_NAME = 'Two balls'
    DEFAULT = True
    
    
     
    def __init__(self, components):
        super().__init__(components)
        
        self.register_sd_var('drive_speed', 0.5)
        self.register_sd_var('use_gyro', True)
        
    def on_enable(self):
        super().on_enable()
        
        if self.use_gyro:
            self.drive.reset_gyro_angle()
        
    def update(self, tm):
       
        if tm > 0.3:
            self.catapult.pulldown()
            
        super().update(tm)
    
    
    @timed_state(duration=1.2, next_state='drive', first=True)       
    def drive_wait(self):
        '''Wait some period before we start driving'''
        self.intake.armDown()
        
        if self.use_gyro:
            self.drive.angle_rotation(0)
        
    @timed_state(duration=1.4, next_state='launch')
    def drive(self):
        '''Start the launch sequence! Drive slowly forward for N seconds'''
        self.drive.move(0, self.drive_speed, 0)
        self.intake.armDown()
        
        if self.use_gyro:
            self.drive.angle_rotation(0)
    
    @timed_state(duration=1, next_state='go_back') 
    def launch(self):
        '''Fire and keep firing for 1 seconds'''
        self.catapult.launchNoSensor()
        
        if self.use_gyro:
            self.drive.angle_rotation(0)
        
    
    @timed_state(duration=2.9,next_state='drive2') 
    def go_back(self):
        '''Go back to get the next ball'''
        self.drive.move(0, -1*self.drive_speed, 0)
        self.intake.ballIn()
        
        if self.use_gyro:
            self.drive.angle_rotation(0)
            
    @timed_state(duration=2.6, next_state='launch2')
    def drive2(self):
        '''Once we get it, drive forward'''
        self.drive.move(0, self.drive_speed, 0)
        self.intake.ballIn()
        
        if self.use_gyro:
            self.drive.angle_rotation(0)
    
    @timed_state(duration=1) 
    def launch2(self):
        '''And shoot!'''
        self.catapult.launchNoSensor()
        self.intake.ballIn()
        
        if self.use_gyro:
            self.drive.angle_rotation(0)
