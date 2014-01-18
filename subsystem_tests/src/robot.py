
try:
    import wpilib
except ImportError:
    from pyfrc import wpilib


class MyRobot(wpilib.SimpleRobot):
    state = 1
    def __init__ (self):
        super().__init__()
   
        print("Tim Winters II")
        
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
    
    challenge= 1

    def OperatorControl(self):
        print(self.IsEnabled())
        
       # dog = wpilib.GetWatchdog()
        #dog.setEnabled(True)
        #dog.SetExpiration(10)
        
        while self.IsOperatorControl()and self.IsEnabled():  
          #  dog.Feed()
            self.drive.MecanumDrive_Cartesian(self.Joystick.GetY(), self.Joystick.GetX(), self.Joystick2.GetX(), 0)
            wpilib.Wait(0.01)
            
        
def run():
    
    robot = MyRobot()
    robot.StartCompetition()
    
    return robot


if __name__ == '__main__':
    wpilib.run()

