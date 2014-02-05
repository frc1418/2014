Catapult Component
==================

Motors
------

* CANJaguar 5 - Winch motor
  * Setting to +1.0 brings the catapult arm down
  * Limit switch connected to Forward
  
Solenoids
---------

* Channel 1: When on, the winch motor pulls the catapult arm down
* Channel 2: When on, the catapult is released

Sensors
-------

* Analog Channel 4 - Potentiometer 
  * Mechanical team still needs to fix this, voltage measurement isn't stable
* Analog Channel 6 - Optical Sensor
  * If catapult is not cocked, then the reading is not accurate because it's in the way



Functions
=========

launcher: controlled by one CIM, which turns on to wind up the winch, which draws catapult down into ready-to-fire position, which is decided by the potentiometer. 

optical sensor will verify that there is in fact a ball

Pnuematic piston will extend to pull dog out, and axil will free wheel, releasing the catapult. 

Returns to to default position, but must be winched down again to fire. 

-----------------------------------------------------------------------

Getting Ball: basket must be winched down to pick up off the floor.

Needs to be able to lower about half way if a human player is to load it. 

