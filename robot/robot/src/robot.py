
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
        
        self.lr_motor = wpilib.Jaguar(1)
        self.rr_motor = wpilib.Jaguar(2)
        self.lf_motor = wpilib.Jaguar(3)
        self.rf_motor = wpilib.Jaguar(4)
        
        self.robot_drive = wpilib.RobotDrive(self.lr_motor, self.rr_motor, self.lf_motor, self.rf_motor)
        
        #
        # Initialize robot components here
        #
        
        self.drive = drive.Drive(self.robot_drive)
        
        
        
        
            
def run():
    
    robot = MyRobot()
    robot.StartCompetition()
    
    return robot


if __name__ == '__main__':
    wpilib.run()

