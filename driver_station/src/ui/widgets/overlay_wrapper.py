
import gobject
import gtk
import cairo


class OverlayWindow(gtk.Window):
    '''
        Code partially taken from the documentation for gtk.gdk.Window
        about compositing windows.  
    '''
    
    def __init__(self, child):
        '''Attaches to a widget and puts an overlay over it'''
        
        gtk.Window.__init__(self)
        
        self.enabled = True
        self.disabled_text = None
        self.disabled_text_size = 64.0
        
        self.ebox = gtk.EventBox()
        
        self.ebox.connect('realize', lambda w: w.window.set_composited(True))
        
        self.add(self.ebox)
        self.ebox.add(child)
        
        
    def set_disabled_text(self, value):
        self.disabled_text = value
        if not self.enabled:
            self.queue_draw()
            
    def set_disabled_text_size(self, value):
        self.disabled_text_size = value
        if not self.enabled:
            self.queue_draw()
        
    def set_enabled(self, value):
        '''When set to true, input is disabled and all child widgets are
           shaded'''
        
        self.ebox.set_above_child(not value)
    
        self.enabled = value
        self.queue_draw()
        
    def do_expose_event(self, event):
        '''Overrides the virtual expose function for the gtk.Window'''
        
        gtk.Window.do_expose_event(self, event)
        
        #get our child (in this case, the event box)
        #child = self.ebox
        child = self.get_child()
        
        #create a cairo context to draw to the window
        cxt = self.window.cairo_create()
    
        #the source data is the (composited) event box
        cxt.set_source_pixmap (child.window,
                               child.allocation.x,
                               child.allocation.y)
    
        #draw no more than our expose event intersects our child
        region = gtk.gdk.region_rectangle(child.allocation)
        r = gtk.gdk.region_rectangle(event.area)
        region.intersect(r)
        cxt.region (region)
        cxt.clip()
    
        #composite, with a 50% opacity
        cxt.set_operator(cairo.OPERATOR_OVER)
        cxt.paint()
        
        if not self.enabled:
            
            cxt.set_source_rgba(0, 0, 0, 0.5)
            cxt.paint()
            
            if self.disabled_text is not None:
                
                w, h = event.window.get_size()
                
                cxt.set_font_size(self.disabled_text_size)
                tx, tx, tw, th, txa, tya = cxt.text_extents(self.disabled_text)
                
                x = (w - tw)/2
                y = (h - th)/2
                
                # draw a box behind the text
                cxt.set_source_rgba(0, 0, 0, 0.75)
                cxt.rectangle(x - 15, y - self.disabled_text_size, tw + 40, th + 40)
                cxt.fill()
                
                cxt.set_source_rgb(1, 1, 1)
                
                cxt.move_to(x, y)
                cxt.show_text(self.disabled_text)
    
        return False


gobject.type_register(OverlayWindow)
