
try:
    import wpilib
except ImportError:
    from pyfrc import wpilib
    
# import components here
from components import drive

class MyRobot(wpilib.SimpleRobot):

    def __init__ (self):
        super().__init__()        
        
        #
        # Initialize wpilib objects here
        #
        
        #lr is left rear lf is left front ect.
        self.potentiometer=wpilib.AnalogChannel(2)
        self.lr_motor = wpilib.Jaguar(1)
        self.rr_motor = wpilib.Jaguar(2)
        self.lf_motor = wpilib.Jaguar(3)
        self.rf_motor = wpilib.Jaguar(4)
        
        #add in port numbers
        self.intakeMotor=wpilib.Jaguar()
        self.intakeSolenoid=wpilib.Solenoid()
        self.joystick=wpilib.Joystick()
        
        self.catapultjaguar=wpilib.Jaguar()
        self.catapultsolenoid=wpilib.Solenoid()
        self.catapultOptics=wpilib.AnalogChannel()
        self.catapultTimer=wpilib.Timer()
        
        
        self.robot_drive = wpilib.RobotDrive(self.lr_motor, self.rr_motor, self.lf_motor, self.rf_motor)
        
        #
        # Initialize robot components here
        #
        catapult = components.catapult()
        intake = components.intake()
        drive = components.drive()
        
        self.catapult=catapult.Catapult(self.catapultjaguar,self.catapultsolenoid,self.potentiometer,self.catapultTimer)
        
        self.intakeTimer=wpilib.Timer
        self.drive = drive.Drive(self.robot_drive)
        self.intake=intake.intake(self.intakeMotor,self.intakeSolenoid,self.intakeTimer)
def OperatorControl(self):
        while self.IsOperatorControl()and self.IsEnabled():
            intakedirection=0
            solenoidDown=False
            if self.joystick.GetButton(1) is True:
                intakedirection=1
                solenoidDown=True
            elif self.joystick.GetButton(2) is True:
                intakedirection=-1
                solenoidDown=True
            else:
                intakedirection=0
                solenoidDown=False
            self.intake.wheels(intakedirection)
            self.intake.arm(solenoidDown)
            self.intake.doit()
            
            
            
            
            wpilib.Wait(.02)            
def run():
    
    robot = MyRobot()
    robot.StartCompetition()
    
    return robot


if __name__ == '__main__':
    wpilib.run()

