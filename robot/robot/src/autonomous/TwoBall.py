class TwoBall(object):
    ''' sample autonomous program'''
    
    DEFAULT = True
    MODE_NAME = "Two-Ball Autonomous"
    
    def __init__(self, components):
        '''Assume that any components needed will be passed in as a parameter. Store them so you can use them'''
        
        self.drive = components['drive']
        self.intake = components['intake']
        self.catapult = components['catapult']

    def on_enable(self):
        '''This function is called when autonomous mode is enabled'''
        self.nextStage = False
        self.in_range = False
        self.ball = False
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
        
        self.catapult.pulldown()
        if not self.in_range:
            self.drive.move(0,1,0)
            if self.drive.closePosition():
                self.in_range=True
                self.nextStage = True
                
        if self.nextStage:
            self.catapult.launchNoSensor()
            self.catapult.pulldown()
            if not self.ball:
                self.drive.move(0,-1,0)
                if self.catapult.check_ready():
                    self.ball = True
                    self.nextStage = False
                    self.in_range=False
                
        
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                