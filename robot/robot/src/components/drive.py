
class Drive(object):
	'''
		The sole interaction between the robot and its driving system
		occurs here. Anything that wants to drive the robot must go
		through this class.
	'''

	def __init__(self, robotDrive):
		'''
			Constructor. 
			
			:param robotDrive: a `wpilib.RobotDrive` object
		'''
		
		# set defaults here
		self.magnitude = 0
		self.direction = 0
		self.rotation = 0
		
		self.robotDrive = robotDrive
		

	#
	# Verb functions -- these functions do NOT talk to motors directly. This
	# allows multiple callers in the loop to call our functions without 
	# conflicts.
	#

	def move(self, magnitude, direction, rotation):
		'''
			Causes the robot to move
		
			:param magnitude: The speed that the robot should drive in a given direction. [-1.0..1.0] 
			:param direction: The direction the robot should drive in degrees. The direction and magnitude are independent of the rotation rate. 
			:param rotation:  The rate of rotation for the robot that is completely independent of the magnitude or direction. [-1.0..1.0]
		'''
		
		self.magnitude = magnitude
		self.direction = direction
		self.rotation = rotation


	#
	# Actually tells the motors to do something
	#

	def doit(self):

		self.robotDrive.MecanumDrive_Polar(self.magnitude, self.direction, self.rotation)

		# by default, the robot shouldn't move
		self.magnitude = 0
		self.direction = 0
		self.rotation = 0
