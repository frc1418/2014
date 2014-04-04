
Team 1418 robot code + driver station UI
========================================

PLEASE NOTE! The contents of this distribution is distributed under two
licenses! The robot portion of the code is distributed under the BSD license,
found in LICENSE. 

The driver station portion of the code is derived from the 2013 KwarqsDashboard,
and is distributed under the GPLv3 license, found in driver_station/COPYING

Introduction
============

This code is released from Team 1418's 2014 robot. Team 1418 had one of their
best years yet in 2014. 

They had a dominating performance at Richmond at the Virginia Regional,
finishing as the #2 seed, and led the #2 alliance to the finals with teams
2383 and 435. They were awarded the Industrial Design award for a variety
of reasons, including their simple but effective robot design, multiple
autonomous modes and useful touchscreen driver station interface.  

At the Greater DC Regional, they had a rocky start and ended up finishing
as the 7th seed, but led the #6 alliance to the finals with teams 1885 and
2537. 

Highlights of the code
----------------------

* Full pyfrc integration for testing & robot simulation
* Unit tests over the robot code with 70% code coverage
* Complex autonomous mode support
	* Multiple working autonomous modes used in competition
		* Two balls - uses a gyro to make sure the robot drives straight
		* Single ball shoot
		* Single ball hot goal shoot
	* Automatic support for tuning the autonomous mode parameters
	  via the UI
* Automation of core catapult functions
* Mechanum drive

The autonomous mode stuff will be rolled into pyfrc in the near future, so
that it can be used by more teams. 


Deploying onto the robot
------------------------

The robot code is written in Python, and so to run it you must install 
RobotPy onto the robot. Refer to the instructions accompanying RobotPy
for more information. 

With the pyfrc library installed, you can deploy the code onto the robot
by running robot.py with the following arguments:

	$ python robot.py upload
	
This will run the unit tests and upload the code to the robot of your
choice.

Testing/Simulation
------------------

The robot code has full integration with pyfrc. You can use the various
simulation/testing options of the code by running robot.py directly. With
pynetworktables installed, you can use netsim mode of pyfrc to test the
robot code and the driver station UI together. 


Code Structure
==============

.
	You are here.

driver_station/
	Code for our driver station user interface. Please see
	driver_station/README.md for more information 

robot/
	robot/
		src/
			The robot code lives here
		tests/
			py.test-based unit tests that test the code and can be run via pyfrc

	electrical_test/
		src/
			Barebones code ran to make sure all of the electronics are working
		tests/
			Basic testing code to make sure we don't have syntax errors

subsystem_tests/
	This code hasn't been cleaned up, various testing code



2014 Team 1418 Programming Team
===============================

Mentors:

	Dustin Spicuzza, lead software mentor
	dustin@virtualroadside.com
	
Students:

	Leon Tan, robot code
	Tim Winters, robot code
	Tyler Gogol, robot code
	Beamlok Hailemariam, robot code
	Sophie McGinnies, robot code
		
	Shayne Ensign, UI programmer
	Matt Puentes, UI programmer
	
	Ben Rice, Image Processing programmer
