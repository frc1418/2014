
try:
    import wpilib
except ImportError:
    from pyfrc import wpilib


class MyRobot(wpilib.SimpleRobot):
    state = 1
    def __init__ (self):
        super().__init__()
   
        print("Tim Winters")
        
        #self.digitalInput=wpilib.DigitalInput(4)
        self.Joystick=wpilib.Joystick(1)
        self.Joystick2=wpilib.Joystick(2)
        self.Timer=wpilib.Timer()
        self.jaguar=wpilib.Jaguar(1)
        self.jaguar2=wpilib.Jaguar(2)
        self.jaguar3=wpilib.Jaguar(3)
        self.jaguar4=wpilib.Jaguar(4)
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
            
    def move_motor(self):
       # print(self.state, self.Timer.Get(), self.digitalInput.Get())
        '''if self.state is 1:
            self.Timer.Reset()
            self.jaguar.Set(self.Joystick.GetY())
            if self.digitalInput.Get()==True:
                self.Timer.Reset()
                self.state =  2
            
        elif self.state is 2:  
            self.jaguar.Set(self.Joystick.GetY())
            if self.Timer.HasPeriodPassed(1):
                self.state = 3
            if not self.digitalInput.Get():
                self.state=1
        elif self.state is 3:
            self.jaguar.Set(1)
            if self.Timer.HasPeriodPassed(3):
                self.state = 4
        elif self.state is 4:
             self.jaguar.Set(-1)
             if(self.Timer.HasPeriodPassed(2)):
                 self.state=1   
        '''
        
def run():
    
    robot = MyRobot()
    robot.StartCompetition()
    
    return robot


if __name__ == '__main__':
    wpilib.run()

