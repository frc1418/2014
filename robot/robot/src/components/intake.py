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
        self.jaguar = wpilib.Jaguar(1)
        self.solenoid = wpilib.Solenoid(1)
    def move(self,x, y):
        self.x = x
        self.y = y
        if self.goin==True:
           
        if self.goOut==False:
            self.jaguar=-1
    def arm(self):
        if self.up = true;
        self.solenoid     
    def doit(self):
        self     
                
             
            
        
        
            