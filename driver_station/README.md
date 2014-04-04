
Team 1418 Dashboard
===================

    Team 1418 Dashboard is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, version 3.

    Team 1418 Dashboard is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Team 1418 Dashboard.  If not, see <http://www.gnu.org/licenses/>.


This software is based on the driver station software put together in 2013
by team 2423. There are lots of improvements that were implemented, and will
probably be extracted out into a separate driver station toolkit. 

The software is designed to be used with a touchscreen, and it has been tested
on the following platforms:

- Windows 7 x64 (32-bit python)
- Windows 8 x64 (32-bit python)
- Ubuntu 12.10 x64 (64-bit python)

Installation
============

Once you install the dependencies, you can just run main.py with the correct
arguments. See launcher.au3 for an example.

You must have the following things installed to run the dashboard:

- Python 2.7
- pynetworktables 2014.4 or above
- PyGTK 2.24 and dependencies
	- GTK+, GObject, GLib, etc
- OpenCV 2.x (tested on 2.4.4) python bindings, with FFMPEG wrappers for OpenCV
- NumPy 1.7.x or above
- Matplotlib 1.3.1

Windows specific install notes
------------------------------

To connect to the camera, you must have the FFMPEG wrappers for OpenCV
installed. On Windows, the wrapper is called opencv_ffmpeg244.dll, and
must be installed in C:\Python27 . If it is not installed correctly,
OpenCV will fail silently when trying to connect to the camera.

To install PyGTK on Windows, we recommend installing the GStreamer SDK along
with the python bindings. The software will automatically find the GStreamer
SDK and load the correct libraries if present.


Features
========

- Comprehensive autonomous mode support
	- Fine tuned autonomous mode parameter tuning
	- Multiple autonomous modes supported
- Graphing of robot catapult parameters
- Visual display of robot status
- Most robot features can be controlled from the UI

- Image processing features:
	- Interactive tuning of threshold parameters
	- Comprehensive debugging support
	- Visual indication of hot goal detection
	- Static and live image processing
	- Can support multiple cameras

- Hot goal in a box mode
	- Start the dashboard only showing the camera feed and the
	  image processing tools. Pass main.py --camera-only to run
	  in this mode
	- Transmits 'IsHotLeft' and 'IsHotRight' to the robot via NetworkTables

Team 1418 UI Team
=================

Mentors:

	Dustin Spicuzza, lead software mentor
	dustin@virtualroadside.com

Students:

	Shayne Ensign, UI programmer
	Matt Puentes, UI programmer
	
	Ben Rice, Image Processing programmer

	Camile Borja, UI design consultant, robot image creator
	
Support
=======

If you run into problems trying to get this to work, I highly recommend using
google to figure out how to solve your problem. The ChiefDelphi forums are an
excellent source of help also. 


	