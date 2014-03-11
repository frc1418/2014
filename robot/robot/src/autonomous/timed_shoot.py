try:
    import wpilib
except ImportError:
    from pyfrc import wpilib
from common.autonomous_helper import StatefulAutonomous, timed_state

class TimedShootAutonomous(StatefulAutonomous):
    '''
        Tunable autonomous mode that does dumb time-based shooting
        decisions. Works consistently. 
    '''
    
    DEFAULT = False
    MODE_NAME = "Timed shoot"
    
    def __init__(self, components):
        super().__init__(components)
        
        self.register_sd_var('drive_speed', 0.5)
    
    def on_disable(self):
         '''This function is called when autonomous mode is disabled'''
         pass

    def update(self, tm):
        if tm > 0.3:
            self.catapult.pulldown()
            
        super().update(tm)
        
 
    @timed_state(time=1.5, next_state='drive', first=True)
    def drive_wait(self, tm, state_tm):
        pass
    
    def pre_drive(self, tm):
        pass
    
    @timed_state(time=1.4, next_state='launch')
    def drive(self, tm, state_tm):
        self.drive.move(0, self.drive_speed, 0)
    
    @timed_state(time=1.0)
    def launch(self, tm):
        self.catapult.launchNoSensor()


