
import sys

try:
    import sys
    
    if sys.version_info[0] != 2:
        sys.stderr.write("ERROR: Unsupported python version %s.%s.%s! This program must be run by a Python 2 interpreter!\n" % \
                          (sys.version_info[0],
                           sys.version_info[1],
                           sys.version_info[2]))
        exit(1)
    

    from common import logutil, image_capture, settings
    from options import configure_options
    
    import cv2
    import numpy as np

    def initialize_pynetworktables(ip):
        
        if ip is not None:
            
            from pynetworktables import NetworkTable
            
            NetworkTable.SetIPAddress(ip)
            NetworkTable.SetClientMode()
            NetworkTable.Initialize()
            
            return NetworkTable.GetTable('SmartDashboard')
        

    if __name__ == '__main__':
        
        front_processor = image_capture.ImageCapture(name='front')
        back_processor = image_capture.ImageCapture(name='back')
        
        # get options first
        parser = configure_options()
        front_processor.configure_options(parser)
        back_processor.configure_options(parser)
        
        options, args = parser.parse_args()
        
        # initialize logging before importing anything that uses logging!
        ql = logutil.configure_logging(options.log_dir)
        
        import logging
        logger = logging.getLogger(__name__)
        
        
        # automatically load pygtk in windows, since the setup is annoying
        if sys.platform == 'win32':
            from common import load_pygtk_windows
            load_pygtk_windows.load_pygtk()
        else:
            import pygtk
            pygtk.require('2.0')
    
        # ok, import stuff so we can get their versions
        import gtk
    
        import gobject
        import glib
    
        import cairo
        
        # do this first, just in case
        gobject.threads_init()
        
        
        logger.info('Starting 1418 Driver Station')

        # show versions
        logger.info('-> Python %s' % sys.version.replace('\n', ' '))
        logger.info('-> GTK %s.%s.%s' % gtk.gtk_version)
        logger.info('-> Cairo %s' % cairo.version)
        logger.info('-> NumPy %s' % np.__version__)
        logger.info('-> OpenCV %s' % cv2.__version__)
        
        # configure and initialize things    
        table = initialize_pynetworktables(options.robot_ip)       

        # initialize cv2.imshow replacement
        import ui.widgets.imshow
        
        # create the back detector
        from targeting.back_detector import BackDetector
        back_processor.set_detector(BackDetector())
        
        # initialize UI
        
        import ui.dashboard
        dashboard=ui.dashboard.Dashboard(table, front_processor, back_processor, options.competition)
        
        try:
            front_processor.initialize(options)
            back_processor.initialize(options)
        except RuntimeError:
            exit(1)
        
        dashboard.initialize_image_processing()

        
        # save the settings every N seconds
        glib.timeout_add_seconds(30, settings.save)
        
            
        #
        # FFMpeg/OpenCV doesn't handle connecting to non-existent cameras
        # particularly well (it hangs), so when we're using a live feed, delay 
        # connecting to the camera (ie, starting processing) until the 
        # NetworkTables client has connected to a robot.
        #
        # Presumably if we can talk to the robot, we can talk to the camera 
        # also. If we're not using a live feed, then just start it regardless.  
        # 
        
        if table is None or not front_processor.is_live_feed():
            front_processor.start()
            
        if table is None or not back_processor.is_live_feed():
            back_processor.start()
        
        # gtk main
        
        
        #gtk.threads_init()
            
        #gtk.threads_enter()
        gtk.main()
        #gtk.threads_leave()
        
        
        logger.info('Shutting down the driver station')
        settings.save()
        
        # shutdown anything needed here, like the logger
        back_processor.stop()
        front_processor.stop()
        
        ql.stop()


except Exception as e:

    if __name__ == '__main__':
        import traceback
        traceback.print_exc()
    
        try:
            import msvcrt
        except ImportError:
            pass
        else:        
            msvcrt.getch()
    else:
        raise