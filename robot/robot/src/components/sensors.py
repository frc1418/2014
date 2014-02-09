
try:
    import wpilib
except ImportError:
    from pyfrc import wpilib
    




class sensors(object):
    def __init__ (self):
        
        
        self.gyro = wpilib.Gyro(1) #THIS IS AN ANALOG PORT
        self.infrared = wpilib.AnalogChannel(2)
        self.potentiometer = wpilib.AnalogChannel(3)
        self.ultrasonic_sensor = wpilib.AnalogChannel(4)
        self.accelerometer = wpilib.ADXL345_I2C(1, wpilib.ADXL345_I2C.kRange_2G)