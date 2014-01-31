
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
        self.lr_motor = wpilib.Jaguar(1)
        self.rr_motor = wpilib.Jaguar(2)
        self.lf_motor = wpilib.Jaguar(3)
        self.rf_motor = wpilib.Jaguar(4)
        
        self.robot_drive = wpilib.RobotDrive(self.lr_motor, self.rr_motor, self.lf_motor, self.rf_motor)
        
        #
        # Initialize robot components here
        #
        catapult = components.catapult()
        intake = components.intake()
        drive = components.drive()
        
        self.drive = drive.Drive(self.robot_drive)
        while self.IsOperatorControl()and self.IsEnabled():
            self.catapult()
            self.intake()
            
        
        
        
            
def run():
    
    robot = MyRobot()
    robot.StartCompetition()
    
    return robot


if __name__ == '__main__':
    wpilib.run()

