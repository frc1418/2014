
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
        self.Joystick=wpilib.Joystick(1)
        self.Joystick2=wpilib.Joystick(2)
        self.Timer=wpilib.Timer()
        self.jaguar=wpilib.Jaguar(1)
        self.jaguar2=wpilib.CANJaguar(2)
        self.jaguar3=wpilib.CANJaguar(3)
        self.jaguar4=wpilib.CANJaguar(4)
        self.drive = wpilib.RobotDrive(self.jaguar, self.jaguar2, self.jaguar3, self.jaguar4)#self.jaguar4=wpilib.Jaguar(4)
        self.drive.SetSafetyEnabled(False)
        

    def OperatorControl(self):
        print(self.IsEnabled())
        
       # dog = wpilib.GetWatchdog()
        #dog.setEnabled(True)
        #dog.SetExpiration(10)
        
        while self.IsOperatorControl():  
          #  dog.Feed()
            #self.drive.MecanumDrive_Cartesian(self.Joystick.GetY(), self.Joystick.GetX(), self.Joystick2.GetX(), 0)
            
            self.gyro.GetAngle()
            wpilib.Wait(0.01)
            wpilib.SmartDashboard.PutNumber('GyroAngle', self.gyro.GetAngle())
            
            
        
def run():
    
    robot = MyRobot()
    robot.StartCompetition()
    
    return robot


if __name__ == '__main__':
    wpilib.run()

