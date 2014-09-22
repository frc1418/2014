try:
    import wpilib
except ImportError:
    from pyfrc import wpilib
from common.autonomous_helper import StatefulAutonomous, timed_state

class TwoBallHotGyro(StatefulAutonomous):
    
    MODE_NAME = 'Two Balls Hot Gyro'
    DEFAULT = False
    
    
    def __init__(self, components):
        super().__init__(components)
        #direction will be positive if we want the robot to rotate to the right,
        #and negative if we want it to rotate to the left
        self.direction = 1
        self.drive_speed = 1
        self.register_sd_var('hotLeft', False)
        self.register_sd_var("hotRight", False)
        # please change the drive rotate speeds, I'm really 
        # just guessing about the values
        self.register_sd_var('rotating_angle', 15)
        
        self.gyroAngle = wpilib.SmartDashboard.GetNumber('GyroAngle')
        # this is used to determine whether we rotated to shoot left or right
        # 1 or -1, 1 for rotating left, -1 for rotating right
        self.decided = False
        
    def update(self, tm):
        #print(self.gyroAngle)
        if tm > 0.3:
            self.catapult.pulldown()
            
            
        if not self.decided:
            
            if (self.hotLeft or self.hotRight) and not (self.hotLeft and self.hotRight):
                self.decided = True
                
                if self.hotLeft:
                    self.direction = -1
                    # print ("hot Left")
                else:
                    self.direction = 1
                    # print ('hot right')

        super().update(tm)
    
    
    @timed_state(duration=1.2, next_state='drive_rotate', first=True)
    def drive_wait(self, tm, state_tm):
        '''intake arm down'''
        self.intake.armDown()
    
    @timed_state(duration=.1, next_state='drive_start')
    def drive_rotate(self, tm, state_tm):
        '''rotating'''
        if not self.decided:
            self.decided = True
            
        self.drive.angle_rotation(self.rotating_angle * self.direction)
        self.intake.armDown()
        

    @timed_state(duration=1.4, next_state='launch')
    def drive_start(self, tm, state_tm):
         '''driving'''
         
         self.drive.move(0, self.drive_speed, 0)
         self.drive.angle_rotation(self.rotating_angle * self.direction)
         self.intake.armDown()
         

    @timed_state(duration=1, next_state='next_ball1')
    def launch(self, tm, state_tm):
        '''launching'''
        
        self.catapult.launchNoSensor()
        print("launched")
        self.intake.armDown()
        
        # self.spinSeconds=calculate_rotate(self.gyroAngle)
        self.drive.angle_rotation(self.rotating_angle * self.direction)
    @timed_state(duration=.7, next_state='next_ball1_rotate')
    def next_ball1(self, tm, state_tm):
        '''moving backwards to get next ball'''
        
        self.drive.move(0, -1 * self.drive_speed, 0)
        self.drive.angle_rotation(self.rotating_angle * self.direction)
        
        self.intake.ballIn()
        self.intake.armNeutral()
        
        #print('attempting the correction code')
        
        
    @timed_state(duration=.1, next_state='move_back_short')        
    def next_ball1_rotate(self, tm, state_tm):
        '''rotating'''
        
        
        self.intake.ballIn()
        self.drive.angle_rotation(0)
        
        
    @timed_state(duration=0.7, next_state='next_ball2')
    def move_back_short(self):
        '''back a short bit'''
        self.drive.move(0, -1*self.drive_speed, 0)
        self.intake.ballIn()
        self.drive.angle_rotation(0)
        
    @timed_state(duration=.7, next_state='rotate2')  
    def next_ball2(self, tm, state_tm):
        '''moving back to position'''
        
        self.drive.move(0, self.drive_speed,0)
        self.drive.angle_rotation(0)
        
        self.intake.ballIn()
              
            
    @timed_state(duration=.1, next_state='driveshoot2')
    def rotate2(self, tm, state_tm):
        '''rotating to shoot'''
        
        self.intake.ballIn()
        self.drive.angle_rotation(self.rotating_angle * (-1*self.direction))
        
    @timed_state(duration=1.5, next_state='launch2')
    def driveshoot2(self, tm, state_tm):
        
        '''moving foreward to shoot'''
        
        self.drive.move(0, self.drive_speed, 0)
        self.drive.angle_rotation(self.rotating_angle * (-1*self.direction))
        
        self.intake.ballIn()
        
    @timed_state(duration=1)    
    def launch2(self, tm, state_tm):
        
        '''Finally, fire and keep firing for 1 seconds'''
        self.catapult.launchNoSensor()
        self.drive.angle_rotation(self.rotating_angle * (-1*self.direction))
        
