
try:
    import wpilib
except ImportError:
    from pyfrc import wpilib

class main(object):
    '''autonomous program'''
    
    DEFAULT = False
    MODE_NAME = "Tim's Mode"
    
    def __init__ (self, components):
        ''' initialize'''
        super().__init__()
        self.drive = components['drive']
        self.intake = components['intake']
        self.catapult = components['catapult']
        
        # number of seconds to drive forward, allow us to tune it via SmartDashboard
        wpilib.SmartDashboard.PutNumber('AutoDriveTime', 1.4)
        wpilib.SmartDashboard.PutNumber('AutoDriveSpeed', 0.5)


    def on_enable(self):
        '''these are called when autonomous starts'''
        
        self.drive_time = wpilib.SmartDashboard.GetNumber('AutoDriveTime')
        self.drive_speed = wpilib.SmartDashboard.GetNumber('AutoDriveSpeed')
        
        print("Team 1418 autonomous code for 2014")
        print("-> Drive time:", self.drive_time, "seconds")
        print("-> Drive speed:", self.drive_speed)
        
        #print("-> Battery voltage: %.02fv" % wpilib.DriverStation.GetInstance().GetBatteryVoltage())
        
        
    
    def on_disable(self):
         '''This function is called when autonomous mode is disabled'''
         pass

    def update(self, time_elapsed):   
        '''The actual autonomous program'''     
       
        # always pulldown
        if time_elapsed > 0.3:
            self.catapult.pulldown()
            
       
        if time_elapsed < 0.3:
            # Get the arm down so that we can winch
            self.intake.armDown()

        
        elif time_elapsed < 1.4:
            # The arm is at least far enough down now that
            # the winch won't hit it, start winching
            self.intake.armDown()
            
        elif time_elapsed < 2.0:
            # We're letting the winch take its sweet time
            pass
            
        elif time_elapsed < 2.0 + self.drive_time:
            # Drive slowly forward for N seconds
            self.drive.move(0, self.drive_speed, 0)
            
            
        elif time_elapsed < 2.0 + self.drive_time + 1.0:
            # Finally, fire and keep firing for 1 seconds
            self.catapult.launchNoSensor()

            

            
