
import cv_widget

class CameraWidget(cv_widget.CvWidget):
    
    def __init__(self, fixed_size):
        cv_widget.CvWidget.__init__(self, fixed_size)
    
    def set_error(self):
        pass
    
    def set_target_data(self, data):
        img, data = data
        
        self.set_from_np(img)
    
    