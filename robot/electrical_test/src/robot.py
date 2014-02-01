
try:
    import wpilib
except ImportError:
    from pyfrc import wpilib


class MyRobot(wpilib.SimpleRobot):
   
    def __init__ (self):
        super().__init__()
        
   
        
        print("Electrical Cim Test")
        #self.digitalInput=wpilib.DigitalInput(4)
        self.Joystick=wpilib.Joystick(1)
        self.Joystick2=wpilib.Joystick(2)
        self.Timer=wpilib.Timer()
        self.LF_motor=wpilib.Jaguar(1)
        self.LR_motor=wpilib.Jaguar(2)
        self.RR_motor=wpilib.Jaguar(3)
        self.RF_motor=wpilib.Jaguar(4)
        self.winch=wpilib.CANJaguar(5)
        self.intake=wpilib.Jaguar(6)
        self.drive = wpilib.RobotDrive(self.LR_motor, self.RR_motor, self.LF_motor, self.RF_motor)#self.jaguar4=wpilib.Jaguar(4)
    
        self.drive.SetSafetyEnabled(False)
    
   
    def OperatorControl(self):
       # print(self.IsEnabled())
       # dog = wpilib.GetWatchdog()
        #dog.setEnabled(True)
        #dog.SetExpiration(10)
        
        while self.IsOperatorControl()and self.IsEnabled():
            #  dog.Feed()
            #Driving
            self.drive.MecanumDrive_Cartesian(self.Joystick.GetY(), self.Joystick.GetX(), self.Joystick2.GetX(), 0)
            self.Intake()
            self.Catapult()
            wpilib.Wait(0.01)
   
            
    def Intake(self):
        #Use joystick to contol the intake 
        x = self.Joystick.GetRawButton(4)
        y = self.Joystick.GetRawButton(5)
        if x:
            self.intake.Set(-1)
        elif y:
            self.intake.Set(1)    
        else:
            self.intake.Set(0) 
            
    def Catapult(self):
        self.winch.Set(self.Joystick.GetZ())
        
def run():
    
    robot = MyRobot()
    robot.StartCompetition()
    
    return robot


if __name__ == '__main__':
    wpilib.run()

