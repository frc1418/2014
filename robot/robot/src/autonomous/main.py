
try:
    import wpilib
except ImportError:
    from pyfrc import wpilib
    
# import components here
from components import drive, intake, catapult

class MyRobot(wpilib.SimpleRobot):
    def __init__ (self):
        super().__init__()
        
        print("Team 1418 robot code for 2014")
        
        #################################################################
        # THIS CODE IS SHARED BETWEEN THE MAIN ROBOT AND THE ELECTRICAL #
        # TEST CODE. WHEN CHANGING IT, CHANGE BOTH PLACES!              #
        #################################################################
        
        wpilib.SmartDashboard.init()