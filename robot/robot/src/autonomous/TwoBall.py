try:
    import wpilib
except ImportError:
    from pyfrc import wpilib
from common.autonomous_helper import StatefulAutonomous, timed_state

class TwoBall(StatefulAutonomous):
    
    MODE_NAME = 'Two balls'
    DEFAULT = False
    
    def __init__(self, components):
        super().__init__(components)
        self.register_sd_var('drive_speed', 0.5)
        
        
        
        
        
    def on_enable(self):
        super().on_enable()
    def update(self, tm):
       
        if tm > 0.3:
            self.catapult.pulldown()
            
        super().update(tm)
        
    
   
   
   
   
   
    
    
    #
    #I have no idea how the timing is supposed to work from states 'nextball1' to 'launch2'.
    #For the moment I'm just going to add one second to each state.    
    #
    #Please contact Timmy and get him to explain the timngs on his old TwoBall class 
    
   
    
    
    @timed_state(duration=1.2, next_state='drive', first=True)       
    def drive_wait(self, tm, state_tm):
        self.intake.armDown()
    
    @timed_state(duration=1.4, next_state='launch', first=False)
    def drive(self, tm, state_tm):
        self.drive.move(0, self.drive_speed, 0)
        self.intake.armDown()
    
    @timed_state(duration=1, next_state='next_ball1') 
    def launch(self, tm):
        self.catapult.launchNoSensor()
        
    
    @timed_state(duration=2.9,next_state='drive2') 
    def next_ball1(self):
            self.drive.move(0, -1*self.drive_speed, 0)
            self.intake.ballIn()
            
    @timed_state(duration=2.4, next_state='launch2', first=False)
    def drive2(self, tm, state_tm):
        self.drive.move(0, self.drive_speed, 0)
        self.intake.ballIn()
    
    @timed_state(duration=1) 
    def launch2(self, tm):
        self.catapult.launchNoSensor()
        self.intake.ballIn()
   
    #@timed_state(duration=2,next_state='drive_start')    
    #def drive_start(self, tm, state_tm):
    #self.drive.move(0, self.drive_speed, 0)
   
   
   
    
   
    '''  
    
    @timed_state(duration=1.5, next_state='launch2')
    def next_ball2(self):
                    
            self.drive.move(0, self.drive_speed, 0)
            self.intake.ballIn()
    @timed_state(duration=1.4)
    def launch2(self):
        
            # Finally, fire and keep firing for 1 seconds
            self.catapult.launchNoSensor()
            self.intake.ballIn()'''

