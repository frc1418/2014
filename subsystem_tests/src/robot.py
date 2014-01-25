
try:
    import wpilib
except ImportError:
    from pyfrc import wpilib


class MyRobot(wpilib.SimpleRobot):
    state = 1
    def __init__ (self):
        super().__init__()
   
        print("Matt the fantastic ultimate wonderful humble person")
        wpilib.SmartDashboard.init()
        #self.digitalInput=wpilib.DigitalInput(4)
        self.CANJaguar = wpilib.CANJaguar(1)
        self.gyro = wpilib.Gyro(1)
        self.joystick=wpilib.Joystick(1)
        self.joystick2=wpilib.Joystick(2)
        self.jaguar=wpilib.Jaguar(1)
        self.accelerometer=wpilib.ADXL345_I2C(1, wpilib.ADXL345_I2C.kRange_2G)
        self.solenoid=wpilib.Solenoid(7)
        self.solenoid2=wpilib.Solenoid(8)
        self.p=1
        self.i=0
        self.d=0
        wpilib.SmartDashboard.PutBoolean('Soleinoid 1', False)
        wpilib.SmartDashboard.PutBoolean('Soleinoid 2', False)
        #self.pid = wpilib.PIDController(self.p, self.i, self.d, self.gyro, self.jaguar)
        self.sensor = wpilib.AnalogChannel(5)
        self.ballthere = False
        
        #self.jaguar2=wpilib.Jaguar(2)
        #self.jaguar3=wpilib.Jaguar(3)
        #self.jaguar4=wpilib.Jaguar(4)
        #self.drive = wpilib.RobotDrive(self.jaguar, self.jaguar2, self.jaguar3, self.jaguar4)#self.jaguar4=wpilib.Jaguar(4)
        #self.drive.SetSafetyEnabled(False)
        

    def OperatorControl(self):
        #yself.pid.Enable()
        print("MyRobot::OperatorControl()")
        
        wpilib.GetWatchdog().SetEnabled(False)
        
        #dog = wpilib.GetWatchdog()
        #dog.setEnabled(True)
        #dog.SetExpiration(10)
        
        while self.IsOperatorControl() and self.IsEnabled():  
            #dog.Feed()
            #self.drive.MecanumDrive_Cartesian(self.Joystick.GetY(), self.Joystick.GetX(), self.Joystick2.GetX(), 0)
            self.FromOperatorControl()
            
            
            wpilib.Wait(0.01)
            
    def FromOperatorControl(self):
        self.CANJaguar.Set((self.joystick.GetY()))
            
    def PIDMove(self):
        self.pid.SetSetpoint(10)
   
   # def SmartDashboard(self):
        #axis=self.accelerometer.GetAccelerations()
        #wpilib.SmartDashboard.PutNumber('GyroAngle', self.gyro.GetAngle())
        #wpilib.SmartDashboard.PutNumber('Acceleration Axis X', axis.XAxis)
        #wpilib.SmartDashboard.PutNumber('Acceleration Axis Y', axis.YAxis)
        #wpilib.SmartDashboard.PutNumber('Acceleration Axis Z', axis.ZAxis)
        #wpilib.SmartDashboard.PutNumber('the getVoltage', self.sensor.GetVoltage())
        #wpilib.SmartDashboard.PutNumber('boolean ballthere', self.ballthere)
        #wpilib.SmartDashboard.PutNumber('soleinoid 1', self.solenoid.Get())
        #wpilib.SmartDashboard.PutNumber('soleinoid 2', self.solenoid2.Get())
        #self.solenoid.Set(wpilib.SmartDashboard.GetBoolean('Soleinoid 1'))
        #self.solenoid2.Set(wpilib.SmartDashboard.GetBoolean('Soleinoid 2'))
            #self.PIDMove()
        #self.OpticalThingy()
            
    def OpticalThingy(self):
        if self.sensor.GetVoltage()>1:
            self.ballthere=True
        if self.sensor.GetVoltage()<1:
            self.ballthere=False
        
        
        
        
        
        
            
def run():
    
    robot = MyRobot()
    robot.StartCompetition()
    
    return robot


if __name__ == '__main__':
    wpilib.run()

