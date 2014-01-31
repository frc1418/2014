'''
Created on Jan 25, 2014

@author: Owner
'''
try:
    import wpilib
except ImportError:
    from pyfrc import wpilib
    
class intake(object):
    def __init__ (self):
        super().__init__()
        self.jaguar = wpilib.Jaguar(6)
        self.solenoid = wpilib.Solenoid(1)
        self.winch=wpilib.CANJaguar(5)
        self.joystick=wpilib.Joystick(1)
        
        
    #wheels function pulls in the ball and also spits the the ball out
    def wheels(self):
        x = self.joystick.GetTrigger()
        y = self.Joystick.GetRawButton(7)
        if x==True:
            self.arm()
            self.jaguar = 1
        else:
            self.jaguar = 0
        if y:
            self.jaguar = -1
    #arm controls the arm on the robot; uses the pnumatics 
    def arm(self):
        if self.up == 1:
            self.solenoid = True    
        else:
            self.solenoid = False 
    
    '''def doit(self):
         self.wheel()
         self.arm()
    '''    
                
             
            
        
        
        