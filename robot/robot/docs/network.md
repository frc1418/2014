## Variables 

#### Sent From Driver Station

	- FirePower:
		Type: Integer (0-100)
		Description:
			A number from 0 to 100 that dictates the power with which
			the winch is to fire. This is related to partially pulling
			back the winch and may or may not be implemented
			
	- ArmSet:
		Type: Integer (1-3, 0 when not used)
		Description:
			A number from 1 to 3 that dictates the state that the arm
			should be moved to:
				1 - Arm down and locked
				2 - Arm unlocked
				3 - Arm up and locked
			This variable MUST be set to 0 after the arm's state has
			been updated


#### Sent From Robot Code

	- Distance:
		Type: Double (0.00 to 255.00)
		Description:
			A number from 0 to 255 that reflects the ultrasonic
			sensors readout
			
	- Battery:
		Type: Double (0.00 to 15.00)
		Description:
			A number from 0 to 15 that reflects the voltage of the
			battery
	
	- ShootAngle:
		Type: Integer (0 to 100)
		Description:
			A number from 0 to 100 that reflects the scaled reading
			from the potentiometer	
	
	- ArmState:
		Type: Integer (1-3)
		Description:
			A number from 1 to 3 that dictates the state that the arm
			should be moved to:
				1 - Arm down and locked
				2 - Arm unlocked
				3 - Arm up and locked
			This variable MUST ALWAYS reflect the current state the
			arm is in
			
	- BallLoaded:
		Type: Boolean (True, False)
		Description:
			A boolean that tells whether the ball is in the shooter
			or not
			
			
	- RobotMode:
		Type: number (0-2)
		0 is disabled
		1 is teleoperated
		2 is autonomus
