
try:
    import wpilib
except ImportError:
    from pyfrc import wpilib

class AutoShooting(object):
    ''' sample autonomous program'''
    
    DEFAULT = False
    MODE_NAME = "AutoShooting"
    
    def __init__(self, components):
        '''Assume that any components needed will be passed in as a parameter. Store them so you can use them'''
        self.drive = components['drive']
        self.intake = components['intake']
        self.catapult = components['catapult']
        self.timer = wpilib.Timer()
        self.timer2=wpilib.Timer()
        self.goalHot=0                 #-1,not active,1 active, 0 maybe
        wpilib.SmartDashboard.PutNumber("position",0)
        wpilib.SmartDashboard.PutNumber("Goal Hot",0)
    def on_enable(self):
        self.timer2.Reset()
        self.timer2.Start()
        self.nextStage = False
        self.in_range = False
        self.ball = False
        self.launchTime = None
        
        
        self.position=wpilib.SmartDashboard.GetNumber("position")            #-1 left, 0 center, 1 right
        #self.position=0
        
        self.rotate=0
        self.rotateTimeLength=0
        self.rotateTimer=wpilib.Timer()
        
        if self.position is -1:             #45 degrees to the right
            self.rotate=45
        if self.position is 0:              #30 degrees to the right
            self.rotate=45
        if self.position is 1:              #45 degrees to the left
            self.rotate=-45

    def on_disable(self):
        '''This function is called when autonomous mode is disabled'''
        pass

    def update(self, time_elapsed):
        self.intake.armDown()
        self.catapult.pulldown()
        self.goalHot=int(wpilib.SmartDashboard.GetNumber("Goal Hot"))
        print(self.timer2.Get(),"        ",self.goalHot)
        if not self.in_range and self.timer2.Get()<3:
            print("not in range")
            self.drive.move(0,1,0)
        if self.drive.closePosition() or self.timer2.Get()>3:
            self.in_range=True
            self.timer.Start()
            if self.timer.HasPeriodPassed(1):
                self.timer.Stop()
                self.nextStage = True

        if self.nextStage:
            print("next Stage is true")            
            if self.position == 0 and self.timer2.Get()<4:       #rotates to the left for 1 second
                self.drive.move(0,0,-1)
            if self.goalHot == -1:
                print("no hotgoal")
                if self.timer2.Get()>8:
                    self.catapult.launchNoSensor()
                    print("Shoot, 8 seconds elapsed")
                elif self.timer2.Get()>5:                #after 5 seconds if the current goal is not hot rotate and shoot
                    rotateToPosition(self.rotate)
            elif self.goalHot == 0:                 #maybe generally means sensors aren't working. shoot after 5 seconds
                print("maybe")
                if self.timer2.Get()>5:
                    self.catapult.launchNoSensor()
                    print("shoot, sensor value is maybe")
            elif self.goalHot == 1:                 #if the goal is currently hot then shoot
                self.catapult.launchNoSensor()
                
    def rotateToPosition(self,degrees):   #degrees is the number of degrees we want to rotate. - for left, + for right
        #assuming 2.5 seconds for a full 360 degrees. probably a bit inaccurate
        degreesPerSecond=144
        self.rotateTimeLength=math.fabs(degrees/degreesPerSecond)
        self.rotateTimer.Start()
        x=0
        y=0
        z=0
        
        if self.rotateTimer.HasPeriodPassed(rotateTimeLength):
            self.catapult.launchNoSensor()
            print("shoot, rotation time elapsed")
        elif degrees<0:
            z=-1
        elif degrees>0:
            z=1
        self.drive.move(x,y,z)
        
    
    
    
    
    
    