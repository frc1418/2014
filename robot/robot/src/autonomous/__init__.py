'''
    Implements an autonomous mode management program. Example usage:
    
        from autonomous import AutonomousModeManager
        
        components = {'drive': drive, 
                      'component1': component1, ... }
        autonomous = AutonomousModeManager(components)
        
        class MyRobot(wpilib.SimpleRobot):
        
            ... 
            
            def Autonomous(self):
                autonomous.run(self, control_loop_wait_time)
                
            def update(self):
            
                ... 
    
    Note that the robot instance passed to AutonomousModeManager.run() must
    have an update function. 
'''

from glob import glob
import imp
import inspect
import os
import sys

from common.delay import PreciseDelay

try:
    import wpilib
except ImportError:
    import fake_wpilib as wpilib


class AutonomousModeManager(object):
    '''
        The autonomous manager loads all autonomous mode modules and allows
        the user to select one of them via the SmartDashboard. 
        
        See template.txt for a sample autonomous mode module
    '''
    
    def __init__(self, components):
        
        self.ds = wpilib.DriverStation.GetInstance()
        self.modes = {}
        self.active_mode = None
        
        print( "AutonomousModeManager::__init__() Begins" )
        
        # load all modules in the current directory
        modules_path = os.path.dirname(os.path.abspath(__file__))
        sys.path.append(modules_path)
        modules = glob(os.path.join(modules_path, '*.py' ))
        
        for module_filename in modules:
            
            module_name = os.path.basename(module_filename[:-3])
            
            if module_name in  ['__init__', 'manager']:
                continue
        
            try:
                module = imp.load_source(module_name, module_filename)
            except:
                if not self.ds.IsFMSAttached():
                    raise
            
            #
            # Find autonomous mode classes in the modules that are present
            # -> note that we actually create the instance of the objects here,
            #    so that way we find out about any errors *before* we get out 
            #    on the field.. 
            
            for name, obj in inspect.getmembers(module, inspect.isclass):

                if hasattr(obj, 'MODE_NAME') :
                    try:
                        instance = obj(components)
                    except:
                        
                        if not self.ds.IsFMSAttached():
                            raise
                        else:
                            continue
                    
                    if instance.MODE_NAME in self.modes:
                        if not self.ds.IsFMSAttached():
                            raise RuntimeError( "Duplicate name %s in %s" % (instance.MODE_NAME, module_filename) )
                        
                        print( "ERROR: Duplicate name %s specified by object type %s in module %s" % (instance.MODE_NAME, name, module_filename))
                        self.modes[name + '_' + module_filename] = instance
                    else:
                        self.modes[instance.MODE_NAME] = instance
        
        # now that we have a bunch of valid autonomous mode objects, let 
        # the user select one using the SmartDashboard.
        
        # SmartDashboard interface
        sd = wpilib.SmartDashboard
        self.chooser = wpilib.SendableChooser()
        
        print("Loaded autonomous modes:")
        for k,v in self.modes.items():
            
            if hasattr(v, 'DEFAULT') and v.DEFAULT == True:
                print(" -> %s [Default]" % k)
                self.chooser.AddDefault(k, v)
            else:
                print( " -> %s" % k )
                self.chooser.AddObject(k, v)
                
        # provide a none option        
        self.chooser.AddObject('None', None)
                
        # must PutData after setting up objects
        sd.PutData('Autonomous Mode', self.chooser)
        
        print( "AutonomousModeManager::__init__() Done" )
    
            
    def run(self, robot, control_loop_wait_time):    
        '''
            This function does everything required to implement autonomous
            mode behavior. 
            
            :param robot: a SimpleRobot derived class, and is expected to 
                          have a function called 'update', which will do 
                          updates on all motors and components.
                          
            :param control_loop_wait_time: Amount of time between loops
        '''
        
        print("AutonomousModeManager::Autonomous()")
        
        # don't risk the watchdog, hopefully we do everything right here :)
        robot.GetWatchdog().SetEnabled(False)
        
        # keep track of how much time has passed in autonomous mode
        timer = wpilib.Timer()
        timer.Start()
        
        try:
            self.on_autonomous_enable()
        except:
            if not self.ds.IsFMSAttached():
                raise
        
        #
        # Autonomous control loop
        #
        
        delay = PreciseDelay(control_loop_wait_time)
        
        while robot.IsAutonomous() and robot.IsEnabled():
 
            try:            
                self.update(timer.Get())
            except:
                if not self.ds.IsFMSAttached():
                    raise
            
            robot.update()
             
            delay.wait()
            
        #
        # Done with autonomous, finish up
        #
            
        try:
            self.on_autonomous_disable()
        except:
            if not self.ds.IsFMSAttached():
                raise
        
    #
    #   Internal methods used to implement autonomous mode switching. Most
    #   users of this class will not want to use these functions, use the
    #   run() function instead. 
    #
    
    def on_autonomous_enable(self):
        '''Select the active autonomous mode here, and enable it'''
        self.active_mode = self.chooser.GetSelected()
        if self.active_mode is not None:
            print("AutonomousModeManager: Enabling %s" % self.active_mode.MODE_NAME)
            self.active_mode.on_enable()
 
    def on_autonomous_disable(self):
        '''Disable the active autonomous mode'''
        if self.active_mode is not None:
            print("AutonomousModeManager: Disabling %s" % self.active_mode.MODE_NAME)
            self.active_mode.on_disable()
            
        self.active_mode = None
        
    def update(self, time_elapsed):
        '''Run the code for the current autonomous mode'''
        if self.active_mode is not None:
            self.active_mode.update(time_elapsed)

