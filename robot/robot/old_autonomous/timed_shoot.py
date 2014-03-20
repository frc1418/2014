
try:
    import wpilib
except ImportError:
    from pyfrc import wpilib

class TimedShootAutonomous(object):
    '''
        Tunable autonomous mode that does dumb time-based shooting
        decisions. Works consistently. 
    '''
    
    DEFAULT = False
    MODE_NAME = "Timed shoot old"
    
    def __init__ (self, components):
        ''' initialize'''
        super().__init__()
        self.drive = components['drive']
        self.intake = components['intake']
        self.catapult = components['catapult']
        
        # number of seconds to drive forward, allow us to tune it via SmartDashboard
        wpilib.SmartDashboard.PutNumber('DriveWaitTime', 1.2)
        wpilib.SmartDashboard.PutNumber('AutoDriveTime', 1.4)
        wpilib.SmartDashboard.PutNumber('AutoDriveSpeed', 0.5)


    def on_enable(self):
        '''these are called when autonomous starts'''
        
        self.drive_wait = wpilib.SmartDashboard.GetNumber('DriveWaitTime')
        self.drive_time = wpilib.SmartDashboard.GetNumber('AutoDriveTime')
        self.drive_speed = wpilib.SmartDashboard.GetNumber('AutoDriveSpeed')
        
        self.battery_voltage = wpilib.DriverStation.GetInstance().GetBatteryVoltage()
        
        print("-> Drive wait:", self.drive_wait, "seconds")
        print("-> Drive time:", self.drive_time, "seconds")
        print("-> Drive speed:", self.drive_speed)
        print("-> Battery voltage: %.02fv" % self.battery_voltage)
        
        
    
    def on_disable(self):
         '''This function is called when autonomous mode is disabled'''
         pass

    def update(self, time_elapsed):   
        '''The actual autonomous program'''     
       
        # always keep the arm down
        self.intake.armDown()
        
        # wait a split second for the arm to come down, then
        # keep bringing the catapult down so we're ready to go
        if time_elapsed > 0.3:
            self.catapult.pulldown()
            
       
        # wait some period before we start driving
        if time_elapsed < self.drive_wait:
            pass
        

        elif time_elapsed < self.drive_wait + self.drive_time:
            # Start the launch sequence! Drive slowly forward for N seconds
            self.drive.move(0, self.drive_speed, 0)
            
            
        elif time_elapsed < self.drive_wait + self.drive_time + 1.0:
            # Finally, fire and keep firing for 1 seconds
            self.catapult.launchNoSensor()
