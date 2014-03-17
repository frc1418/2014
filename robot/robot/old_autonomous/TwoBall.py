
try:
    import wpilib
except ImportError:
    from pyfrc import wpilib
    
import timed_shoot

class TwoBall(timed_shoot.TimedShootAutonomous):
    ''' sample autonomous program'''
    
    DEFAULT = False
    MODE_NAME = "Two-Ball Autonomous"
    
    def __init__(self, components):
        '''Assume that any components needed will be passed in as a parameter. Store them so you can use them'''
        
        super().__init__(components)
        

    def on_enable(self):
        '''This function is called when autonomous mode is enabled'''
        super().on_enable()
        

    def on_disable(self):
        '''This function is called when autonomous mode is disabled'''
        pass

    def update(self, time_elapsed):
        
        # always keep the arm down
        
        # wait a split second for the arm to come down, then
        # keep bringing the catapult down so we're ready to go
        if time_elapsed > 0.3:
            self.catapult.pulldown()
            
       
        # wait some period before we start driving
        if time_elapsed < self.drive_wait:
            self.intake.armDown()
        

        elif time_elapsed < self.drive_wait + self.drive_time:
            # Start the launch sequence! Drive slowly forward for N seconds
            self.drive.move(0, self.drive_speed, 0)
            self.intake.armDown()
            
            
        elif time_elapsed < self.drive_wait + self.drive_time + 1.0:
            # Finally, fire and keep firing for 1 seconds
            self.catapult.launchNoSensor()
            
            
        elif time_elapsed < self.drive_wait + self.drive_time + 1.0 + self.drive_time + 1.5:
            
            self.drive.move(0, -1*self.drive_speed, 0)
            self.intake.ballIn()
            
        elif time_elapsed < self.drive_wait + self.drive_time + 1.0 + self.drive_time + 1.5 + \
                            self.drive_time + 1.0:
            
            self.drive.move(0, self.drive_speed, 0)
            self.intake.ballIn()
            
        elif time_elapsed < self.drive_wait + self.drive_time + 1.0 + self.drive_time + 1.5 + \
                            self.drive_time + 1.0 + 1.0:
            
            # Finally, fire and keep firing for 1 seconds
            self.catapult.launchNoSensor()
            self.intake.ballIn()
            
            
            
            
      