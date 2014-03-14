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
        
    def update(self, tm):
        if tm > 0.3:
            self.catapult.pulldown()
            
        super().update(tm)
        
    
    @timed_state(time=1, next_state='drive_wait', first=True)
    @timed_state(time=2,next_state='drive_start')
    @timed_state(time=4,next_state='try_shoot')
    @timed_state(time=5.5, next_state='next_ball1')
    
    @timed_state(time=6.5, next_state='next_ball2')
    @timed_state(time=7.5, next_state='launch2')
    
    
    #
    #I have no idea how the timing is supposed to work from states 'nextball1' to 'launch2'.
    #For the moment I'm just going to add one second to each state.    
    #
    #Please contact Timmy and get him to explain the timngs on his old TwoBall class
    
    
    def launch2(self):
        
            # Finally, fire and keep firing for 1 seconds
            self.catapult.launchNoSensor()
            self.intake.ballIn()
            
    def next_ball2(self):
                    
            self.drive.move(0, self.drive_speed, 0)
            self.intake.ballIn()
            
    def next_ball1(self):
            self.drive.move(0, -1*self.drive_speed, 0)
            self.intake.ballIn()
            
    def drive_wait(self, tm, state_tm):
        self.intake.armDown
    def drive_start(self):
         self.drive.move(0, self.drive_speed, 0)
         self.intake.armDown()
    def try_shoot(self,tm,state_tm):
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

