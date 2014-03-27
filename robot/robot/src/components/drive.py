
class Drive(object):
	'''
		The sole interaction between the robot and its driving system
		occurs here. Anything that wants to drive the robot must go
		through this class.
	'''

	def __init__(self, robotDrive, analog_channel,gyro):
		'''
			Constructor. 
			
			:param robotDrive: a `wpilib.RobotDrive` object
		'''
		
		# set defaults here
		self.ultraSonic = analog_channel
		self.x = 0
		self.y = 0
		self.rotation = 0
		self.gyro=gyro
		
		self.robotDrive = robotDrive
		

	#
	# Verb functions -- these functions do NOT talk to motors directly. This
	# allows multiple callers in the loop to call our functions without 
	# conflicts.
	#

	def move(self, x, y, rotation):
		'''
			Causes the robot to move
		
			:param x: The speed that the robot should drive in the X direction. 1 is right [-1.0..1.0] 
			:param y: The speed that the robot should drive in the Y direction. -1 is forward. [-1.0..1.0] 
			:param rotation:  The rate of rotation for the robot that is completely independent of the translation. 1 is rotate to the right [-1.0..1.0]
		'''
		
		self.x = x
		self.y = y
		self.rotation = rotation
		
	def closePosition(self):
		'''returns true if the robot is in shooting range, false if it's not'''	
		volts = self.ultraSonic.GetAverageVoltage()
		if volts <= 1.75 and volts >= 1.5:
			return True
		else:
			return False
	
	#
	# Actually tells the motors to do something
	#
	def return_gyro_angle(self):
		return self.gyro.GetAngle()
	def reset_gyro_angle(self):
		self.gyro.Reset()
	def calculate_rotate(self,degreesToSpin):
        #this function is to calculate length of time
        #the robot needs to rotate once
        #it gets back to position to get the 
        #second ball
        
        #not yet completed
		if degreesToSpin >0 and degreesToSpin<180:
			pass
		elif degreesToSpin>=180 and degreesToSpin<360:
			degreesToSpin=360-degreesToSpin
		else:
			pass
		fullSpinTime=2.0
		degreesPerSecond=360.0/fullSpinTime
		secondsToSpin=degreesToSpin/degreesPerSecond

	
	def angle_rotation(self, newDegree):
		oldDegree = self.return_gyro_angle()
		degreesTospin = newDegree-oldDegree
		constant = .00055555555555
		motorValue = degreesToSpin*constant
		if degreesTospin > 0:
			while(self.return_gyro_angle()<(newDegree-1)):
			    self.drive.move(0,0,motorValue)
		if degreesTospin <0:
			while(self.return_gyro_angle()>(newDegree+1)):
				self.drive.move(0,0,-1*motorValue)
				
		
	def doit(self):
		''' actually does stuff'''
		self.robotDrive.MecanumDrive_Cartesian(self.y, self.x, self.rotation*-1)
		#print('x=%s, y=%s, r=%s ' % (self.x, self.y, self.rotation))
		

		# by default, the robot shouldn't move
		self.x = 0
		self.y = 0
		self.rotation = 0
	
