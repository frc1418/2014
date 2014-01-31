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
        
    #move the wheels on the arm/intake
    def move(self,x):
        self.x=x
        if self.goin==True:
            self.jaguar = 1
        if self.goOut==False:
            self.jaguar= -1
    
    def arm(self):
        if self.up ==True:
            self.solenoid = True    
        else:
            self.solenoid = False 
    def doit(self):
        pass   
                
             
            
        
        
            