
class Drive(object):
	'''
		The sole interaction between the robot and its driving system
		occurs here. Anything that wants to drive the robot must go
		through this class.
	'''

	def __init__(self, robotDrive, analog_channel):
		'''
			Constructor. 
			
			:param robotDrive: a `wpilib.RobotDrive` object
		'''
		
		# set defaults here
		self.ultraSonic = analog_channel
		self.x = 0
		self.y = 0
		self.rotation = 0
		
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
		if self.ultraSonic.GetVoltage()<=.9 and self.ultraSonic.GetVoltage()>=.6:
			return True
		else:
			return False
	
	#
	# Actually tells the motors to do something
	#
	
	
	def doit(self):
''' actually does stuff'''
		self.robotDrive.MecanumDrive_Cartesian(self.y, self.x, self.rotation*-1)
		print('x=%s, y=%s, r=%s ' % (self.x, self.y, self.rotation))
		

		# by default, the robot shouldn't move
		self.x = 0
		self.y = 0
		self.rotation = 0
	
		
