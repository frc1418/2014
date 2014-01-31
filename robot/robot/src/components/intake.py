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
        
        solenoid=self.solenoid 
        winch=self.winch
        joystick=self.joystick        
        tempsolenoid=False
    #wheels function pulls in the ball and also spits the the ball out
    def wheels(self):
        x = self.joystick.GetTrigger()
        y = self.Joystick.GetRawButton(7)
        if x==True:
            self.arm(1)
            self.jaguar = 1
        else:
            self.jaguar = 0
        if y:
            self.jaguar = -1
    #arm controls the arm on the robot; trigger makes arm fall
    def arm(self, x):
        if x == 1:
            self.solenoid = True    
        else:
            self.solenoid = False 
    
    '''def doit(self):
         self.wheel()
         self.arm()
    '''