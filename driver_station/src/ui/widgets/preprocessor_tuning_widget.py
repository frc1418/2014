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

from itertools import izip
from common import settings
from .. import util

import gtk

class PreprocessorTuningWidget(gtk.VBox):
    '''
        Debugging/tuning settings for the image preprocessor
    '''
    
    ui_filename = 'preprocessor_tuning_widget.ui'
    
    ui_widgets = [
        'tuning_widget',
                  
        'adj_thresh_hue_p',
        'adj_thresh_hue_n',
        'adj_thresh_sat_p',
        'adj_thresh_sat_n',
        'adj_thresh_val_p',
        'adj_thresh_val_n',
        
        'thresh_selection_combo',
        'thresh_model',
    ]
    
    ui_signals = [
                  
        'on_save_thresh_button_clicked',
        'on_save_as_thresh_button_clicked',
        'on_delete_thresh_button_clicked',
                  
        'on_thresh_selection_combo_changed',
                  
        'on_adj_thresh_hue_p_value_changed',
        'on_adj_thresh_hue_n_value_changed',
        'on_adj_thresh_sat_p_value_changed',
        'on_adj_thresh_sat_n_value_changed',
        'on_adj_thresh_val_p_value_changed',
        'on_adj_thresh_val_n_value_changed',
        
        'on_check_show_hue_p_toggled',
        'on_check_show_hue_n_toggled',
        'on_check_show_sat_p_toggled',
        'on_check_show_sat_n_toggled',
        'on_check_show_val_p_toggled',
        'on_check_show_val_n_toggled',
        
        'on_check_show_bin_toggled',
        'on_check_show_bin_overlay_toggled',
        
        'on_camera_refresh_clicked'
    ]
    
    thresh_names = ['thresh_hue_p', 'thresh_hue_n', 'thresh_sat_p', 'thresh_sat_n', 'thresh_val_p', 'thresh_val_n']
    
    # builtin settings: values stored in order of thresh names
    settings = [ 
        ('Old Competition', [30, 75, 188, 255, 16, 255], False),
        ('Sample', [0, 255, 150, 255, 100, 170], False),
        ('Pit', [45, 75, 200, 255, 55, 255], False),
        ('FRC', [105, 137, 230, 255, 133, 183], True)
    ]
    
    
    def __init__(self, processor):
        
        gtk.VBox.__init__(self)
        
        self.processor = processor
        self.preprocessor = processor.detector.preprocessor
        
        util.initialize_from_xml(self)
        
        self.pack_start(self.tuning_widget)
        
    def initialize(self):
        
        # store references to these so we don't have to do it later
        self.thresh_widgets = [getattr(self, 'adj_%s' % name) for name in self.thresh_names]

        # always setup builtins, they shouldn't change at all
        default_settings = None
        
        for name, setting, is_default in self.settings:
            if is_default:
                default_settings = setting
            settings.set('camera/thresholds/%s' % name, setting)
        
        
        
        # setup widgets with thresholds
        # -> this implicitly sets up the detector correctly, since the widget
        #    change event changes the detector value
        current_thresholds = [settings.get('camera/%s' % name, default) for name, default in izip(self.thresh_names, default_settings)]
        self.set_thresholds(current_thresholds)
        
        
        # initialize the combo box with existing settings
        # -> but block the handler, so we don't accidentally set the settings again
        self.thresh_selection_combo.handler_block_by_func(self.on_thresh_selection_combo_changed)
        
        for i, (name, value) in enumerate(settings.items('camera/thresholds')):
            
            self.thresh_model.append((name,))
            
            # if the value matches completely, set this as the currently selected setting
            # -> this way, the user knows the current settings aren't saved!
            match = True
            for tvalue, cvalue in izip(value, current_thresholds):
                if int(tvalue) != int(cvalue):
                    match = False
                    break
                
            if match:
                self.thresh_selection_combo.set_active(i)
        
        self.thresh_selection_combo.handler_unblock_by_func(self.on_thresh_selection_combo_changed)
        
    # 
    # Threshold setting management
    #
    
    def get_selected_threshold_setting(self):
        return self.thresh_model[self.thresh_selection_combo.get_active()][0]
    
    def get_thresholds(self):
        return [widget.get_value() for widget in self.thresh_widgets]
        
    def set_thresholds(self, thresholds):
        for thresh, widget in izip(thresholds, self.thresh_widgets):
            widget.set_value(thresh)
            widget.value_changed()
            
    def save_thresholds(self, name, thresholds):
        settings.set('camera/thresholds/%s' % name, thresholds)
            
    def on_thresh_selection_combo_changed(self, widget):
        self.set_thresholds(settings.get('camera/thresholds/%s' % self.get_selected_threshold_setting()))
    
    def on_save_thresh_button_clicked(self, widget):
        # get current setting name
        name = self.get_selected_threshold_setting()
        
        # don't allow saving to builtins!
        if name in [k for k, v, d in self.settings]:
            util.show_error(None, "Cannot overwrite builtin settings!")
            return
        
        self.save_thresholds(name, self.get_thresholds())
    
    def on_save_as_thresh_button_clicked(self, widget):
        
        name = self.get_selected_threshold_setting()
        
        def _validator(text):
            if settings.has_option('camera/thresholds/%s' % text):
                return 'Setting already exists!'
            return True
         
        new_name = util.get_text(None, 'Save settings as', name, _validator)
        if new_name is not None:
            self.save_thresholds(new_name, self.get_thresholds())
            self.thresh_model.append((new_name,))
            self.thresh_selection_combo.set_active(len(self.thresh_model)-1)
    
    def on_delete_thresh_button_clicked(self, widget):
        name = self.get_selected_threshold_setting()
        
        # don't allow deleting builtins!
        if name in ['Competition', 'Pit']:
            util.show_error(None, "Cannot delete builtin settings!")
            return
        
        if util.yesno(None, "Delete setting %s?" % name) == gtk.RESPONSE_YES:
            for i, row in enumerate(self.thresh_model):
                if name == row[0]:
                    del self.thresh_model[i]
                    break
            
            settings.remove_option('camera/thresholds/%s' % name)
            settings.save()
    
    def _on_thresh(self, widget, name):
        v = widget.get_value()
        settings.set('camera/%s' % name, v)
        setattr(self.preprocessor, name, v)
        self.processor.refresh()
        
    on_adj_thresh_hue_p_value_changed = lambda self, w: self._on_thresh(w, 'thresh_hue_p')
    on_adj_thresh_hue_n_value_changed = lambda self, w: self._on_thresh(w, 'thresh_hue_n')
    on_adj_thresh_sat_p_value_changed = lambda self, w: self._on_thresh(w, 'thresh_sat_p')
    on_adj_thresh_sat_n_value_changed = lambda self, w: self._on_thresh(w, 'thresh_sat_n')
    on_adj_thresh_val_p_value_changed = lambda self, w: self._on_thresh(w, 'thresh_val_p')
    on_adj_thresh_val_n_value_changed = lambda self, w: self._on_thresh(w, 'thresh_val_n')
            
    def on_check_show_hue_p_toggled(self, widget):
        self.preprocessor.show_hue = widget.get_active()
        self.processor.refresh()
        
    def on_check_show_hue_n_toggled(self, widget):
        self.preprocessor.show_hue = widget.get_active()
        self.processor.refresh()
    
    def on_check_show_sat_p_toggled(self, widget):
        self.preprocessor.show_sat = widget.get_active()
        self.processor.refresh()
        
    def on_check_show_sat_n_toggled(self, widget):
        self.preprocessor.show_sat = widget.get_active()
        self.processor.refresh()
    
    def on_check_show_val_p_toggled(self, widget):
        self.preprocessor.show_val = widget.get_active()
        self.processor.refresh()
        
    def on_check_show_val_n_toggled(self, widget):
        self.preprocessor.show_val = widget.get_active()
        self.processor.refresh()
        
    def on_check_show_bin_toggled(self, widget):
        self.preprocessor.show_bin = widget.get_active()
        self.processor.refresh()
        
    def on_check_show_bin_overlay_toggled(self, widget):
        self.preprocessor.show_bin_overlay = widget.get_active()
        self.processor.refresh()
        
    def on_camera_refresh_clicked(self, widget):
        self.processor.refresh()
        
