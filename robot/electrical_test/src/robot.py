
try:
    import wpilib
except ImportError:
    from pyfrc import wpilib


class MyRobot(wpilib.SimpleRobot):
   
    def __init__ (self):
        super().__init__()
        
        print("Electrical test program -- don't use for competition!")
        
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
        
        # Arm up/down control
        self.vent_bottom_solenoid = wpilib.Solenoid(3)
        self.fill_bottom_solenoid = wpilib.Solenoid(4)
        self.fill_top_solenoid = wpilib.Solenoid(5)
        self.vent_top_solenoid = wpilib.Solenoid(6)
        
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
    
   
    def OperatorControl(self):
        # print(self.IsEnabled())
        
        # for testing, we don't care about this
        wpilib.GetWatchdog().SetEnabled(False)
        
        while self.IsOperatorControl()and self.IsEnabled():

            
            #Driving
            self.robot_drive.MecanumDrive_Cartesian(self.joystick1.GetY(), self.joystick1.GetX(), -1*self.joystick2.GetX())
            
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
        self.gearbox_in_solenoid.Set(self.joystick2.GetRawButton(6))
        self.gearbox_out_solenoid.Set(self.joystick2.GetRawButton(7))
        self.vent_bottom_solenoid.Set(self.joystick2.GetRawButton(8))
        self.fill_bottom_solenoid.Set(self.joystick2.GetRawButton(9))
        self.fill_top_solenoid.Set(self.joystick2.GetRawButton(10))
        self.vent_top_solenoid.Set(self.joystick2.GetRawButton(11))
                
        
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

