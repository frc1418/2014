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

import os.path
import ConfigParser as cp

import logging
logger = logging.getLogger(__name__)


class Settings(cp.RawConfigParser):
    '''
        A class to save/load settings. Settings are referenced as a directory
        like format (option name would be rootsection/section/optionname like
        structure), so that one doesn't need to setup the section name 
        separately from the option name. 
        
        The way this works is inspired by the way settings work in Exaile, 
        which is licensed under GPLv2
    '''
    
    __version__ = 1
        
    __types_to = {
        # type: (key, tofn, fromfn)
        bool:   ('B', str, lambda v: True if v == 'True' else False),
        dict:   ('D', repr, eval),
        float:  ('F', str, float),
        int:    ('I', str, int),
        list:   ('L', repr, eval),
        str:    ('S', str, str),
    }
    
    __types_from = dict((v[0], v[2]) for k, v in __types_to.iteritems())
    
    def __init__(self, location):
        
        cp.RawConfigParser.__init__(self)
        
        # make this case-sensitive
        self.optionxform = str
        
        self._dirty = False
        self._saving = False
        self.location = location
        self.read([location])
        
        version = self.get('settings/version', None)
        
        if version is None:
            self.set('settings/version', self.__version__)
        elif version > self.__version__:
            raise ValueError("Settings version %s not supported, current version is %s" % (version, self.__version__))
        
    def __convtostr(self, value):
        try:
            vtype, convto, convfrom = self.__types_to[type(value)] 
            return '%s: %s' % (vtype, convto(value)) 
        except KeyError:
            raise KeyError('Settings does not currently support saving the following type: %s' % type(value))
               
    def __convfromstr(self, value):
        try:
            vtype, vstr = value.split(': ',1)
        except ValueError:
            return ''
        
        try:
            return self.__types_from[vtype](vstr)
        except KeyError:
            raise KeyError('Unrecognized settings string: %s' % value)
               
        
    def get(self, option, default=None):
        '''Gets the value of an option'''
        
        options = option.split('/')
        section = '/'.join(options[:-1])
        key = options[-1]
        
        try:
            return self.__convfromstr(cp.RawConfigParser.get(self, section, key))
        except cp.NoOptionError:
            return default
        except cp.NoSectionError:
            return default
        
    def has_option(self, option):
        '''Returns True if the specified option exists, False otherwise'''
        
        options = option.split('/')
        section = '/'.join(options[:-1])
        key = options[-1]
        
        return cp.RawConfigParser.has_option(self, section, key)
    
    def items(self, section):
        '''Returns a (name, value) for each option in the section'''
        return [(k, self.__convfromstr(v)) for k,v in cp.RawConfigParser.items(self, section)]
    
    def remove_option(self, option):
        '''Removes an option from the config'''
        
        options = option.split('/')
        section = '/'.join(options[:-1])
        key = options[-1]
        
        retval = cp.RawConfigParser.remove_option(self, section, key)
        self._dirty = True
        
        return retval
        
    def set(self, option, value):
        '''Sets an option to a specific value'''
        
        options = option.split('/')
        section = '/'.join(options[:-1])
        key = options[-1]
        value = self.__convtostr(value)
        
        try:
            cp.RawConfigParser.set(self, section, key, value)
        except cp.NoSectionError:
            self.add_section(section)
            cp.RawConfigParser.set(self, section, key, value)
            
        self._dirty = True
            
    def save(self):
        '''Saves the settings to a file'''
        
        if self._saving == True or self._dirty == False:
            return
        
        self._saving = True
        logger.info('Saving settings to %s' % self.location)
        
        with open(self.location, 'w') as fp:
            self.write(fp)
            fp.flush()
            
        self._dirty = False
        self._saving = False
            
        return True
            

location = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'settings.ini'))
_settings = Settings(location)

# globals used by application

get = _settings.get
set = _settings.set

has_option = _settings.has_option
has_section = _settings.has_section
items = _settings.items
options = _settings.options
remove_option = _settings.remove_option
sections = _settings.sections


save = _settings.save
