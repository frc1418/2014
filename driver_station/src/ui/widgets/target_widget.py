
from camera_widget import CameraWidget

class TargetWidget(CameraWidget):
    
    def __init__(self, fixed_size, table):
        CameraWidget.__init__(self, fixed_size)
        self.table = table
        
    def set_target_data(self, data):
        CameraWidget.set_target_data(self, data)
        
        img, isHot = data
        self.table.PutBoolean('IsHot', isHot)