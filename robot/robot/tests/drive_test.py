
def test_drive_initial(robot):
    
    # make sure that calling doit works without ever calling one of the
    # verb functions
    robot.drive.doit()
    
    assert robot.lf_motor.value == 0
    assert robot.lr_motor.value == 0
    assert robot.rf_motor.value == 0
    assert robot.rr_motor.value == 0


def test_drive_reset(robot):
    
    # retrieve your object from the MyRobot object
    drive = robot.drive
    
    # call all of the functions to see if they work
    drive.move(1,1,0)
    
    drive.doit()
    
    # you can access the wpilib objects to see if the results are
    # what you expected
    assert robot.lf_motor.value != 0
    assert robot.lr_motor.value != 0
    assert robot.rf_motor.value != 0
    assert robot.rr_motor.value != 0
    
    # now we test to see if the motor values reset to the defaults
    # if we don't call move
    drive.doit()
    
    assert robot.lf_motor.value == 0
    assert robot.lr_motor.value == 0
    assert robot.rf_motor.value == 0
    assert robot.rr_motor.value == 0
    
    
    # obviously other components are going to need more complex tests..
