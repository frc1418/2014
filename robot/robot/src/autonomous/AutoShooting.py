
try:
    import wpilib
except ImportError:
    from pyfrc import wpilib

class AutoShooting(object):
    ''' sample autonomous program'''
    
    DEFAULT = True
    MODE_NAME = "AutoShooting"
    
    def __init__(self, components):
        '''Assume that any components needed will be passed in as a parameter. Store them so you can use them'''
        self.drive = components['drive']
        self.intake = components['intake']
        self.catapult = components['catapult']
        self.timer = wpilib.Timer()
        self.goalHot=0                 #-1,not active,1 active, 0 maybe
    def on_enable(self):
        pass

    def on_disable(self):
        '''This function is called when autonomous mode is disabled'''
        pass

    def update(self, time_elapsed):
        self.intake.armDown()
        self.catapult.pulldown()
        self.goalHot=wpilib.SmartDashboard.getNumber("goalHot")
        if not self.in_range:
            self.drive.move(0,1,0)
        if self.drive.closePosition():
            self.in_range=True
            self.timer.Start()
            if self.timer.HasPeriodPassed(2):
                self.nextStage = True
        

        if self.nextStage:
            if self.goalHot is -1:
                if time_elapsed>9:
                    self.catapult.ShootNoSensor()
                elif time_elapsed>5:
                    rotatetoposition()
            elif self.goalHot is 0:
                if time_elapsed>5:
                    self.catapult.ShootNoSensor()
            elif self.goalHot is 1:
                self.catapult.ShootNoSensor()
    def rotate(self):
        x=0
        y=0
        z=0
        self.drive.move(x,y,z)
        pass
    
    
    
    
    
    