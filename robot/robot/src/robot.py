
try:
    import wpilib
except ImportError:
    from pyfrc import wpilib
    
# import components here
from autonomous import AutonomousModeManager
from components import drive, intake, catapult

class MyRobot(wpilib.SimpleRobot):
    def __init__ (self):
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
        self.catapult=catapult.Catapult(self.winch_motor,self.gearbox_solenoid,self.pass_solenoid,self.potentiometer,self.infrared,self.catapultTimer)
        
        self.intakeTimer=wpilib.Timer()
        self.intake=intake.Intake(self.vent_top_solenoid,self.fill_top_solenoid,self.fill_bottom_solenoid,self.vent_bottom_solenoid,self.intake_motor,self.intakeTimer)
        
        self.pulldowntoggle=False
        
        self.components = {
            'drive': self.drive,
            'catapult': self.catapult,
            'intake': self.intake                   
        }
        
        self.control_loop_wait_time = 0.4
        self.autonomous = AutonomousModeManager(self.components)
        self.directiontoggleboo=False
        self.pulldowntoggleboo=False
        self.intakedirection=0
    def Autonomous(self):
        '''Called when the robot is in autonomous mode'''
        self.autonomous.run(self, self.control_loop_wait_time)
        
        
    def OperatorControl(self):

        while self.IsOperatorControl()and self.IsEnabled():
            self.drive.move(self.joystick1.GetX(), self.joystick1.GetY(), self.joystick2.GetX())
            potentiometer1=self.potentiometer.GetVoltage()
            launcherup=self.catapult.check_up()
            pushval=False

            #solenoidDown=0
            if self.joystick1.GetRawButton(1) is True:
                self.intake.armUp()
            elif self.joystick1.GetRawButton(2) is True:
                self.intake.armDown()
            else:
                self.intake.armNeutral()

            if self.joystick1.GetRawButton(3) is True:
                self.directiontoggleboo=True
            if self.directiontoggleboo==True and self.joystick1.GetRawButton(3) is False:
                if self.intakedirection is 0 or -1:
                    self.intakedirection=1
                elif intakedirection is 1:
                    self.intakedirection=-1
                self.directiontoggleboo=False
            if self.joystick1.GetRawButton(4) is True:
                self.intakedirection=0
                
            if self.joystick1.GetRawButton(5) is True:
                self.catapult.check_ready()
                self.catapult.launchNoSensor()
                
            if self.joystick1.GetRawButton(6) is True:
                self.pulldowntoggleboo=True
            if self.pulldowntoggleboo is True and self.joystick1.GetRawButton(6) is False:
                self.pulldowntoggleboo=False
                if self.pulldowntoggle is False:
                    self.pulldowntoggle=True
                elif self.pulldowntoggle is True:
                    self.pulldowntoggle=False
            if self.joystick1.GetRawButton(7) is True:
                self.catapult.passBall()
            
            if self.pulldowntoggle is True:
                print("pulling down")
                #self.catapult.pulldown(potentiometer1)
                self.catapult.pulldownNoSensor()
            #self.intake.wheels(intakedirection,launcherup)
            else:
                pass
            self.smartdashboard()
            self.update()
            wpilib.Wait(self.control_loop_wait_time)
            
    def update(self):
        '''This function calls all of the doit functions for each component'''
        for component in self.components.values():
            component.doit()
    def smartdashboard(self):
        wpilib.SmartDashboard.PutNumber("ultrasonic",self.ultrasonic_sensor.GetVoltage())

                        
def run():
    
    robot = MyRobot()
    robot.StartCompetition()
    
    return robot


if __name__ == '__main__':
    wpilib.run()

