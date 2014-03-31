try:
    import wpilib
except ImportError:
    from pyfrc import wpilib
from common.autonomous_helper import StatefulAutonomous, timed_state

import timed_shoot

class HotShootAutonomous(timed_shoot.TimedShootAutonomous):
    '''
        Based on the TimedShootAutonomous mode. Modified to allow
        shooting based on whether the hot goal is enabled or not.
    '''
    
    DEFAULT = False
    MODE_NAME = "Hot shoot"

    def __init__(self, components):
        super().__init__(components)
        
        wpilib.SmartDashboard.PutBoolean('IsHotLeft', False)
        wpilib.SmartDashboard.PutBoolean('IsHotRight', False)
        
        self.register_sd_var('Left Side', False)
        
        self.register_sd_var('Right Side', False)

    def on_enable(self):
        '''these are called when autonomous starts'''
        
        super().on_enable()
        
        self.decided = False
        self.start_time = None
        
    def update(self, tm):
        
        #self.intake.armDown()
        #if tm > 0.3:
            #self.catapult.pulldown()
       if not self.decided and tm >1.2:
            self.hot = wpilib.SmartDashboard.GetBoolean("IsHotLeft") or \
                       wpilib.SmartDashboard.GetBoolean("IsHotRight")
            
            if self.hot:
                self.decided = True
                
            elif tm > 6:
                # at 6 seconds, give up and shoot anyways
                self.decided = True
         
       super().update(tm)
        
    @timed_state(duration=1.2, next_state='wait_for_decision',first=True)
    def drive_wait(self):
        '''wait some period before we start driving'''
        pass
    
    @timed_state(duration=100)   
    def wait_for_decision(self):
        '''Only begin shooting once a decision has been made
           TODO: is there a better way to express this state?'''
        if self.decided:
            self.next_state('drive1')
    
    @timed_state(duration=1.6, next_state='launch')
    def drive1(self):
        '''Start the launch sequence! Drive slowly forward for N seconds'''
        self.drive.move(0, self.drive_speed, 0)
    
    @timed_state(duration=1.0)
    def launch(self):
        '''Finally, fire and keep firing for 1 seconds'''
        self.catapult.launchNoSensor()
    