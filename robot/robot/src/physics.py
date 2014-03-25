
from pyfrc import wpilib

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
        
    
    def update_sim(self, tm):
        
        last_tm = self.last_tm
        self.last_tm = tm
        
        if last_tm is None:
            return
        
        time_diff = tm - last_tm
        
        # if motor is running, voltage is constant (probably not realistic)
        motor = wpilib.CAN._devices[5]
        motor.forward_ok = True
        
        # when motor starts, spike the current
        
        # bring it back
        
        
        
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
            
        
    
    def sim_CANJaguar_GetOutputCurrent(self):
        pass
    
    def sim_CANJaguar_GetOutputVoltage(self):
        pass
    
    def sim_CANJaguar_Set(self, obj, fn, value):
        if obj.deviceNumber == 5:
            self.winch_value = value
        
        fn(value)