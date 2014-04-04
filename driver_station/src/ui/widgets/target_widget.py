#
#    This file is part of Team 1418 Dashboard
#
#    Team 1418 Dashboard is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, version 3.
#
#    Team 1418 Dashboard is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Team 1418 Dashboard.  If not, see <http://www.gnu.org/licenses/>.
#


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