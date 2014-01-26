try:
    import wpilib
except ImportError:
    from pyfrc import wpilib

''' Implementation of a complementary angle filter. This combines the gyro (low pass filter) and the accelerometer (high pass filter)
    to make a constant reading over time '''
    
class ComplementaryFilter():
    
    self.timer = wpilib.Timer
    self.lastTime = 0
    self.prevAngle = 0
    self.timeConstant = 1.75
        
    
    def __init__(self):
        self.timer.Start()
        
    def filterAngle(self, gyroAngle, accelRate):
        if(self.lastTime == 0):
            self.lastTime = self.timer.Get()
        
        currentTime = self.timer.Get()
        dt = currentTime - self.lastTime
        
        filterTerm0 = (angle-self.prevAngle) * self.timeConstant * self.timeConstant
        filterTerm2 = filterTerm0 * dt
        filterTerm1 = filterTerm2 + ((angle-self.prevAngle) * 2 * self.timeConstant) + accelRate
        filteredAngle = (filterTerm1 * dt) + prevAngle
        
        self.lastTime = currentTime
        
        return filteredAngle