
#
# Add this to robotpy as the autonomous toolbox?
#

#
# Or distribute it separately?
#

#
# Interesting. Could implement commands and such in python using decorators
# and other neat madness?
#

try:
    import wpilib
except ImportError:
    from pyfrc import wpilib

import functools
import inspect

#
# Decorators:
#
#   timed_state 
#
def timed_state(f=None, time=None, next_state=None, first=False):
    
    if f is None:
        return functools.partial(timed_state, time=time, next_state=next_state, first=first)
    
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        return f(*args, **kwargs)

    # store state variables here
    wrapper.first = first
    wrapper.name = f.__name__
    wrapper.next_state = next_state
    wrapper.time = time
    wrapper.expires = 0xffffffff
    wrapper.ran = False
    
    # inspect the args, provide a correct call implementation
    args, varargs, keywords, defaults = inspect.getargspec(f)
    
    if keywords is not None or varargs is not None:
        raise ValueError("Invalid function parameters for function %s" % wrapper.name)
    
    # TODO: there has to be a better way to do this. oh well.
    
    if len(args) == 1:
        wrapper.run = lambda self, tm, state_tm: f(self)
    elif len(args) == 2:
        if args[1] == 'tm':
            wrapper.run = lambda self, tm, state_tm: f(self, tm)
        elif args[1] == 'state_tm':
            wrapper.run = lambda self, tm, state_tm: f(self, state_tm)
        else:
            raise ValueError("Invalid parameter name for function %s" % wrapper.name)
    elif args == ['self', 'tm', 'state_tm']:
        wrapper.run = lambda self, tm, state_tm: f(self, tm, state_tm)
    elif args == ['self', 'state_tm', 'tm']:
        wrapper.run = lambda self, tm, state_tm: f(self, state_tm, tm)
    else:
        print(args)
        raise ValueError("Invalid parameter names for function %s" % wrapper.name)
    
    
    # provide a default docstring?
    
    return wrapper


        

class StatefulAutonomous(object):
    '''
        TODO: document this
    '''
    
    __built = False
    __done = False
    
    __sd_args = []
    
    def __init__(self, components):
        
        if not hasattr(self, 'MODE_NAME'):
            raise ValueError("Must define MODE_NAME class variable")
        
        for k,v in components.items():
            setattr(self, k, v)
        
        self.__build_states()
        
    def register_sd_var(self, name, default, add_prefix=True):
        
        sd_name = name
        if add_prefix:
            sd_name = '%s %s' % (self.MODE_NAME, name) 
        
        if isinstance(default, bool):
            wpilib.SmartDashboard.PutBoolean(sd_name, default)
            args = (name, sd_name, wpilib.SmartDashboard.GetBoolean)
            
        elif isinstance(default, int) or isinstance(default, float):
            wpilib.SmartDashboard.PutNumber(sd_name, default)
            args = (name, sd_name, wpilib.SmartDashboard.GetNumber)
            
        elif isinstance(default, str):
            wpilib.SmartDashboard.PutString(sd_name, default)
            args = (name, sd_name, wpilib.SmartDashboard.GetString)
            
        else:
            raise ValueError("Invalid default value")
        
        self.__sd_args.append(args)
    
    def __build_states(self):
    
        has_first = False
    
        #for each state function:
        for name in dir(self.__class__):
            
            state = getattr(self.__class__, name)
            if name.startswith('__') or not hasattr(state, 'next_state'):
                continue
            
            # find a pre-execute function if available
            state.pre = getattr(self.__class__, 'pre_%s' % name, None)

            # is this the first state to execute?
            if state.first:
                if has_first:
                    raise ValueError("Multiple states were specified as the first state!")
                
                self.__first = state
                has_first = True
                
            # make the time tunable
            if state.time is not None:
                self.register_sd_var(state.name + '_time', state.time)
    
        if not has_first:
            raise ValueError("Starting state not defined! Use first=True on a state decorator")
    
        self.__built = True
        
        
        
    def _validate(self):
        # TODO: make sure the state machine can be executed
        # - run at robot time? Probably not. Run this as part of a unit test
        pass
        
    # how long does introspection take? do this in the constructor?
    
    # can do things like add all of the timed states, and project how long
    # it will take to execute it (don't forget about cycles!)
    
    def on_enable(self):
        
        if not self.__built:
            raise ValueError('super().__init__(components) was never called!')
        
        # print out the details of this autonomous mode, and any tunables
        print("Tunable values:")
        
        # read smart dashboard values, print them
        for name, sd_name, fn in self.__sd_args:
            val =  fn(sd_name)
            setattr(self, name, val)
            print("-> %20s: %s" % (name, val))
    
        # set the starting state
        self.__state = self.__first
    
    def on_disable(self):
        '''Called when the autonomous mode is disabled'''
        pass
    
    
    def next_state(self, name):
        '''Call this function to transition to the next state'''
        if name is not None:
            self.__state = getattr(self.__class__, name)
        else:
            self.__state = None
            
        if self.__state is None:
            return
        
        self.__state.ran = False
        
    
    def update(self, tm):
        
        # state: first, name, pre, time
        
        state = self.__state
        
        # determine if the time has passed to execute the next state
        if state is not None and state.expires < tm:
            self.next_state(state.next_state)
            state = self.__state
        
        if state is None:
            if not self.__done:
                print("%.3fs: Done with autonomous mode" % tm)
                self.__done = True
            return
        
        # is this the first time this was executed?
        if not state.ran:
            state.ran = True
            state.expires = tm + getattr(self, state.name + '_time')
            state.start_time = tm
            
            print("%.3fs: Entering state:" % tm, state.name)
        
            # execute the pre state if it exists
            if state.pre is not None:
                state.pre(self, tm)
        
        # execute the state
        state.run(self, tm, tm - state.start_time)

    