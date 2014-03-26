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
    def on_enable(self):
        super().on_enable()
        
    def update(self, tm):
       
        if tm > 0.3:
            self.catapult.pulldown()
            
        super().update(tm)
    
    
    @timed_state(duration=1.2, next_state='drive', first=True)       
    def drive_wait(self, tm, state_tm):
        '''Wait some period before we start driving'''
        self.intake.armDown()
        
    @timed_state(duration=1.4, next_state='launch')
    def drive(self, tm, state_tm):
        '''Start the launch sequence! Drive slowly forward for N seconds'''
        self.drive.move(0, self.drive_speed, 0)
        self.intake.armDown()
    
    @timed_state(duration=1, next_state='go_back') 
    def launch(self, tm):
        '''Fire and keep firing for 1 seconds'''
        self.catapult.launchNoSensor()
        
    
    @timed_state(duration=2.9,next_state='drive2') 
    def go_back(self):
        '''Go back to get the next ball'''
        self.drive.move(0, -1*self.drive_speed, 0)
        self.intake.ballIn()
            
    @timed_state(duration=2.5, next_state='launch2', first=False)
    def drive2(self, tm, state_tm):
        '''Once we get it, drive forward'''
        self.drive.move(0, self.drive_speed, 0)
        self.intake.ballIn()
    
    @timed_state(duration=1) 
    def launch2(self, tm):
        '''And shoot!'''
        self.catapult.launchNoSensor()
        self.intake.ballIn()
