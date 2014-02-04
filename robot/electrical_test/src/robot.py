
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
        
        self.winch=wpilib.CANJaguar(5)
        self.intake=wpilib.Jaguar(6)
        
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
        self.ultrasonic=wpilib.AnalogChannel(2)
        self.potentiometer=wpilib.AnalogChannel(3)
        self.accelerometer=wpilib.ADXL345_I2C(1, wpilib.ADXL345_I2C.kRange_2G)
    
   
    def OperatorControl(self):
        # print(self.IsEnabled())
        # dog = wpilib.GetWatchdog()
        #dog.setEnabled(True)
        #dog.SetExpiration(10)
        
        while self.IsOperatorControl()and self.IsEnabled():
            #  dog.Feed()
            
            #Driving
            self.drive.MecanumDrive_Cartesian(self.joystick1.GetY(), self.joystick1.GetX(), -1*self.joystick2.GetX())
            
            #self.Intake()
            #self.Catapult()t
            #self.Solenoids()
            #self.SmartDash()
            
            #print (int (self.joystick.GetRawButton(8)))
            wpilib.Wait(0.05)
   
            
    def Intake(self):
        #Use joystick to contol the intake 
        x = self.joystick.GetRawButton(4)
        y = self.joystick.GetRawButton(5)
        if x:
            self.intake.Set(-1)
        elif y:
            self.intake.Set(1)    
        else:
            self.intake.Set(0) 
            
    def Catapult(self):
        self.winch.Set(self.joystick.GetZ())
        
    def Solenoids(self):
        self.solenoid_intake_up.Set(self.joystick2.GetRawButton(1))
        self.solenoid_intake_down.Set(self.joystick2.GetRawButton(2))
        self.solenoid_release_release.Set(self.joystick2.GetRawButton(3))
        self.solenoid_release_engage.Set(self.joystick2.GetRawButton(4))
        self.solenoid_kicker_out.Set(self.joystick2.GetRawButton(5))
        self.solenoid_kicker_in.Set(self.joystick2.GetRawButton(6))
                
        
    def SmartDash(self):
        wpilib.SmartDashboard.PutNumber('GyroAngle', self.gyro.GetAngle())
        wpilib.SmartDashboard.PutNumber('ultrasonic', self.ultrasonic.GetVoltage())
        wpilib.SmartDashboard.PutNumber('potentiometer', self.potentiometer.GetVoltage())
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

