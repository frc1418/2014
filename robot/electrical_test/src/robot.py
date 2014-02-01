
try:
    import wpilib
except ImportError:
    from pyfrc import wpilib


class MyRobot(wpilib.SimpleRobot):
   
    def __init__ (self):
        super().__init__()
        
   
        
        print("Electrical Cim Test")
        #self.digitalInput=wpilib.DigitalInput(4)
        wpilib.SmartDashboard.init()
        self.joystick=wpilib.Joystick(1)
        self.joystick2=wpilib.Joystick(2)
        self.Timer=wpilib.Timer()
        self.LF_motor=wpilib.Jaguar(1)
        self.LR_motor=wpilib.Jaguar(2)
        self.RR_motor=wpilib.Jaguar(3)
        self.RF_motor=wpilib.Jaguar(4)
        self.winch=wpilib.CANJaguar(5)
        self.intake=wpilib.Jaguar(6)
        self.solenoid_intake_up=wpilib.Solenoid(1)
        self.solenoid_intake_down=wpilib.Solenoid(2)
        self.solenoid_release_release=wpilib.Solenoid(3)
        self.solenoid_release_engage=wpilib.Solenoid(4)
        self.solenoid_kicker_out=wpilib.Solenoid(5)
        self.solenoid_kicker_in=wpilib.Solenoid(6)
        self.drive = wpilib.RobotDrive(self.LR_motor, self.RR_motor, self.LF_motor, self.RF_motor)#self.jaguar4=wpilib.Jaguar(4)
        self.gyro = wpilib.Gyro(1)
        self.ultrasonic=wpilib.AnalogChannel(2)
        self.potentiometer=wpilib.AnalogChannel(3)
        self.accelerometer=wpilib.ADXL345_I2C(1, wpilib.ADXL345_I2C.kRange_2G)
        self.drive.SetSafetyEnabled(False)
    
   
    def OperatorControl(self):
       # print(self.IsEnabled())
       # dog = wpilib.GetWatchdog()
        #dog.setEnabled(True)
        #dog.SetExpiration(10)
        
        while self.IsOperatorControl()and self.IsEnabled():
            #  dog.Feed()
            #Driving
            self.drive.MecanumDrive_Cartesian(self.joystick.GetY(), self.joystick.GetX(), self.joystick2.GetX(), 0)
            self.Intake()
            self.Catapult()
            self.Solenoids()
            self.SmartDash()
            wpilib.Wait(0.01)
   
            
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

