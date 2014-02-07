#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
#

# taken from Exaile

from __future__ import division, print_function, unicode_literals

import logging, os, sys

def error(message1, message2=None, die=True):
    """Show error message and exit.
    
    If two message arguments are supplied, the first one will be used as title.
    If `die` is true, exit after showing the message.
    """
    logging.error(message1 + (('\r\n\r\n' + message2) if message2 else ''))
    if sys.stdout.isatty():
        if die:
            print("\r\n[Press Enter to exit.]", file=sys.stderr)
            raw_input()
    else:
        import ctypes
        if not message2:
            message1, message2 = message2, message1
        ctypes.windll.user32.MessageBoxW(None, message2, message1, 0x10)
    if die:
        sys.exit(1)

def load_pygtk():
    try:
        import pygst
        pygst.require('0.10')
        import gst
    except Exception:
        import struct
        is64bit = len(struct.pack(b'P', 0)) == 8
        logging.info("Python arch: %d-bit" % (64 if is64bit else 32))
        gstroot = os.environ.get('GSTREAMER_SDK_ROOT_X86_64', r'C:\gstreamer-sdk\0.10\x64') \
                if is64bit \
                else os.environ.get('GSTREAMER_SDK_ROOT_X86', r'C:\gstreamer-sdk\0.10\x86')
        if not os.path.exists(gstroot):
            error("GStreamer not found",
                    "GStreamer was not found. It can be downloaded from http://www.gstreamer.com/\r\n\r\n" +
                    "See README.Windows for more information.")
        os.environ['PATH'] = gstroot + r'\bin;' + os.environ['PATH']
        gstpypath = gstroot + r'\lib\python2.7\site-packages'
        sys.path.insert(1, gstpypath)
        os.environ['PYTHONPATH'] = gstpypath
        try:
            import pygst
            pygst.require('0.10')
            import gst
        except Exception:
            error("GStreamer Python bindings not found",
                    "The Python bindings for GStreamer could not be imported. Please re-run the GStreamer installer and ensure that \"GStreamer python bindings\" is selected for installation (it should be selected by default).\r\n\r\n" +
                    "GStreamer can be downloaded from http://www.gstreamer.com/\r\n\r\n" +
                    "See README.Windows for more information.")
        else:
            logging.info("GStreamer: %s" % gstroot)
    else:
        logging.info("GStreamer works out of the box")

    try:
        import pygtk
        pygtk.require('2.0')
        import gtk
    except Exception:
        error("GTK/PyGTK not found",
                "PyGTK 2.x could not be imported. Please re-run the GStreamer installer and ensure that \"Gtk toolkit\" and \"Gtk python bindings\" are selected (they should be selected by default). Note that the PyGTK library from pygtk.org is NOT compatible with the GStreamer library from gstreamer.com.\r\n\r\n" +
                "GStreamer can be downloaded from http://www.gstreamer.com/\r\n\r\n" +
                "See README.Windows for more information.")
    else:
        logging.info("PyGTK works")

# vi: et sts=4 sw=4 ts=4
