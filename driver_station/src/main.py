
import sys

try:

    #from common import logutil, settings
    #from options import configure_options

    # ok, import stuff so we can get their versions
    import pygtk
    pygtk.require('2.0')
    import gtk

    import gobject
    import glib

    import cairo

    import cv2
    import numpy as np

    # do this first, just in case
    gobject.threads_init()

    def initialize_pynetworktables(ip):
        
        if ip is not None:
            
            from pynetworktables import NetworkTable
            
            NetworkTable.SetIPAddress(ip)
            NetworkTable.SetClientMode()
            NetworkTable.Initialize()
            
            return NetworkTable.GetTable('SmartDashboard')
        

    if __name__ == '__main__':
        
        # get options first
        #parser = configure_options()
        #options, args = parser.parse_args()
        
        # initialize logging before importing anything that uses logging!
        #ql = logutil.configure_logging(options.log_dir)
        
        import logging
        logger = logging.getLogger(__name__)
        
        logger.info('Starting 1418 Driver Station')

        # show versions
        logger.info('-> Python %s' % sys.version.replace('\n', ' '))
        logger.info('-> GTK %s.%s.%s' % gtk.gtk_version)
        logger.info('-> Cairo %s' % cairo.version)
        logger.info('-> NumPy %s' % np.__version__)
        logger.info('-> OpenCV %s' % cv2.__version__)
        
        # configure and initialize things    
        #table = initialize_pynetworktables(options.robot_ip)

        # setup the image processing and start it
        #import target_detector.processing
        
        #processor = target_detector.processing.ImageProcessor()

        # initialize UI
        #import ui.dashboard
        #dashboard = ui.dashboard.Dashboard(processor, table, options.competition)
        
        # save the settings every N seconds
        #glib.timeout_add_seconds(30, settings.save)
        
        # initialize cv2.imshow replacement
        #import ui.widgets.imshow
        
        #try:
        #    processor.initialize(options, dashboard.camera_widget)
        #except RuntimeError:
        #    exit(1)
            
        #
        # FFMpeg/OpenCV doesn't handle connecting to non-existent cameras
        # particularly well (it hangs), so when we're using a live feed, delay 
        # connecting to the camera (ie, starting processing) until the 
        # NetworkTables client has connected to a robot.
        #
        # Presumably if we can talk to the robot, we can talk to the camera 
        # also. If we're not using a live feed, then just start it regardless.  
        # 
        
        #if table is None or not processor.is_live_feed():
        #    processor.start()
        
        # gtk main
        #dashboard.show_all()
        import ui.test
        test=ui.test.Test()
        
        #gtk.threads_init()
            
        #gtk.threads_enter()
        gtk.main()
        #gtk.threads_leave()
        
        
        #logger.info('Shutting down Kwarqs Dashboard')
        #settings.save()
        
        # shutdown anything needed here, like the logger
        #processor.stop()
        #ql.stop()


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