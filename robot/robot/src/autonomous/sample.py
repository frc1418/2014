

class SampleAutonomousMode(object):
    
    DEFAULT = True
    MODE_NAME = "Sample Mode"
    
    def __init__(self, components):
        '''Assume that any components needed will be passed in as a parameter. Store them so you can use them'''
        #self.drive = components['drive']

    def on_enable(self):
        '''This function is called when autonomous mode is enabled'''
        pass

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
        
        if time_elapsed < 3.0:
            self.drive.move(0, 0, -1.0)
            
        elif time_elapsed < 6.0:
            self.drive.move(0, 0, 1.0)
            
         