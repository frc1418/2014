
import gtk
import time
import math

#from matplotlib.backends.backend_gtk import FigureCanvasGTK as FigureCanvas
from matplotlib.backends.backend_gtkagg import FigureCanvasGTKAgg as FigureCanvas
#from matplotlib.backends.backend_gtkcairo import FigureCanvasGTKCairo as FigureCanvas

from matplotlib.backends.backend_gtkagg import NavigationToolbar2GTKAgg as NavigationToolbar

from matplotlib.figure import Figure
from numpy import arange

import util

from widgets import (
   network_tables,
 )

import logging
logger = logging.getLogger(__name__)

class GraphPlot(object):

    # glade file to load
    ui_filename = "GraphPlot.ui"
    
    # widgets to load from the glade file. Each one of these is added to 'self' after
    # you call 'initialize_from_xml'
    ui_widgets = [
        'window',
        'graphImage',
        'toolbar'
    ]
    
    HISTORY = 3
    
    def __init__(self, NetworkTable):
        
        util.initialize_from_xml(self)
        
        self.dead = False
        self.plots = []
        
        self.count = 0
        
        self.netTable = NetworkTable
        self.netTable.PutBoolean('EnableTuning',True)
        
        self.figure = Figure(figsize=(5,4), dpi=100)
        self.axes = self.figure.add_subplot(111)
         
        self.canvas = FigureCanvas(self.figure)  # a gtk.DrawingArea
        
        self.graphImage = util.replace_widget(self.graphImage, self.canvas)
        self.toolbar = util.replace_widget(self.toolbar, NavigationToolbar(self.canvas, self.window))
                           
        self.window.show_all()
        
        # listen to network tables variables
        network_tables.attach_fn(self.netTable, "Catapult Values", self.on_update_CatapultValues, self.window)
        network_tables.attach_fn(self.netTable, "EnableTuning", self.on_update_EnableTuning, self.window)
        
    def on_update_EnableTuning(self, key, value):
        if not self.dead and not value:
            self.netTable.PutBoolean('EnableTuning', True)
        
    def on_update_CatapultValues(self, key, value):
        arraybutitsastring = self.netTable.GetString('Catapult Values', key)
        print(arraybutitsastring, 'String version')
        array=eval(arraybutitsastring)
        print(array, 'array version')
        self.count += 1
        
        step = 0.025
        x = arange(0, len(array)*step, step)
        
        plot = self.axes.plot(x, array, label=str(self.count))
        
        # clear old things
        if len(self.axes.lines) > self.HISTORY:
            self.axes.lines.pop(0)
            
        self.axes.legend()
        self.canvas.draw() 
    
    def on_destroy(self, window):
        self.dead = True
        self.netTable.PutBoolean('EnableTuning',False)
        
    
class GraphOpener(object):
    
    def __init__(self, NetworkTable):
        self.graphPlot = None
        self.netTable = NetworkTable
        
    def show(self):
        if self.graphPlot == None:
            self.graphPlot = GraphPlot(self.netTable)
            self.graphPlot.window.connect("destroy", self.on_destroy)
     
    def on_destroy(self, widget):
        self.graphPlot=None
    