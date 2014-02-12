

class UltrasonicAutonomous(object):
    ''' sample autonomous program'''
    
    DEFAULT = False
    MODE_NAME = "Ultrasonic-based"
    
    def __init__(self, components):
        '''Assume that any components needed will be passed in as a parameter. Store them so you can use them'''
        
        self.drive = components['drive']
        self.intake = components['intake']
        self.catapult = components['catapult']

    def on_enable(self):
        '''This function is called when autonomous mode is enabled'''
        
        self.in_range = False
        self.launchTime = None
        

    def on_disable(self):
        '''This function is called when autonomous mode is disabled'''
        pass

    def update(self, time_elapsed):
        '''Do not implement your own loop for autonomous mode. Instead, assume that
           this function is called over and over and over again during autonomous
           mode if this mode is active

           time_elapsed is a number that tells you how many seconds autonomous mode has
           been running so far.
           
           This sample makes the robot spin one way for 3 seconds, the other way for 3
           seconds, and stops the robot.
        '''
        
        self.intake.armDown()
        
        # always pull the catapult down
        if time_elapsed > 0.5:
            self.catapult.pulldown()
    
        
        if time_elapsed < 0.5:
            # Get the arm down so that we can winch
            self.intake.armDown()
        
        elif time_elapsed < 1.5:
            # The arm is at least far enough down now that
            # the winch won't hit it, start winching
            self.intake.armDown()
            
        elif time_elapsed < 2.5:
            # We're letting the winch take its sweet time
            pass
            
        else:
            
            if not self.in_range:
                # Drive slowly forward until the ultrasonic says to shoot
                self.drive.move(0,1,0)
                
                # once it says we're in range, then stop moving and shoot
                if self.drive.closePosition():
                    self.in_range = True
                    self.launchTime = time_elapsed
                
            elif time_elapsed < self.launchTime + 2.0:
                self.catapult.launchNoSensor()
                
            
         
