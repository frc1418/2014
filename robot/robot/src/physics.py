
from pyfrc import wpilib

import math

class PhysicsEngine(object):
    '''
        Useful simulation pieces for testing our robot code
    '''
    
    def __init__(self):
        
        self.winch_value = 0
        
        self.winch_min = 2.5    # top
        self.winch_max = 4.1    # bottom
        
        self.winch_position = self.winch_min
        
        
        
        self.winch_range = self.winch_max - self.winch_min
        
        self.last_tm = None
        self.motor_tm = None
        
    
    def update_sim(self, tm):
        
        last_tm = self.last_tm
        self.last_tm = tm
        
        if last_tm is None:
            return
        
        time_diff = tm - last_tm
        
        
        motor = wpilib.CAN._devices[5]
        motor.forward_ok = True
        
        
        # when the dog is let out, then position will never go down
        dog_out = (wpilib.Solenoid._channels[1].value == True)
        
        # let the winch out!
        if dog_out:
            if self.winch_position > self.winch_min:
                self.winch_position += self.winch_range * time_diff * -3
                
        else:
            # calculate winch based on motor value
            if self.winch_position <= self.winch_max:
                self.winch_position += motor.value * self.winch_range * time_diff * .7
            else:
                motor.forward_ok = False
        
        # potentiometer value is position
        wpilib.AnalogModule._channels[3].voltage = self.winch_position
        
        # calculate the voltage/current
        if motor.value == 0 or motor.forward_ok == False:
            self.motor_tm = None
            motor.voltage = 0
            motor.current = 0
        else:
            
            # if motor is running, voltage is constant (probably not realistic)
            motor.voltage = motor.value * 12.5
            
            if self.motor_tm is None:
                self.motor_tm = 0
            else:
                self.motor_tm += time_diff
            
            # some equation that makes a pretty graph
            motor.current = motor.value * math.sin(8*self.motor_tm) + 3*self.motor_tm
        