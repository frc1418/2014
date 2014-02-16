
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
        self.lr_motor = wpilib.Jaguar(2)
        self.rr_motor = wpilib.Jaguar(3)
        self.rf_motor = wpilib.Jaguar(4)
        
        self.winch_motor = wpilib.CANJaguar(5)
        self.intake_motor = wpilib.Jaguar(6)
        
        # Catapult gearbox control
        '''
        self.gearbox_in_solenoid = wpilib.Solenoid(1)
        self.gearbox_out_solenoid = wpilib.Solenoid(2)'''
        self.gearbox_solenoid=wpilib.DoubleSolenoid(2, 1)
        # Arm up/down control
        self.vent_bottom_solenoid = wpilib.Solenoid(3)
        self.fill_bottom_solenoid = wpilib.Solenoid(4)
        self.fill_top_solenoid = wpilib.Solenoid(5)
        self.vent_top_solenoid = wpilib.Solenoid(6)
        self.pass_solenoid=wpilib.Solenoid(7)
        '''
        self.bottom_solenoid=wpilib.DoubleSolenoid(3,4)
        self.top_solenoid=wpilib.DoubleSolenoid(5,6)
        '''
        self.robot_drive = wpilib.RobotDrive(self.lr_motor, self.rr_motor, self.lf_motor, self.rf_motor)
        self.robot_drive.SetSafetyEnabled(False)
        
        self.robot_drive.SetInvertedMotor(wpilib.RobotDrive.kFrontLeftMotor, True)
        self.robot_drive.SetInvertedMotor(wpilib.RobotDrive.kRearLeftMotor, True)
        
        # Sensors
        
        self.gyro = wpilib.Gyro(1)
        
        self.ultrasonic_sensor = wpilib.AnalogChannel(3)
        self.arm_angle_sensor = wpilib.AnalogChannel(4)
        self.ball_sensor = wpilib.AnalogChannel(6)
        self.accelerometer = wpilib.ADXL345_I2C(1, wpilib.ADXL345_I2C.kRange_2G)
        
        self.compressor = wpilib.Compressor(1,1)
        self.compressor.Start()
        
        #################################################################
        #                      END SHARED CODE                          #
        #################################################################
        
        #
        # Initialize robot components here
        #
        
        self.initSmartDashboard()
        
        
        self.drive = drive.Drive(self.robot_drive, self.ultrasonic_sensor)

        self.pushTimer=wpilib.Timer()
        self.catapultTimer=wpilib.Timer()
        self.catapult=catapult.Catapult(self.winch_motor,self.gearbox_solenoid,self.pass_solenoid,self.arm_angle_sensor,self.ball_sensor,self.catapultTimer, self.joystick1)
        
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
            wpilib.Wait(0.01)
            
        
    def OperatorControl(self):
        '''Called when the robot is in Teleoperated mode'''
        
        wpilib.SmartDashboard.PutNumber('RobotMode', MODE_TELEOPERATED)
        
        dog = self.GetWatchdog()
        dog.SetExpiration(0.25)
        dog.SetEnabled(True)
        
        preciseDelay = delay.PreciseDelay(self.control_loop_wait_time)

        while self.IsOperatorControl()and self.IsEnabled():
            self.robotMode=1
            dog.Feed()
            
            #
            # Driving
            #
            
            self.drive.move(self.joystick1.GetX(), self.joystick1.GetY(), self.joystick2.GetX())
            
            #
            # Intake
            #
            
            if self.joystick1.GetRawButton(2):
                self.intake.armDown()
            
            if self.joystick1.GetRawButton(3):
                self.intake.armUp()
                
            if self.joystick1.GetRawButton(4):
                self.intake.ballIn()
                
            if self.joystick1.GetRawButton(5):
                self.intake.ballOut()
                
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
           
            self.communicateWithSmartDashboard()
            self.update()
            
            
            preciseDelay.wait()
            
        # Disable the watchdog at the end
        dog.SetEnabled(False)
            
    def update(self):
        '''This function calls all of the doit functions for each component'''
        for component in self.components.values():
            component.doit()
    
    def initSmartDashboard(self):
        wpilib.SmartDashboard.PutBoolean("AutoWinch", False)  
        wpilib.SmartDashboard.PutNumber("FirePower", 100)
        wpilib.SmartDashboard.PutNumber("ArmSet", 0)
        wpilib.SmartDashboard.PutBoolean("Fire", False)
        wpilib.SmartDashboard.PutNumber("GyroAngle",self.gyro.GetAngle())
    
    def communicateWithSmartDashboard(self):
        '''Sends and recieves values to/from the SmartDashboard'''
        
        # Send the distance to the driver station
        wpilib.SmartDashboard.PutNumber("Distance",self.ultrasonic_sensor.GetVoltage())
        # Battery can actually be done dashboard side, fix that self (Shayne)
        
        # Put the arm state
        wpilib.SmartDashboard.PutNumber("ArmState",self.intake.GetMode())
        
        # Get if a ball is loaded
        wpilib.SmartDashboard.PutBoolean("BallLoaded", self.catapult.check_ready())
        
        # Get the number to set the winch power
        #self.WinchPowerVar = wpilib.SmartDashboard.PutNumber("FirePower",1)
        # TODO: Cleanup catapult.py and finish this
        
        # If its 0 then update the arm state
        arm_state = wpilib.SmartDashboard.GetNumber("ArmSet")
        if arm_state != 0:
            self.intake.SetMode(arm_state)
            wpilib.SmartDashboard.PutNumber("ArmSet", 0)
            # 0 it to avoid locking the driver out of arm controls

        wpilib.SmartDashboard.PutNumber("ShootAngle",self.catapult.Angle_Sensor_Values())
            
        if wpilib.SmartDashboard.GetBoolean("Fire"):
            self.catapult.launchNoSensor()
            wpilib.SmartDashboard.PutBoolean("Fire", False)
            
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
    # if you get a TypeError here, you don't have the correct version
    # of pyfrc installed
    wpilib.run(min_version='2014.4.0')

