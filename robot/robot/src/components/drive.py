
try:
	import wpilib
except ImportError:
	from pyfrc import wpilib

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
		
		self.angle_constant = .040
		self.gyro_enabled = True
		
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
		if (self.x<.8 and self.x > -.8):
			self.x = 0
		if self.y < .8 and self.y > -.8:
			self.y = 0
		
	def closePosition(self):
		'''returns true if the robot is in shooting range, false if it's not'''	
		volts = self.ultraSonic.GetAverageVoltage()
		if volts <= 1.75 and volts >= 1.5:
			return True
		else:
			return False
	
	def set_gyro_enabled(self, value):
		self.gyro_enabled = value
	
	def return_gyro_angle(self):
		return self.gyro.GetAngle()
	
	def reset_gyro_angle(self):
		self.gyro.Reset()

	
	def set_angle_constant(self, constant):
		'''Sets the constant that is used to determine the robot turning speed'''
		self.angle_constant = constant
	
	def angle_rotation(self, target_angle):
		'''
			Adjusts the robot so that it points at a particular angle. Returns True 
		    if the robot is near the target angle, False otherwise
		   
		    :param target_angle: Angle to point at, in degrees
		    
		    :returns: True if near angle, False otherwise
		'''
		
		if not self.gyro_enabled:
			return False
		
		angleOffset = target_angle - self.return_gyro_angle()
		
		if angleOffset < -1 or angleOffset > 1:
			self.rotation = angleOffset*self.angle_constant
			self.rotation = max(min(0.5, self.rotation), -0.5)
			
			return False
		
		return True
		
	
	#
	# Actually tells the motors to do something
	#
		
	def doit(self):
		''' actually does stuff'''
		self.robotDrive.MecanumDrive_Cartesian(self.y, self.x, self.rotation*-1)
		#print('x=%s, y=%s, r=%s ' % (self.x, self.y, self.rotation))
		

		# by default, the robot shouldn't move
		self.x = 0
		self.y = 0
		self.rotation = 0
	
