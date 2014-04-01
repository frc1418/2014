'''
    Runs all of the autonomous modes in a basic way
'''


def test_all_autonomous(robot, wpilib, fake_time):

    autonomous_chooser = wpilib.SmartDashboard._table.data['Autonomous Mode']
    
    auto_tm = 10
    tm_limit = auto_tm

    for choice in autonomous_chooser.choices.keys():

        # set the mode
        autonomous_chooser.selected = choice
    
        # run autonomous mode for 10 seconds
        wpilib.internal.enabled = True
        wpilib.internal.on_IsAutonomous = lambda tm: tm < tm_limit
        
        robot.Autonomous()
        
        # make sure autonomous mode ran for the entire time, and 
        # didn't exit early
        assert int(fake_time.Get()) == tm_limit

        tm_limit += auto_tm
