try:
    import wpilib
except ImportError:
    from pyfrc import wpilib
from common.autonomous_helper import StatefulAutonomous, timed_state

class TwoBallHotAim(StatefulAutonomous):
    
    MODE_NAME = 'Two Balls Hot Aim'
    DEFAULT = False
    
    DISABLED = True
    
    def __init__(self, components):
        super().__init__(components)
        self.drive_speed=1
        self.register_sd_var('hotLeft',False)
        self.register_sd_var("hotRight",False)

        self.register_sd_var('drive_rotate_speed_left', -0.5)
        self.register_sd_var('drive_rotate_speed_right', 0.55)
        
        
        wpilib.SmartDashboard.PutBoolean('IsHotLeft', False)
        wpilib.SmartDashboard.PutBoolean('IsHotRight', False)
        
        self.gyroAngle=wpilib.SmartDashboard.GetNumber('GyroAngle')
        self.spinSeconds=0
        self.spinAdjust=0
        
        
        
        self.decided=False
        
        self.initial_right_rotation=True
        #this is used to determine whether we initially 
        #rotated to shoot left or right
        #default right

    def update(self, tm):
        print(self.gyroAngle)
        if tm > 0.3:
            self.catapult.pulldown()
        if tm>.5 and tm<1.2:
            check_hot(tm)
            #because of the possible delay
            #only ever really needs to do it once at the beginning
        '''
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
                self.RotateLeft()'''
        super().update(tm)
    def RotateRight(self):
        self.drive_rotate_speed = self.drive_rotate_speed_right
        print('hot left')

    def RotateLeft(self):
        self.drive_rotate_speed = self.drive_rotate_speed_left
        print('hot right')

    
    @timed_state(duration=1.2, next_state='drive_rotate', first=True)
    def drive_wait(self, tm, state_tm):
        '''intake arm down'''
        self.intake.armDown

        
    
    @timed_state(duration=.1,next_state='drive_start')
    def drive_rotate(self, tm, state_tm):
        '''rotating'''
        #testing out moving while rotating
        self.drive.move(0,1,self.drive_rotate_speed)
        self.rotatedRight

    @timed_state(duration=1,next_state='launch')
    def drive_start(self, tm, state_tm):
         '''driving'''
        #.4 seconds reduced, added in drive to state'launch'
         self.drive.move(0, self.drive_speed, 0)

    @timed_state(duration=.8,next_state='reverse_launch')
    def launch(self, tm, state_tm):
        '''launching'''
        #in order to shave some time we're going to try moving
        #and shooting at the same time
        #.4 seconds reduced in drive_start, .8 seconds at half speed in launch
        self.drive.move(0,(self.drive_speed/2),0)
        self.catapult.launchNoSensor()
        self.spinAdjust=adjustment_rotation()
        
        #total time moving so far is
        #state:time,(speed,rotation)
        #note that 1 is standard speed for speed and rotation
        #
        #drive_rotate:.1,(1,1)
        #drive_start:1,(1,0)
        #launch:.8,(.5,0)
        #
        #total time=1.9
        #
        
        
        #
        #The reverse functions are to get us back to our start by
        #reversing the drive and rotations when we were shooting
        #
    @timed_state(duration=.8, next_state='reverse_drive_start')
    def reverse_launch(self,tm, state_tm):
            '''moving backwards to get next ball'''
            #reverse launch
            self.drive.move(0, -1*self.drive_speed/2,0)
            self.intake.ballIn()
    @timed_state(duration=1, next_state='reverse_drive_rotate')
    def reverse_drive_start(self,tm, state_tm):
            '''moving backwards to get next ball'''
            #reverse drivestart
            self.drive.move(0, -1*self.drive_speed,0)
            self.intake.ballIn()
    @timed_state(duration=.1, next_state='next_ball1_rotate')
    def reverse_drive_rotate(self,tm,state_tm):
            #reverse drive_rotate
            self.drive.move(0,-1(self.drive_speed),self.drive_rotate_speed)
            
            #Here the correction time we need to do is calculated
            self.spinSeconds=calculate_rotate()
            
    @timed_state(duration=.3, next_state='move_back_short')        
    def next_ball1_rotate(self,tm, state_tm):
            '''rotating'''
            #by now we should hopefully be back at start.
            #this state should correct any deviation from that
            #
            #calculate_rotate function needs to be fixed
            #
            #We need to use the gyro to find out the deviation
            #between going strait back and our current direction
            #feed it calculate_rotate in reverse_drive_rotate
            if state_tm>self.spinSeconds:
                next_state="move_back_short"
            self.drive.move(0,0,adjust_rotation_faster())
            self.intake.ballIn()  
    @timed_state(duration=0.7,next_state='next_ball2')
    def move_back_short(self):
            '''back a short bit'''
            self.drive.move(0,-1*self.drive_speed, 0)
            self.intake.ballIn()
            
            
    @timed_state(duration=.7, next_state='rotate2')        
    def next_ball2(self,tm, state_tm):
            '''moving back to position'''
            self.drive.move(0, self.drive_speed,adjust_rotation())
            self.intake.ballIn()
            
    @timed_state(duration=.1,next_state='driveshoot2')
    def rotate2(self,tm, state_tm):
        '''rotateing to shoot'''
        self.drive.move(0,0,-1*self.drive_rotate_speed)
        self.intake.ballIn()
    @timed_state(duration=1.5,next_state='launch2')
    def driveshoot2(self,tm,state_tm):
        '''moving foreward to shoot'''
        self.drive.move(0,self.drive_speed,0)
        self.intake.ballIn()
    @timed_state(duration=1)    
    def launch2(self,tm, state_tm):
            '''Finally, fire and keep firing for 1 seconds'''
            self.catapult.launchNoSensor()

    def calculate_rotate(self,degreesToSpin):
        #this function is to calculate length of time
        #the robot needs to rotate once
        #it gets back to position to get the 
        #second ball
        
        #not yet completed
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
        #this function is to make the robot go strait
        #in order to use put it inside the drive.move
        #Ex: drive.move(0,0,adjust_rotation())
        
        degreesToSpin=self.drive.return_gyro_angle()
        adjustment=0
        #5 degree deadzone
        if degreesToSpin>5 and degreesToSpin<180:
            adjustment=-.1
        elif degreesToSpin<-5 or (degreesToSpin>=180 and degreesToSpin<355):
            adjustment=.1
        else:
            print(degreesToSpin,' degrees rotate, failed adjustment, defaulting to zero')
        return adjustment
    def adjust_rotation_faster(self):
        if degreesToSpin>5 and degreesToSpin<180:
            adjustment=-1*self.drive_rotate_speed
        elif degreesToSpin<-5 or (degreesToSpin>=180 and degreesToSpin<355):
            adjustment=self.drive_rotate_speed
        else:
            print(degreesToSpin,' degrees rotate, failed adjustment, defaulting to zero')
        return adjustment
    def check_hot(self,tm):
        self.hotLeft = wpilib.SmartDashboard.GetBoolean("IsHotLeft")
        self.hotRight = wpilib.SmartDashboard.GetBoolean("IsHotRight")
        if self.decided==False:
            if (self.hotLeft or self.hotRight) and not (self.hotLeft and self.hotRight):
                self.decided=True
                if self.hotLeft:
                    self.RotateLeft()
                    self.initial_right_rotation=False
                    #print ("hot Left")
                else:
                    self.RotateRight()
                    #print ('hot right')
            elif tm>1:
                self.decided=True
                self.RotateRight()
                print('defaulting to right, no hotgoal detected after 1 second')
            
        