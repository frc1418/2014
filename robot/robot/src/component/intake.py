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
    def move(self):
            