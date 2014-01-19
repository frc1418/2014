
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
        
        #self.jaguar=wpilib.Jaguar(1)
        #self.jaguar2=wpilib.Jaguar(2)
        #self.jaguar3=wpilib.Jaguar(3)
        #self.jaguar4=wpilib.Jaguar(4)
        #self.drive = wpilib.RobotDrive(self.jaguar, self.jaguar2, self.jaguar3, self.jaguar4)#self.jaguar4=wpilib.Jaguar(4)
        #self.drive.SetSafetyEnabled(False)
        

    def OperatorControl(self):
        
        print("MyRobot::OperatorControl()")
        
        wpilib.GetWatchdog().SetEnabled(False)
        
       # dog = wpilib.GetWatchdog()
        #dog.setEnabled(True)
        #dog.SetExpiration(10)
        
        while self.IsOperatorControl() and self.IsEnabled():  
          #  dog.Feed()
            #self.drive.MecanumDrive_Cartesian(self.Joystick.GetY(), self.Joystick.GetX(), self.Joystick2.GetX(), 0)
            
            wpilib.SmartDashboard.PutNumber('GyroAngle', self.gyro.GetAngle())
            
            wpilib.Wait(0.01)
            
            
        
def run():
    
    robot = MyRobot()
    robot.StartCompetition()
    
    return robot


if __name__ == '__main__':
    wpilib.run()

