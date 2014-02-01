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
import ui.util

from target_detector import target_data

import gtk

class TargetingTuningWidget(object):
    '''
        Targeting debugging settings
    '''
    
    ui_filename = 'targeting_tuning_widget.ui'
    
    ui_widgets = [
        'targeting_tuning_widget',
                  
        'adj_thresh_hue_p',
        'adj_thresh_hue_n',
        'adj_thresh_sat_p',
        'adj_thresh_sat_n',
        'adj_thresh_val_p',
        'adj_thresh_val_n',
        'adj_aim_horizontal',
        'adj_aim_vertical',
        
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
        
        'on_adj_aim_horizontal_value_changed',
        'on_adj_aim_vertical_value_changed',
        
        'on_check_show_hue_p_toggled',
        'on_check_show_hue_n_toggled',
        'on_check_show_sat_p_toggled',
        'on_check_show_sat_n_toggled',
        'on_check_show_val_p_toggled',
        'on_check_show_val_n_toggled',
        'on_check_show_bin_toggled',
        'on_check_show_bin_overlay_toggled',
        
        'on_check_show_contours_toggled',
        'on_check_show_missed_toggled',
        'on_check_show_badratio_toggled',
        'on_check_show_ratio_labels_toggled',
        'on_check_show_labels_toggled',
        'on_check_show_hangle_toggled',
        'on_check_show_targets_toggled',
        
        'on_camera_refresh_clicked'
    ]
    
    thresh_names = ['thresh_hue_p', 'thresh_hue_n', 'thresh_sat_p', 'thresh_sat_n', 'thresh_val_p', 'thresh_val_n']
    
    # builtin settings: values stored in order of thresh names
    kCompSettings = [30, 75, 188, 255, 16, 255]
    kPitSettings = [45, 75, 200, 255, 55, 255]
    
    
    def __init__(self, processor, targeter):
        self.processor = processor
        self.targeter = targeter
        
        ui.util.initialize_from_xml(self)
        
    def initialize(self):
        
        # store references to these so we don't have to do it later
        self.thresh_widgets = [getattr(self, 'adj_%s' % name) for name in self.thresh_names]

        # always setup builtins, they shouldn't change at all
        settings.set('camera/thresholds/Competition', self.kCompSettings)
        settings.set('camera/thresholds/Pit', self.kPitSettings)
        
        # setup widgets with thresholds
        # -> this implicitly sets up the detector correctly, since the widget
        #    change event changes the detector value
        current_thresholds = [settings.get('camera/%s' % name, default) for name, default in izip(self.thresh_names, self.kCompSettings)]
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
        
        # initialize aim height variable
        aim_horizontal = settings.get('targeting/aim_horizontal', target_data.kOptimumHorizontalPosition)
        self.adj_aim_horizontal.set_value(aim_horizontal * 100.0)
        
        aim_vertical = settings.get('targeting/aim_vertical', target_data.kOptimumVerticalPosition)
        self.adj_aim_vertical.set_value(aim_vertical * 100.0)
        
    def get_widget(self):
        return self.targeting_tuning_widget
    
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
            
    def save_thresholds(self, name, thresholds):
        settings.set('camera/thresholds/%s' % name, thresholds)
            
    def on_thresh_selection_combo_changed(self, widget):
        self.set_thresholds(settings.get('camera/thresholds/%s' % self.get_selected_threshold_setting()))
    
    def on_save_thresh_button_clicked(self, widget):
        # get current setting name
        name = self.get_selected_threshold_setting()
        
        # don't allow saving to builtins!
        if name in ['Competition', 'Pit']:
            ui.util.show_error(None, "Cannot overwrite builtin settings!")
            return
        
        self.save_thresholds(name, self.get_thresholds())
    
    def on_save_as_thresh_button_clicked(self, widget):
        
        name = self.get_selected_threshold_setting()
        
        def _validator(text):
            if settings.has_option('camera/thresholds/%s' % text):
                return 'Setting already exists!'
            return True
         
        new_name = ui.util.get_text(None, 'Save settings as', name, _validator)
        if new_name is not None:
            self.save_thresholds(new_name, self.get_thresholds())
            self.thresh_model.append((new_name,))
            self.thresh_selection_combo.set_active(len(self.thresh_model)-1)
    
    def on_delete_thresh_button_clicked(self, widget):
        name = self.get_selected_threshold_setting()
        
        # don't allow deleting builtins!
        if name in ['Competition', 'Pit']:
            ui.util.show_error(None, "Cannot delete builtin settings!")
            return
        
        if ui.util.yesno(None, "Delete setting %s?" % name) == gtk.RESPONSE_YES:
            for i, row in enumerate(self.thresh_model):
                if name == row[0]:
                    del self.thresh_model[i]
                    break
            
            settings.remove_option('camera/thresholds/%s' % name)
            settings.save()
    
    def _on_thresh(self, widget, name):
        v = widget.get_value()
        settings.set('camera/%s' % name, v)
        setattr(self.processor.detector, name, v)
        self.processor.refresh()
        
    on_adj_thresh_hue_p_value_changed = lambda self, w: self._on_thresh(w, 'thresh_hue_p')
    on_adj_thresh_hue_n_value_changed = lambda self, w: self._on_thresh(w, 'thresh_hue_n')
    on_adj_thresh_sat_p_value_changed = lambda self, w: self._on_thresh(w, 'thresh_sat_p')
    on_adj_thresh_sat_n_value_changed = lambda self, w: self._on_thresh(w, 'thresh_sat_n')
    on_adj_thresh_val_p_value_changed = lambda self, w: self._on_thresh(w, 'thresh_val_p')
    on_adj_thresh_val_n_value_changed = lambda self, w: self._on_thresh(w, 'thresh_val_n')
    
    def on_adj_aim_horizontal_value_changed(self, widget):
        value = widget.get_value() * 0.01
        self.processor.detector.kOptimumHorizontalPosition = value
        self.targeter.kOptimumHorizontalPosition = value
        settings.set('targeting/aim_horizontal', value)
        self.processor.refresh()
        
    def on_adj_aim_vertical_value_changed(self, widget):
        value = widget.get_value() * 0.01
        self.processor.detector.kOptimumVerticalPosition = value
        self.targeter.kOptimumVerticalPosition = value
        settings.set('targeting/aim_vertical', value)
        self.processor.refresh()
            
    def on_check_show_hue_p_toggled(self, widget):
        self.processor.detector.show_hue = widget.get_active()
        self.processor.refresh()
        
    def on_check_show_hue_n_toggled(self, widget):
        self.processor.detector.show_hue = widget.get_active()
        self.processor.refresh()
    
    def on_check_show_sat_p_toggled(self, widget):
        self.processor.detector.show_sat = widget.get_active()
        self.processor.refresh()
        
    def on_check_show_sat_n_toggled(self, widget):
        self.processor.detector.show_sat = widget.get_active()
        self.processor.refresh()
    
    def on_check_show_val_p_toggled(self, widget):
        self.processor.detector.show_val = widget.get_active()
        self.processor.refresh()
        
    def on_check_show_val_n_toggled(self, widget):
        self.processor.detector.show_val = widget.get_active()
        self.processor.refresh()
        
    def on_check_show_bin_toggled(self, widget):
        self.processor.detector.show_bin = widget.get_active()
        self.processor.refresh()
        
    def on_check_show_bin_overlay_toggled(self, widget):
        self.processor.detector.show_bin_overlay = widget.get_active()
        self.processor.refresh()
        
    def on_check_show_contours_toggled(self, widget):
        self.processor.detector.show_contours = widget.get_active()
        self.processor.refresh()
        
    def on_check_show_missed_toggled(self, widget):
        self.processor.detector.show_missed = widget.get_active()
        self.processor.refresh()
        
    def on_check_show_badratio_toggled(self, widget):
        self.processor.detector.show_badratio = widget.get_active()
        self.processor.refresh()
        
    def on_check_show_ratio_labels_toggled(self, widget):
        self.processor.detector.show_ratio_labels = widget.get_active()
        self.processor.refresh()
        
    def on_check_show_labels_toggled(self, widget):
        self.processor.detector.show_labels = widget.get_active()
        self.processor.refresh()
        
    def on_check_show_hangle_toggled(self, widget):
        self.processor.detector.show_hangle = widget.get_active()
        self.processor.refresh()
        
    def on_check_show_targets_toggled(self, widget):
        self.processor.detector.show_targets = widget.get_active()
        self.processor.refresh()
        
    def on_camera_refresh_clicked(self, widget):
        self.processor.refresh()
        
