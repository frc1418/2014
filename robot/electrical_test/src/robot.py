
try:
    import wpilib
except ImportError:
    from pyfrc import wpilib


class MyRobot(wpilib.SimpleRobot):
   
    def __init__ (self):
        super().__init__()
        
        print("Electrical Simulation Test. NOT LEGAL FOR COMPETITION!!!")
              
        wpilib.SmartDashboard.init()
        
        self.joystick1=wpilib.Joystick(1)
        self.joystick2=wpilib.Joystick(2)
        
        self.lf_motor=wpilib.Jaguar(1)
        self.lr_motor=wpilib.Jaguar(2)
        self.rr_motor=wpilib.Jaguar(3)
        self.rf_motor=wpilib.Jaguar(4)
        
        self.winch_motor = wpilib.CANJaguar(5)
        self.intake_motor = wpilib.Jaguar(6)
        
        self.compressor=wpilib.Compressor(1,1)
        self.compressor.Start()
        
        self.solenoid_intake_up=wpilib.Solenoid(1)
        self.solenoid_intake_down=wpilib.Solenoid(2)
        self.solenoid_release_release=wpilib.Solenoid(3)
        self.solenoid_release_engage=wpilib.Solenoid(4)
        self.solenoid_kicker_out=wpilib.Solenoid(5)
        self.solenoid_kicker_in=wpilib.Solenoid(6)
        
        self.drive = wpilib.RobotDrive(self.lr_motor, self.rr_motor, self.lf_motor, self.rf_motor)
        self.drive.SetSafetyEnabled(False)
        
        self.drive.SetInvertedMotor(wpilib.RobotDrive.kFrontLeftMotor, True)
        self.drive.SetInvertedMotor(wpilib.RobotDrive.kRearLeftMotor, True)
        
        
        self.gyro = wpilib.Gyro(1)
        
        self.ultrasonic_sensor=wpilib.AnalogChannel(3)
        self.arm_angle_sensor=wpilib.AnalogChannel(4)
        self.ball_sensor=wpilib.AnalogChannel(6)
        self.accelerometer=wpilib.ADXL345_I2C(1, wpilib.ADXL345_I2C.kRange_2G)
    
   
    def OperatorControl(self):
        # print(self.IsEnabled())
        
        # for testing, we don't care about this
        wpilib.GetWatchdog().SetEnabled(False)
        
        while self.IsOperatorControl()and self.IsEnabled():

            
            #Driving
            self.drive.MecanumDrive_Cartesian(self.joystick1.GetY(), self.joystick1.GetX(), -1*self.joystick2.GetX())
            
            self.Intake()
            self.Catapult()
            self.Solenoids()
            self.SmartDash()
            
            wpilib.Wait(0.05)
   
            
    def Intake(self):
        #Use joystick to contol the intake 
        x = self.joystick1.GetRawButton(4)
        y = self.joystick1.GetRawButton(5)
        if x:
            self.intake_motor.Set(-1)
        elif y:
            self.intake_motor.Set(1)    
        else:
            self.intake_motor.Set(0) 
            
    def Catapult(self):
        self.winch_motor.Set(self.joystick1.GetZ())
        
    def Solenoids(self):
        self.solenoid_intake_up.Set(self.joystick2.GetRawButton(6))
        self.solenoid_intake_down.Set(self.joystick2.GetRawButton(7))
        self.solenoid_release_release.Set(self.joystick2.GetRawButton(8))
        self.solenoid_release_engage.Set(self.joystick2.GetRawButton(9))
        self.solenoid_kicker_out.Set(self.joystick2.GetRawButton(10))
        self.solenoid_kicker_in.Set(self.joystick2.GetRawButton(11))
                
        
    def SmartDash(self):
        wpilib.SmartDashboard.PutNumber('GyroAngle', self.gyro.GetAngle())
        wpilib.SmartDashboard.PutNumber('Ultrasonic', self.ultrasonic_sensor.GetVoltage())
        wpilib.SmartDashboard.PutNumber('Angle Sensor', self.arm_angle_sensor.GetVoltage())
        wpilib.SmartDashboard.PutNumber('Ball Sensor', self.ball_sensor.GetVoltage())
        axis=self.accelerometer.GetAccelerations()
        wpilib.SmartDashboard.PutNumber('Acceleration Axis X', axis.XAxis)
        wpilib.SmartDashboard.PutNumber('Acceleration Axis Y', axis.YAxis)
        wpilib.SmartDashboard.PutNumber('Acceleration Axis Z', axis.ZAxis)
        
            
def run():
    robot = MyRobot()
    robot.StartCompetition()
    
    return robot


if __name__ == '__main__':
    wpilib.run()

