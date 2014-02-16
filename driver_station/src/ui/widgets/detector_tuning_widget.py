
import gtk

from .preprocessor_tuning_widget import PreprocessorTuningWidget

class DetectorTuningWidget(gtk.VBox):
    
    
    def __init__(self, processor):
        gtk.VBox.__init__(self)
        
        self.processor = processor
        self.detector = processor.detector
            
        self.preprocessor_tuner = PreprocessorTuningWidget(processor)
        
        self.pack_start(self.preprocessor_tuner, expand=False, fill=True)
        
        
        # gather all of the settings from the detector, and create them
        # -> basically, anything that starts with 'show' is a setting we
        #    can tune. 
        
        def on_toggled(widget, name):
            setattr(self.detector, name, widget.get_active())
            self.processor.refresh()
        
        
        for attr in dir(self.detector):
            if attr.startswith('show'):
                
                default, label = getattr(self.detector, attr)
                
                widget = gtk.CheckButton(label=label)
                self.pack_start(widget, expand=False, fill=False)
                widget.connect('toggled', on_toggled, attr)
                
                widget.set_active(default)
                setattr(self.detector, attr, default)
                
    
    def initialize(self):
        self.preprocessor_tuner.initialize()
                
        
            