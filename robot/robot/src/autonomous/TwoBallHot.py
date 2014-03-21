try:
    import wpilib
except ImportError:
    from pyfrc import wpilib
from common.autonomous_helper import StatefulAutonomous, timed_state

class TwoBall(StatefulAutonomous):
    
    MODE_NAME = 'Two Balls Hot'
    DEFAULT = False
    
    DISABLED = True
    
    def __init__(self, components):
        super().__init__(components)
        self.drive_speed=1
        self.register_sd_var('hotLeft',False)
        self.register_sd_var("hotRight",False)
        #please change the drive rotate speeds, I'm really 
        #just guessing about the values
        self.register_sd_var('drive_rotate_speed_left', -0.5)
        self.register_sd_var('drive_rotate_speed_right', 0.55)
        
        
        wpilib.SmartDashboard.PutBoolean('IsHotLeft', False)
        wpilib.SmartDashboard.PutBoolean('IsHotRight', False)
        
        self.gyroAngle=wpilib.SmartDashboard.GetNumber('GyroAngle')
        self.spinSeconds=0
        self.spinAdjust=0
        
        self.rotatedRight=-1
        #this is used to determine whether we rotated to shoot left or right
        #1 or -1, 1 for rotating left, -1 for rotating right
        self.decided = False
        
    def update(self, tm):
        print(self.gyroAngle)
        if tm > 0.3:
            self.catapult.pulldown()
            
        if not self.decided:
            self.hotLeft = wpilib.SmartDashboard.GetBoolean("IsHotLeft")
            self.hotRight = wpilib.SmartDashboard.GetBoolean("IsHotRight")
            
            if (self.hotLeft or self.hotRight) and not (self.hotLeft and self.hotRight):
                self.decided = True
                
                if self.hotLeft:
                    self.RotateLeft()
                    #print ("hot Left")
                else:
                    self.RotateRight()
                    #print ('hot right')
            else:
                self.RotateLeft()
        super().update(tm)
    def RotateRight(self):
        self.drive_rotate_speed = self.drive_rotate_speed_right
        print('hot left')

    def RotateLeft(self):
        self.drive_rotate_speed = self.drive_rotate_speed_left
        print('hot right')

    
    #
    #I have no idea how the timing is supposed to work from states 'nextball1' to 'launch2'.
    #For the moment I'm just going to add one second to each state.    
    #
    #Please contact Timmy and get him to explain the timngs on his old TwoBall class
    @timed_state(duration=.5, next_state='drive_rotate', first=True)
    def drive_wait(self, tm, state_tm):
        '''intake arm down'''
        self.intake.armDown
        
    
    @timed_state(duration=1,next_state='drive_start')
    def drive_rotate(self, tm, state_tm):
        '''rotating'''
        self.drive.move(0,0,self.drive_rotate_speed)
        self.rotatedRight

    @timed_state(duration=1,next_state='launch')
    def drive_start(self, tm, state_tm):
         '''driving'''
         self.drive.move(0, self.drive_speed, 0)

    @timed_state(duration=1,next_state='next_ball1')
    def launch(self, tm, state_tm):
        '''launching'''
        self.catapult.launchNoSensor()
        #self.spinSeconds=calculate_rotate(self.gyroAngle)
        self.spinAdjust=adjustment_rotation()
    @timed_state(duration=1, next_state='next_ball1_rotate')
    def next_ball1(self,tm, state_tm):
            '''moving backwards to get next ball'''
            self.drive.move(0, -1*self.drive_speed,adjust_rotation())
            self.intake.ballIn()
            print('attempting the correction code')
        
    @timed_state(duration=1, next_state='next_ball2')        
    def next_ball1_rotate(self,tm, state_tm):
            '''rotating'''
            
            self.drive.move(0, 0, self.drive_rotate_speed)
            self.intake.ballIn()  
            
    @timed_state(duration=1, next_state='rotate2')        
    def next_ball2(self,tm, state_tm):
            '''moving back to position'''
            self.drive.move(0, self.drive_speed,adjust_rotation())
            self.intake.ballIn()
            
    @timed_state(duration=1,next_state='driveshoot2')
    def rotate2(self,tm, state_tm):
        '''rotateing to shoot'''
        self.drive.move(0,0,self.drive_rotate_speed)
        self.intake.ballIn()
    @timed_state(duration=1,next_state='launch2')
    def driveshoot2(self,tm,state_tm):
        '''moving foreward to shoot'''
        self.drive.move(0,self.drive_speed,0)
        self.intake.ballIn()
    @timed_state(duration=1, next_state='finished_shoot')    
    def launch2(self,tm, state_tm):
            '''Finally, fire and keep firing for 1 seconds'''
            self.catapult.launchNoSensor()
    @timed_state(duration=1000)
    def finished_shoot(self,tm,state_tm):
        '''idle'''
        pass
    def calculate_rotate(self,degreesToSpin):
        if degreesToSpin >0 and degreesToSpin<180:
            pass
        elif degreesToSpin>=180 and degreesToSpin<360:
            degreesToSpin=360-degreesToSpin
        else:
            print(degreesToSpin)
        fullSpinTime=2.0
        degreesPerSecond=360.0/fullSpinTime
        secondsToSpin=degreesToSpin/degreesPeSecond
        print('spining for ',self.spinSeconds,' seconds')
        return secondsToSpin
    def adjust_rotation(self):
        degreesToSpin=wpilib.SmartDashboard.GetNumber('GyroAngle')
        adjustment=0
        if degreesToSpin>0:
            adjustment=-.1
        elif degreesToSpin<0:
            adjustment=.1
        return adjustment
        