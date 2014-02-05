Driving Component
=================

Motors
------

* Jaguar 1: Left front motor: 1 is forward
* Jaguar 2: Left rear motor: 1 is forward
* Jaguar 3: Right rear motor: -1.0 is forward
* Jaguar 4: Right front motor: -1.0 is forward

Need to call SetInvertedMotor on left side motors. Something is a bit odd
about this arrangement, I'm not convinced we're doing it right.
 
 
Functions
=========

move(x, y, rotation)
--------------------

Causes the robot to move

* x: The speed that the robot should drive in the X direction. 1 is right [-1.0..1.0] 
* y: The speed that the robot should drive in the Y direction. -1 is forward. [-1.0..1.0] 
* rotation: The rate of rotation for the robot that is completely independent of the translation. 1 is rotate to the right [-1.0..1.0]

