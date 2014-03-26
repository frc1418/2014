
import gtk
import pygtk
import util
import glib
import time
import math
#from matplotlib.backends.backend_gtk import FigureCanvasGTK as FigureCanvas
from matplotlib.backends.backend_gtkagg import FigureCanvasGTKAgg as FigureCanvas
#from matplotlib.backends.backend_gtkcairo import FigureCanvasGTKCairo as FigureCanvas

from matplotlib.figure import Figure
from numpy import arange

from widgets import (
   network_tables,
 )

import logging
logger = logging.getLogger(__name__)

class GraphPlot(object):
    # Reference Links:
    #    Dropdown: http://www.pygtk.org/pygtk2tutorial/sec-ComboBoxAndComboboxEntry.html#comboboxbasicfig
    # glade file to load
    ui_filename = "GraphPlot.ui"
    
    # widgets to load from the glade file. Each one of these is added to 'self' after
    # you call 'initialize_from_xml'
    ui_widgets = [
    'Window',
    'GraphImage',
    ]
    def __init__(self, NetworkTable):
        self.netTable = NetworkTable
        util.initialize_from_xml(self)
        self.Window.show_all()
        self.netTable.PutBoolean('EnableTuning',True)
        network_tables.attach_fn(self.netTable, "Catapult Values", self.updategraph,self.Window)
        
        
        f = Figure(figsize=(5,4), dpi=100)
        self.a = f.add_subplot(111)
        #t = arange(0.0,3.0,0.01)
        #s = sin(2*pi*t)
        #a.plot(t,s)
        
        canvas = FigureCanvas(f)  # a gtk.DrawingArea

        util.replace_widget(self.GraphImage, canvas)
        #self.Window.add(canvas)                        
        self.Window.show_all()
        
    def updategraph(self, key, value):
        newestarray=network_tables.get_number_array(self.netTable, 'Catapult Values')
        
        
    
    def on_destroy(self, window):
        self.netTable.PutBoolean('EnableTuning',False)
        
    
class GraphOpener(object):
    
    def __init__(self, NetworkTable):
        self.GraphPlot = None
        self.foo=NetworkTable
        
    def show(self):
        if self.GraphPlot==None:
            self.GraphPlot=GraphPlot(self.foo)
            self.GraphPlot.Window.connect("destroy", self.destroy)
            array=network_tables.get_number_array(self.foo,"Catapult Values")
            step = 0.025
            x = arange(0, len(array)*step, step)
            print(array)
            self.GraphPlot.a.plot(x, array)
    def destroy(self, widget):
        self.GraphPlot=None;
    