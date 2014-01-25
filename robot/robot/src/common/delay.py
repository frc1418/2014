
try:
    import wpilib
except ImportError:
    import fake_wpilib as wpilib


class PreciseDelay(object):
    '''
        Used to synchronize a timing loop.
    
        Usage:
        
            delay = PreciseDelay(time_to_delay)
            
            while something:
                # do things here
                delay.wait()
                
        TODO: Does this add unwanted overhead?
    '''
    
    def __init__(self, delay_period):
        self.timer = wpilib.Timer()        
        self.delay_period = delay_period
        
        self.timer.Start()
        
    def wait(self):
        
        # we must *always* yield here, so other things can run
        wpilib.Wait(0.001)
        
        while not self.timer.HasPeriodPassed(self.delay_period):
            wpilib.Wait(0.001)
