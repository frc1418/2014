
try:
    import wpilib
except ImportError:
    from pyfrc import wpilib
    
# import components here
from autonomous import AutonomousModeManager
from components import drive, intake, catapult

from common import delay


# keep in sync with the driver station
MODE_DISABLED       = 0
MODE_AUTONOMOUS     = 1
MODE_TELEOPERATED   = 2


class MyRobot(wpilib.SimpleRobot):
    '''
        This is where it all starts
    '''
    def __init__ (self):
        '''
            Constructor. 
        '''
        
        super().__init__()
        
        print("Team 1418 robot code for 2014")
        
        #################################################################
        # THIS CODE IS SHARED BETWEEN THE MAIN ROBOT AND THE ELECTRICAL #
        # TEST CODE. WHEN CHANGING IT, CHANGE BOTH PLACES!              #
        #################################################################
        
       
        wpilib.SmartDashboard.init()
        
        
        # Joysticks
        
        self.joystick1 = wpilib.Joystick(1)
        self.joystick2 = wpilib.Joystick(2)
        
        # Motors
        
        self.lf_motor = wpilib.Jaguar(1)
        self.lf_motor.label = 'lf_motor'
        
        self.lr_motor = wpilib.Jaguar(2)
        self.lr_motor.label = 'lr_motor'
        
        self.rr_motor = wpilib.Jaguar(3)
        self.rr_motor.label = 'rr_motor'
        
        self.rf_motor = wpilib.Jaguar(4)
        self.rf_motor.label = 'rf_motor'
        
        self.winch_motor = wpilib.CANJaguar(5)
        self.winch_motor.label = 'winch'
        
        self.intake_motor = wpilib.Jaguar(6)
        self.intake_motor.label = 'intake'
        
        # Catapult gearbox control
        self.gearbox_solenoid=wpilib.DoubleSolenoid(2, 1)
        self.gearbox_solenoid.label = 'gearbox'
        
        # Arm up/down control
        self.vent_bottom_solenoid = wpilib.Solenoid(3)
        self.vent_bottom_solenoid.label = 'vent bottom'
        
        self.fill_bottom_solenoid = wpilib.Solenoid(4)
        self.fill_bottom_solenoid.label = 'fill bottom'
        
        self.fill_top_solenoid = wpilib.Solenoid(5)
        self.fill_top_solenoid.label = 'fill top'
        
        self.vent_top_solenoid = wpilib.Solenoid(6)
        self.vent_top_solenoid.label = 'vent top'
        
        self.pass_solenoid = wpilib.Solenoid(7)
        self.pass_solenoid.label = 'pass'
        
        self.robot_drive = wpilib.RobotDrive(self.lr_motor, self.rr_motor, self.lf_motor, self.rf_motor)
        self.robot_drive.SetSafetyEnabled(False)
        
        self.robot_drive.SetInvertedMotor(wpilib.RobotDrive.kFrontLeftMotor, True)
        self.robot_drive.SetInvertedMotor(wpilib.RobotDrive.kRearLeftMotor, True)
        
        # Sensors
        
        self.gyro = wpilib.Gyro(1)
        
        self.ultrasonic_sensor = wpilib.AnalogChannel(3)
        self.ultrasonic_sensor.label = 'Ultrasonic'
        
        self.arm_angle_sensor = wpilib.AnalogChannel(4)
        self.arm_angle_sensor.label = 'Arm angle'
        
        self.ball_sensor = wpilib.AnalogChannel(6)
        self.ball_sensor.label = 'Ball sensor'
        
        self.accelerometer = wpilib.ADXL345_I2C(1, wpilib.ADXL345_I2C.kRange_2G)
        
        self.compressor = wpilib.Compressor(1,1)
        
        #################################################################
        #                      END SHARED CODE                          #
        #################################################################
        
        #
        # Initialize robot components here
        #
        
        
        self.drive = drive.Drive(self.robot_drive, self.ultrasonic_sensor,self.gyro)
        
        self.initSmartDashboard()
        
        

        self.pushTimer=wpilib.Timer()
        self.catapultTimer=wpilib.Timer()
        self.catapult=catapult.Catapult(self.winch_motor,self.gearbox_solenoid,self.pass_solenoid,self.arm_angle_sensor,self.ball_sensor,self.catapultTimer)
        
        self.intakeTimer=wpilib.Timer()
        self.intake=intake.Intake(self.vent_top_solenoid,self.fill_top_solenoid,self.fill_bottom_solenoid,self.vent_bottom_solenoid,self.intake_motor,self.intakeTimer)
        
        self.pulldowntoggle=False
        
        self.components = {
            'drive': self.drive,
            'catapult': self.catapult,
            'intake': self.intake                   
        }
        
        self.control_loop_wait_time = 0.025
        self.autonomous = AutonomousModeManager(self.components)
        
    def Autonomous(self):
        '''Called when the robot is in autonomous mode'''
        
        wpilib.SmartDashboard.PutNumber('RobotMode', MODE_AUTONOMOUS)
        self.autonomous.run(self, self.control_loop_wait_time)
        
        
    def Disabled(self):
        '''Called when the robot is in disabled mode'''
        
        wpilib.SmartDashboard.PutNumber('RobotMode', MODE_DISABLED)
        
        while self.IsDisabled():
            
            self.communicateWithSmartDashboard(True)
            
            wpilib.Wait(0.01)
            
        
    def OperatorControl(self):
        '''Called when the robot is in Teleoperated mode'''
        
        wpilib.SmartDashboard.PutNumber('RobotMode', MODE_TELEOPERATED)
        
        dog = self.GetWatchdog()
        dog.SetExpiration(0.25)
        dog.SetEnabled(True)
        
        self.compressor.Start()
        
        preciseDelay = delay.PreciseDelay(self.control_loop_wait_time)

        while self.IsOperatorControl()and self.IsEnabled():
            self.robotMode=1
            dog.Feed()
            
            #
            # Driving
            #
            if self.joystick2.GetZ()==1:
                self.drive.move((-1)*self.joystick1.GetX(), self.joystick1.GetY(), self.joystick2.GetX())
            else:
                self.drive.move(self.joystick1.GetX(), (-1)*self.joystick1.GetY(), self.joystick2.GetX())
            
            # Intake
            #
            
            if self.joystick1.GetRawButton(2):
                self.intake.armDown()
            
            if self.joystick1.GetRawButton(3):
                self.intake.armUp()
                
            if self.joystick1.GetRawButton(5):
                self.intake.ballIn()
                
            if self.joystick1.GetRawButton(4):
                self.intake.ballOut()
                
            if self.joystick1.GetRawButton(6):
                self.drive.angle_rotation(-10)
                
            if self.joystick1.GetRawButton(7):
                self.drive.angle_rotation(10)
                
            #
            # Catapult
            #
            
            if wpilib.SmartDashboard.GetBoolean("AutoWinch"):
                self.catapult.autoWinch()
           
            if self.joystick2.GetRawButton(1):
                self.catapult.launchNoSensor()
                
            if self.joystick1.GetRawButton(1):
                self.catapult.pulldownNoSensor()
            
            #
            # Other
            #
           
            self.communicateWithSmartDashboard(False)
            self.update()
            
            
            preciseDelay.wait()
            
        # Disable the watchdog at the end
        dog.SetEnabled(False)
        
        # only run the compressor in teleoperated mode
        self.compressor.Stop()
            
    def update(self):
        '''This function calls all of the doit functions for each component'''
        for component in self.components.values():
            component.doit()
    
    def initSmartDashboard(self):
        
        self.sdTimer = wpilib.Timer()
        self.sdTimer.Start()
        
        wpilib.SmartDashboard.PutBoolean("AutoWinch", False)
        wpilib.SmartDashboard.PutBoolean("EnableTuning", False)
        wpilib.SmartDashboard.PutNumber("FirePower", 100)
        wpilib.SmartDashboard.PutNumber("ArmSet", 0)
        wpilib.SmartDashboard.PutBoolean("Fire", False)
        
        wpilib.SmartDashboard.PutBoolean("GyroEnabled", True)
        wpilib.SmartDashboard.PutNumber("GyroAngle",self.gyro.GetAngle())
        
        wpilib.SmartDashboard.PutNumber("Compressor", self.compressor.GetPressureSwitchValue())
        
        wpilib.SmartDashboard.PutNumber("AngleConstant", self.drive.angle_constant)
        
        print (self.compressor.GetPressureSwitchValue())
        
    def communicateWithSmartDashboard(self, in_disabled):
        '''Sends and recieves values to/from the SmartDashboard'''
        
        # only send values every once in awhile
        if self.sdTimer.HasPeriodPassed(0.1):
        
            # Send the distance to the driver station
            wpilib.SmartDashboard.PutNumber("Distance",self.ultrasonic_sensor.GetVoltage())
            wpilib.SmartDashboard.PutNumber("GyroAngle",self.gyro.GetAngle())
            
            # Battery can actually be done dashboard side, fix that self (Shayne)
            
            # Put the arm state
            wpilib.SmartDashboard.PutNumber("ArmState",self.intake.GetMode())
            
            # Get if a ball is loaded
            wpilib.SmartDashboard.PutBoolean("BallLoaded", self.catapult.check_ready())
            
            wpilib.SmartDashboard.PutNumber("ShootAngle",self.catapult.getCatapultLocation())
            
            wpilib.SmartDashboard.PutNumber("Compressor", self.compressor.GetPressureSwitchValue())
         
        # don't remove this, this allows us to disable the gyro
        self.drive.set_gyro_enabled(wpilib.SmartDashboard.GetBoolean('GyroEnabled'))
        
         
        # don't set any of the other variables in disabled mode!
        if in_disabled:
            return
            
        # Get the number to set the winch power
        #self.WinchPowerVar = wpilib.SmartDashboard.PutNumber("FirePower",1)
        # TODO: Cleanup catapult.py and finish this
        
        
        self.drive.set_angle_constant(wpilib.SmartDashboard.GetNumber('AngleConstant'))
        
        # If its 0 then update the arm state
        arm_state = wpilib.SmartDashboard.GetNumber("ArmSet")
        if arm_state != 0:
            self.intake.SetMode(arm_state)
            wpilib.SmartDashboard.PutNumber("ArmSet", 0)
            # 0 it to avoid locking the driver out of arm controls
        
        if wpilib.SmartDashboard.GetBoolean("Fire"):
            self.catapult.launchNoSensor()
            wpilib.SmartDashboard.PutBoolean("Fire", False)
            
        self.catapult.setWinchLocation(wpilib.SmartDashboard.GetNumber('FirePower'))
        
            
def run():

    '''
        When the robot starts, this is the very first function that
        gets called
        
        :returns: a new instance of the `MyRobot` class
    '''
    
    robot = MyRobot()
    robot.StartCompetition()
    
    return robot


if __name__ == '__main__':
    
    if not hasattr(wpilib, 'require_version'):
        print("ERROR: You must have pyfrc 2014.7.3 or above installed!") # pragma: no cover
    else:    
        wpilib.require_version('2014.7.3')
    
    import physics
    wpilib.internal.physics_controller.setup(physics)
    
    wpilib.run()

