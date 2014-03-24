#
#   This file is part of KwarqsDashboard.
#
#   KwarqsDashboard is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, version 3.
#
#   KwarqsDashboard is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with KwarqsDashboard.  If not, see <http://www.gnu.org/licenses/>.
#

import datetime
import os
import optparse

def _get_logdir_path():
    ''' Each time the application starts, we store logs in a different 
        directory that has a timestamp in its name
    
        do not call this function, use log_dir instead
    '''
    now = datetime.datetime.now().strftime('%Y-%m-%d %H%M-%S')
    return os.path.abspath(os.path.join(os.path.dirname(__file__), 'logs', now))


def configure_options():
    
    # TODO: integrate settings with options

    parser = optparse.OptionParser()
    
    parser.add_option('--robot-ip', dest='robot_ip', default=None,
                      help='Specified the IP address of the robot')
    
    parser.add_option('--logdir', dest='log_dir', default=_get_logdir_path(),
                      help='Directory to store logging information into')
    
    parser.add_option('--competition', dest='competition', default=False, action='store_true',
                      help='Set the dashboard to be in competition mode')
    
    parser.add_option('--camera-only', dest='camera_only', default=False, action='store_true',
                      help='Enable the single camera UI')
    
    return parser
