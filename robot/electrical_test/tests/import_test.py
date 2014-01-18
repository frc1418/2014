#
# This is a py.test based testing system. Anything you can do with
# py.test, you can do with this too. There are a few magic parameters
# provided as fixtures that will allow your tests to access the robot
# code and stuff
#
#    robot - This is whatever is returned from the run function in robot.py
#    wpilib - This is the wpilib module
#


#
# Each of these functions is an individual test run by py.test. Global
# wpilib state is cleaned up between each test run, and a new robot
# object is created each time
#

def test_autonomous(robot, wpilib):
    
    wpilib.internal.enabled = True
    robot.Autonomous()


def test_disabled(robot):
    robot.Disabled()


def test_operator_control(robot, wpilib):
    
    class TestController(object):
        '''This object is only used for this test'''
    
        loop_count = 0
        
        stick_prev = 0
        
        def IsOperatorControl(self, tm):
            '''
                Continue operator control for 1000 control loops
                
                The idea is to change the joystick/other inputs, and see if the 
                robot motors/etc respond the way that we expect. 
                
                Keep in mind that when you set a value, the robot code does not
                see the value until after this function returns. So, when you
                use assert to check a motor value, you have to check to see that
                it matches the previous value that you set on the inputs, not the
                current value.
            '''
            self.loop_count += 1
            
            # motor value is equal to the previous value of the stick
            #assert robot.motor.value == self.stick_prev
            
            # set the stick value based on time
            #robot.lstick.y = (tm % 2.0) - 1.0
            #self.stick_prev = robot.lstick.y
            
            return not self.loop_count == 1000
    
    wpilib.internal.set_test_controller(TestController)
    wpilib.internal.enabled = True
    
    robot.OperatorControl()
    
    # do something like assert the motor == stick value

