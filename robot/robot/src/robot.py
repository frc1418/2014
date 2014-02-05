
try:
    import wpilib
except ImportError:
    from pyfrc import wpilib
    
# import components here
from components import drive, intake, catapult

class MyRobot(wpilib.SimpleRobot):
    def __init__ (self):
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
        self.gearbox_in_solenoid = wpilib.Solenoid(1)
        self.gearbox_out_solenoid = wpilib.Solenoid(2)
        self.gearbox_solenoid=wpilib.DoubleSolenoid(1,2)
        # Arm up/down control
        self.vent_bottom_solenoid = wpilib.Solenoid(3)
        self.fill_bottom_solenoid = wpilib.Solenoid(4)
        self.fill_top_solenoid = wpilib.Solenoid(5)
        self.vent_top_solenoid = wpilib.Solenoid(6)
        
        self.bottom_solenoid=wpilib.DoubleSolenoid(3,4)
        self.top_solenoid=wpilib.DoubleSolenoid(5,6)
        
        self.robot_drive = wpilib.RobotDrive(self.lr_motor, self.rr_motor, self.lf_motor, self.rf_motor)
        self.robot_drive.SetSafetyEnabled(False)
        
        self.robot_drive.SetInvertedMotor(wpilib.RobotDrive.kFrontLeftMotor, True)
        self.robot_drive.SetInvertedMotor(wpilib.RobotDrive.kRearLeftMotor, True)
        
        # Sensors
        
        self.gyro = wpilib.Gyro(1) #THIS IS AN ANALOG PORT
        self.infrared = wpilib.AnalogChannel(2)
        self.potentiometer = wpilib.AnalogChannel(3)
        self.ultrasonic_sensor = wpilib.AnalogChannel(4)
        self.accelerometer = wpilib.ADXL345_I2C(1, wpilib.ADXL345_I2C.kRange_2G)
        self.compressor = wpilib.Compressor(1,1)
        self.compressor.Start()
        
        
        #################################################################
        #                      END SHARED CODE                          #
        #################################################################
        
        #
        # Initialize robot components here
        #
        
        self.drive = drive.Drive(self.robot_drive)

        self.catapultTimer=wpilib.Timer()
        self.catapult=catapult.Catapult(self.winch_motor,self.gearbox_solenoid,self.arm_angle_sensor,self.ball_sensor,self.catapultTimer)
        
        self.intakeTimer=wpilib.Timer()
        self.intake=intake.Intake(self.top_solenoid,self.bottom_solenoid,self.intake_motor,self.intakeTimer)
        
    def OperatorControl(self):
        while self.IsOperatorControl()and self.IsEnabled():
            potentiometer1=self.arm_angle_sensor.GetVoltage()
            launcherup=self.catapult.check_up()
            intakedirection=0
            solenoidDown=False
            if self.joystick1.GetRawButton(1) is True:
                intakedirection=1
                solenoidDown=True
            elif self.joystick1.GetRawButton(2) is True:
                intakedirection=-1
                solenoidDown=True
            elif self.joystick1.GetRawButton(3) is True:
                self.catapult.launch()
            else:
                intakedirection=0
                solenoidDown=False
            
            self.intake.wheels(intakedirection,launcherup)
            self.intake.arm(solenoidDown)
            self.intake.doit()
            self.catapult.pulldown(potentiometer1)
            self.catapult.check_ready(self.ball_sensor.GetVoltage())
            
            
           
            self.catapult.doit()
            wpilib.Wait(.02)            
def run():
    
    robot = MyRobot()
    robot.StartCompetition()
    
    return robot


if __name__ == '__main__':
    wpilib.run()

