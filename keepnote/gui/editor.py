"""

    KeepNote
    Editor widget in main window

"""

#
#  KeepNote
#  Copyright (c) 2008-2009 Matt Rasmussen
#  Author: Matt Rasmussen <rasmus@alum.mit.edu>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 2 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301, USA.
#

import logging

# GObject introspection imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GObject, Gtk

# keepnote imports
import keepnote


_ = keepnote.translate


class KeepNoteEditor (Gtk.Box):
    """
    Base class for all KeepNoteEditors
    """

    def __init__(self, app):
        GObject.GObject.__init__(self, orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.logger = logging.getLogger('keepnote')
        self.logger.debug("keepnote.gui.editor.KeepNoteEditor.__init__()")
        self._app = app
        self._notebook = None
        self._textview = None
        self.show_all()

    def set_notebook(self, notebook):
        """Set notebook for editor"""

    def get_textview(self):
        return self._textview

    def is_focus(self):
        """Return True if text editor has focus"""
        return False

    def grab_focus(self):
        """Pass focus to textview"""

    def clear_view(self):
        """Clear editor view"""

    def view_nodes(self, nodes):
        """View a node(s) in the editor"""

    def save(self):
        """Save the loaded page"""

    def save_needed(self):
        """Returns True if textview is modified"""
        return False

    def load_preferences(self, app_pref, first_open=False):
        """Load application preferences"""

    def save_preferences(self, app_pref):
        """Save application preferences"""

    def add_ui(self, window):
        pass

    def remove_ui(self, window):
        pass

    def undo(self):
        pass

    def redo(self):
        pass


# add new signals to KeepNoteEditor
GObject.type_register(KeepNoteEditor)
GObject.signal_new("view-node", KeepNoteEditor, GObject.SignalFlags.RUN_LAST,
                   None, (object,))
GObject.signal_new("visit-node", KeepNoteEditor, GObject.SignalFlags.RUN_LAST,
                   None, (object,))
GObject.signal_new("modified", KeepNoteEditor, GObject.SignalFlags.RUN_LAST,
                   None, (object, bool))
GObject.signal_new("font-change", KeepNoteEditor, GObject.SignalFlags.RUN_LAST,
                   None, (object,))
GObject.signal_new("error", KeepNoteEditor, GObject.SignalFlags.RUN_LAST,
                   None, (str, object))
GObject.signal_new("child-activated", KeepNoteEditor, GObject.SignalFlags.RUN_LAST,
                   None, (object, object))
GObject.signal_new("window-request", KeepNoteEditor, GObject.SignalFlags.RUN_LAST,
                   None, (str,))
GObject.signal_new("make-link", KeepNoteEditor, GObject.SignalFlags.RUN_LAST,
                   None, ())
