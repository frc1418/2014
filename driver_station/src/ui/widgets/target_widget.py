
from camera_widget import CameraWidget

class TargetWidget(CameraWidget):
    
    def __init__(self, fixed_size, table):
        CameraWidget.__init__(self, fixed_size)
        self.table = table
        
    def set_target_data(self, data):
        CameraWidget.set_target_data(self, data)
        
        img, (isHotLeft, isHotRight) = data
        
        # problem -- this should only be communicated when the robot
        #            mode changes. The goals default to showing
        self.table.PutBoolean('IsHotLeft', isHotLeft)
        self.table.PutBoolean('IsHotRight', isHotRight)