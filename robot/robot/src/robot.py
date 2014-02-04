
try:
    import wpilib
except ImportError:
    from pyfrc import wpilib
    
# import components here
from components import drive, intake, catapult

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
        self.intakeMotor=wpilib.Jaguar(6)
        self.intakeSolenoid=wpilib.Solenoid(1)
        self.joystick=wpilib.Joystick(1)
        
        self.catapultjaguar=wpilib.CANJaguar(5)
        self.catapultsolenoid=wpilib.Solenoid(2)
        self.catapultOptics=wpilib.AnalogChannel(1)
        self.catapultTimer=wpilib.Timer()
        
        
        self.robot_drive = wpilib.RobotDrive(self.lr_motor, self.rr_motor, self.lf_motor, self.rf_motor)
        
        #
        # Initialize robot components here
        #

        
        self.catapult=catapult.Catapult(self.catapultjaguar,self.catapultsolenoid,self.potentiometer,self.catapultOptics,self.catapultTimer)
        
        self.intakeTimer=wpilib.Timer
        self.drive = drive.Drive(self.robot_drive)
        self.intake=intake.Intake(self.intakeMotor,self.intakeSolenoid,self.intakeTimer)
        
    def OperatorControl(self):
        while self.IsOperatorControl()and self.IsEnabled():
            potentiometer1=self.potentiometer.GetVoltage()
            launcherup=self.catapult.check_up()
            intakedirection=0
            solenoidDown=False
            if self.joystick.GetRawButton(1) is True:
                intakedirection=1
                solenoidDown=True
            elif self.joystick.GetRawButton(2) is True:
                intakedirection=-1
                solenoidDown=True
            elif self.joystick.GetRawButton(3) is True:
                self.catapult.launch(potentiometer1)
                print(potentiometer1)
            else:
                intakedirection=0
                solenoidDown=False
            
            self.intake.wheels(intakedirection,launcherup)
            self.intake.arm(solenoidDown)
            self.intake.doit()
            self.catapult.pulldown(potentiometer1)
            self.catapult.check_ready(self.catapultOptics.GetVoltage())
            
           
            self.catapult.doit()
            wpilib.Wait(.02)            
def run():
    
    robot = MyRobot()
    robot.StartCompetition()
    
    return robot


if __name__ == '__main__':
    wpilib.run()

