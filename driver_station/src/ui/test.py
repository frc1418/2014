import util
class Test():

    ui_filename = "TestSampleThing.ui"
    
    ui_widgets = [
        "hbox1",
        "window",
                  ]
    
    def __init__(self):
        util.initialize_from_xml(self)
        self.window.show()