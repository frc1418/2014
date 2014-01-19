from pyfrc.wpilib._wpilib._pid_controller import PIDController

try:
    import wpilib
except ImportError:
    from pyfrc import wpilib


class MyRobot(wpilib.SimpleRobot):
    state = 1
    def __init__ (self):
        super().__init__()
   
        print("Matt the fantastic ultimate wonderful humble person")
        
        #self.digitalInput=wpilib.DigitalInput(4)
        self.gyro = wpilib.Gyro(1)
        self.joystick=wpilib.Joystick(1)
        self.joystick2=wpilib.Joystick(2)
        self.jaguar=wpilib.Jaguar(1)
        self.accelerometer=wpilib.ADXL345_I2C(1, wpilib.ADXL345_I2C.kRange_2G)
        self.p=1
        self.i=0
        self.d=0
        self.pid = wpilib.PIDController(p, i, d, self.gyro, self.jaguar)
        
        #self.jaguar2=wpilib.Jaguar(2)
        #self.jaguar3=wpilib.Jaguar(3)
        #self.jaguar4=wpilib.Jaguar(4)
        #self.drive = wpilib.RobotDrive(self.jaguar, self.jaguar2, self.jaguar3, self.jaguar4)#self.jaguar4=wpilib.Jaguar(4)
        #self.drive.SetSafetyEnabled(False)
        

    def OperatorControl(self):
        self.pid.Enable()
        print("MyRobot::OperatorControl()")
        
        wpilib.GetWatchdog().SetEnabled(False)
        
        #dog = wpilib.GetWatchdog()
        #dog.setEnabled(True)
        #dog.SetExpiration(10)
        
        while self.IsOperatorControl() and self.IsEnabled():  
            #dog.Feed()
            #self.drive.MecanumDrive_Cartesian(self.Joystick.GetY(), self.Joystick.GetX(), self.Joystick2.GetX(), 0)
            
            wpilib.SmartDashboard.PutNumber('GyroAngle', self.gyro.GetAngle())
            axis=self.accelerometer.GetAccelerations()
            wpilib.SmartDashboard.PutNumber('Acceleration Axis X', axis.XAxis)
            wpilib.SmartDashboard.PutNumber('Acceleration Axis Y', axis.YAxis)
            wpilib.SmartDashboard.PutNumber('Acceleration Axis Z', axis.ZAxis)
            
            wpilib.SmartDashboard.GetNumber('')
            self.PIDMove()
            
            wpilib.Wait(0.01)
            
            
    def PIDMove(self):
        self.pid.SetSetpoint(10)
        
        
        
        
        
        
            
def run():
    
    robot = MyRobot()
    robot.StartCompetition()
    
    return robot


if __name__ == '__main__':
    wpilib.run()

