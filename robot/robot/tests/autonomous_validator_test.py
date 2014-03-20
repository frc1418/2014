#
# This set of tests only exists to make sure that our new autonomous modes
# match the old autonomous modes exactly. 
#
# The way this works is we load each mode, iterate time, and record the 
# output of the components. We cheat a bit and use fake components, and just
# record the values and compare those instead. This should make analysis
# easier.
#
# For easier testing, you should comment out the files that you aren't
# currently testing. When you test new modes, you will want to uncomment
# them otherwise the test won't run. :) See lines 144 - 157
#
#

import imp
import sys
from os.path import abspath, basename, dirname, join

import inspect


ENABLED = True

class Recorder(object):
    
    def __init__(self):
        self.data = []
    
    def record_data(self, data):
        self.data.append(data)
        print('>>       ', data)
        
    def clear(self):
        old_data = self.data
        self.data = []
        return old_data

class FakeComponent(object):
    '''
        This deep magic object forwards function calls + parameters
        to the recorder object
    '''
    
    def __init__(self, name, recorder):
        self._name = name
        self._recorder = recorder
        
    def recorder_call(self, fn_name, *args, **kwargs):
        
        all_args = list(args) + ['%s=%s' % (k, v) for k, v in kwargs.items()]
        self._recorder.record_data("%s.%s(%s)" % (self._name, fn_name, ', '.join(map(str,all_args))))
        
    def __getattribute__(self, key):
        if key in ['_name', '_recorder']:
            return object.__getattribute__(self, key)
        
        return lambda *args, **kwargs: object.__getattribute__(self, 'recorder_call')(key, *args, **kwargs)



def do_component_test(old_cls, new_cls):
    
    print(">> Begin testing autonomous class", new_cls.__name__)
    
    # create fake components and a recorder
    recorder = Recorder()
    components = dict([(name, FakeComponent(name, recorder)) for name in ['drive', 'catapult', 'intake']])
    
    old_obj = old_cls(components)
    new_obj = new_cls(components)
    
    # enable the thing
    print(">> old_component on_enable")
    old_obj.on_enable()
    
    print(">> new_component on_enable")
    new_obj.on_enable()
    
    print(">> Running autonomous mode")
    
    tm = 0
    while tm <= 10.0:
        
        print(">> Time: %.3f" % tm)
        print(">>    old_component:")
        
        # run the old object first
        old_obj.update(tm)
        old_data = recorder.clear()
        
        print(">>    new_component:")
        
        # run the new object next
        new_obj.update(tm)
        new_data = recorder.clear()
        
        # did they match?
        if old_data != new_data:
            print(">>   ERROR: old_component function calls don't match new_component function calls at time %.3f!" % tm)
            
        assert old_data == new_data
        
        tm += 0.025
        
    print(">> Test complete.")


def find_autonomous_object(module):
    '''Returns the first object that is an autonomous mode'''
    for name, obj in inspect.getmembers(module, inspect.isclass):
        if hasattr(obj, 'MODE_NAME') :
            return obj
        
    raise ValueError("No valid autonomous mode object found in %s!" % module)

def load_autonomous(module_filename):
    sys.path = [dirname(module_filename)]
    module_name = basename(module_filename[:-3])
    module = imp.load_source(module_name, module_filename)
    return find_autonomous_object(module)

def load_old_autonomous(name):
    module_filename = abspath(join(dirname(__file__), '..', 'old_autonomous', name))
    return load_autonomous(module_filename)

def load_new_autonomous(name):
    module_filename = abspath(join(dirname(__file__), '..', 'src', 'autonomous', name))
    return load_autonomous(module_filename)

def run_autonomous_mode(wpilib, mode_filename):
    wpilib.SmartDashboard.init()
        
    new_cls = load_new_autonomous(mode_filename)
    old_cls = load_old_autonomous(mode_filename)
            
    do_component_test(old_cls, new_cls)

if ENABLED:
    
    #
    # These actually run the tests for each file
    #
    
    #def test_timed_shoot(wpilib):
        #run_autonomous_mode(wpilib, 'timed_shoot.py')
        
    def test_hot_aim_shoot(wpilib):
        run_autonomous_mode(wpilib, 'hot_aim_shoot.py')
    
    #//def test_hot_shoot(wpilib):
        #run_autonomous_mode(wpilib, 'hot_shoot.py')
        
    #//def test_two_ball(wpilib):
        #run_autonomous_mode(wpilib, 'TwoBall.py')
    
    #def test_two_ball_hot(wpilib):
        #run_autonomous_mode(wpilib, 'TwoBallHot.py')
