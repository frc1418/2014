
try:
    import wpilib
except ImportError:
    from pyfrc import wpilib
    
# import components here
from autonomous import AutonomousModeManager
from components import drive, intake, catapult

from common import delay

class MyRobot(wpilib.SimpleRobot):
    '''
        This is where it all starts
    '''
    
    
    def __init__ (self):
        '''
            Constructor. 
        '''
        
        super().__init__()
        
        print("Team 1418 robot code for 2014")
        
        #################################################################
        # THIS CODE IS SHARED BETWEEN THE MAIN ROBOT AND THE ELECTRICAL #
        # TEST CODE. WHEN CHANGING IT, CHANGE BOTH PLACES!              #
        #################################################################
        
       
        wpilib.SmartDashboard.init()
        
        
        # Joysticks
        
        self.joystick1 = wpilib.Joystick(1)
        self.joystick2 = wpilib.Joystick(2)
        
        # Motors
        
        self.lf_motor = wpilib.Jaguar(1)
        self.lr_motor = wpilib.Jaguar(2)
        self.rr_motor = wpilib.Jaguar(3)
        self.rf_motor = wpilib.Jaguar(4)
        
        self.winch_motor = wpilib.CANJaguar(5)
        self.intake_motor = wpilib.Jaguar(6)
        
        # Catapult gearbox control
        '''
        self.gearbox_in_solenoid = wpilib.Solenoid(1)
        self.gearbox_out_solenoid = wpilib.Solenoid(2)'''
        self.gearbox_solenoid=wpilib.DoubleSolenoid(1,2)
        # Arm up/down control
        self.vent_bottom_solenoid = wpilib.Solenoid(3)
        self.fill_bottom_solenoid = wpilib.Solenoid(4)
        self.fill_top_solenoid = wpilib.Solenoid(5)
        self.vent_top_solenoid = wpilib.Solenoid(6)
        self.pass_solenoid=wpilib.Solenoid(7)
        '''
        self.bottom_solenoid=wpilib.DoubleSolenoid(3,4)
        self.top_solenoid=wpilib.DoubleSolenoid(5,6)
        '''
        self.robot_drive = wpilib.RobotDrive(self.lr_motor, self.rr_motor, self.lf_motor, self.rf_motor)
        self.robot_drive.SetSafetyEnabled(False)
        
        self.robot_drive.SetInvertedMotor(wpilib.RobotDrive.kFrontLeftMotor, True)
        self.robot_drive.SetInvertedMotor(wpilib.RobotDrive.kRearLeftMotor, True)
        
        # Sensors
        
        
        self.gyro = wpilib.Gyro(1) #THIS IS AN ANALOG PORT
        self.infrared = wpilib.AnalogChannel(3)
        self.potentiometer = wpilib.AnalogChannel(4)
        self.ultrasonic_sensor = wpilib.AnalogChannel(6)
        self.accelerometer = wpilib.ADXL345_I2C(1, wpilib.ADXL345_I2C.kRange_2G)
        self.compressor = wpilib.Compressor(1,1)
        self.compressor.Start()
        
        
        #################################################################
        #                      END SHARED CODE                          #
        #################################################################
        
        #
        # Initialize robot components here
        #
        
        
        self.drive = drive.Drive(self.robot_drive, self.ultrasonic_sensor)

        self.pushTimer=wpilib.Timer()
        self.catapultTimer=wpilib.Timer()
        self.catapult=catapult.Catapult(self.winch_motor,self.gearbox_solenoid,self.pass_solenoid,self.potentiometer,self.infrared,self.catapultTimer, self.joystick1)
        
        self.intakeTimer=wpilib.Timer()
        self.intake=intake.Intake(self.vent_top_solenoid,self.fill_top_solenoid,self.fill_bottom_solenoid,self.vent_bottom_solenoid,self.intake_motor,self.intakeTimer)
        
        self.pulldowntoggle=False
        
        self.components = {
            'drive': self.drive,
            'catapult': self.catapult,
            'intake': self.intake                   
        }
        
        self.control_loop_wait_time = 0.025
        self.autonomous = AutonomousModeManager(self.components)
        
    
    def Autonomous(self):
        '''Called when the robot is in autonomous mode'''
        self.autonomous.run(self, self.control_loop_wait_time)
        
        
    def OperatorControl(self):
        '''Called when the robot is in Teleoperated mode'''
        
        dog = self.GetWatchdog()
        dog.SetExpiration(0.25)
        dog.SetEnabled(True)
        
        preciseDelay = delay.PreciseDelay(self.control_loop_wait_time)

        while self.IsOperatorControl()and self.IsEnabled():

            dog.Feed()
            
            #
            # Driving
            #
            
            self.drive.move(self.joystick1.GetX(), self.joystick1.GetY(), self.joystick2.GetX())
            
            #
            # Intake
            #
            
            if self.joystick1.GetRawButton(2):
                self.intake.armDown()
            
            if self.joystick1.GetRawButton(3):
                self.intake.armUp()
                
            if self.joystick1.GetRawButton(4):
                self.intake.ballIn()
                
            if self.joystick1.GetRawButton(5):
                self.intake.ballOut()
                
            #
            # Catapult
            #
            
            if self.joystick2.GetRawButton(1):
                self.catapult.pulldown()
                
            if self.joystick1.GetRawButton(1):
                self.catapult.launch()
            
            #
            # Other
            #
           
            self.sendToSmartDashboard()
            self.update()
            
            preciseDelay.wait()
            
        # Disable the watchdog at the end
        dog.SetEnabled(False)
            
    def update(self):
        '''This function calls all of the doit functions for each component'''
        for component in self.components.values():
            component.doit()
    
    def sendToSmartDashboard(self):
        '''Sends values to the SmartDashboard'''
        wpilib.SmartDashboard.PutNumber("ultrasonic",self.ultrasonic_sensor.GetVoltage())
        wpilib.SmartDashboard.PutNumber("potentiometer",self.potentiometer.GetVoltage())

                        
def run():
    '''
        When the robot starts, this is the very first function that
        gets called
        
        :returns: a new instance of the `MyRobot` class
    '''
    
    robot = MyRobot()
    robot.StartCompetition()
    
    return robot


if __name__ == '__main__':
    wpilib.run()

