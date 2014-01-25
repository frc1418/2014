'''	
	Driving component
'''

class Drive(object):

	def __init__(self, robotDrive):
		self.robotDrive = robotDrive

	#
	# Verb functions
	#

	def move(self, x, y, z):
		self.x = x
		self.y = y
		self.z = z


	#
	# Actually does stuff
	#

	def doit(self):

		self.robotDrive.MecanumDrive_Cartesian(self.x, self.y, self.z)

		# reset things to defaults
		self.x = 0
		self.y = 0
		self.z = 0
