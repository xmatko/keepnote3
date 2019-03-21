"""

    KeepNote
    TreeView

"""
#
#  KeepNote
#  Copyright (c) 2008-2011 Matt Rasmussen
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
from gi.repository import GObject, Gtk, Gdk

# keepnote imports
from keepnote.gui import treemodel
from keepnote.gui import basetreeview


class KeepNoteTreeView (basetreeview.KeepNoteBaseTreeView):
    """
    TreeView widget for the KeepNote NoteBook
    """

    def __init__(self):
        self.logger = logging.getLogger('keepnote')
        self.logger.debug("keepnote.gui.treeview.KeepNoteTreeView.__init__()")
        basetreeview.KeepNoteBaseTreeView.__init__(self)

        self._notebook = None

        self.logger.debug("\n$$$\n$$$ INSTANTIATE MODEL from KeepNoteTreeView\n$$$")
        model = treemodel.KeepNoteTreeModel()
        self.logger.debug("\n$$$\n$$$ INSTANTIATE MODEL from KeepNoteTreeView  DONE\n$$$")
        self.logger.debug("\n$$$\n$$$ set_model() from KeepNoteTreeView\n$$$")
        self.set_model(model)
        self.logger.debug("\n$$$\n$$$ set_model() DONE\n$$$")

        # treeview signals
        self.logger.debug("$$$ connect signals()")
        self.connect("key-release-event", self.on_key_released)
        self.connect("button-press-event", self.on_button_press)
        self.logger.debug("$$$ DONE")

        # selection config
        self.logger.debug("$$$ set_mode()")
        self.get_selection().set_mode(Gtk.SelectionMode.MULTIPLE)
        self.logger.debug("$$$ DONE")

        self.set_headers_visible(False)

        # tree style
        self.set_property("enable-tree-lines", True)

        self.logger.debug("\n$$$\n$$$ _setup_columns()\n$$$")
        self._setup_columns()
        self.logger.debug("\n$$$\n$$$ _setup_columns() DONE\n$$$")
        self.set_sensitive(False)
        self.logger.debug("\n$$$ keepnote.gui.treeview.KeepNoteTreeView.__init__()  DONE\n\n")

    def load_preferences(self, app_pref, first_open=False):
        """Load application preferences"""
        pass

    def save_preferences(self, app_pref):
        """Save application preferences"""
        pass

    def _setup_columns(self):

        self.logger.debug("keepnote.gui.treeview.TreeView._setup_columns()")
        self.clear_columns()

        if self._notebook is None:
            return

        # create the treeview column
        self.column = Gtk.TreeViewColumn()
        self.column.set_clickable(False)
        self.append_column(self.column)

        self._add_model_column("title")
        self._add_title_render(self.column, "title")

        # make treeview searchable
        self.set_search_column(self.model.get_column_by_name("title").pos)
        #self.set_fixed_height_mode(True)
        self.logger.debug("keepnote.gui.treeview.TreeView._setup_columns()  DONE")

    #=============================================
    # gui callbacks

    def on_key_released(self, widget, event):
        """Process key presses"""
        # no special processing while editing nodes
        if self.editing_path:
            return

        if event.keyval == Gdk.KEY_Delete:
            self.emit("delete-node", self.get_selected_nodes())
            self.stop_emission("key-release-event")

    def on_button_press(self, widget, event):
        """Process context popup menu"""
        if event.button == 3:
            # popup menu
            return self.popup_menu(event.x, event.y, event.button, event.time)

        if event.button == 1 and event.type == Gdk.EventType.BUTTON_PRESS:
            nodes = self.get_selected_nodes()
            if len(nodes) > 0:
                # double click --> goto node
                self.emit("activate-node", nodes[0])

    #==============================================
    # actions

    def set_notebook(self, notebook):
        basetreeview.KeepNoteBaseTreeView.set_notebook(self, notebook)
        self.logger.debug("keepnote.gui.treeview.TreeView.set_notebook() notebook: %s" % str(notebook))
        self.logger.debug("keepnote.gui.treeview.TreeView.set_notebook() self._notebook: %s" % str(self._notebook))

        if self._notebook is None:
            self.model.set_root_nodes([])
            self.set_sensitive(False)

        else:
            self.set_sensitive(True)

            root = self._notebook
            model = self.model

            self.set_model(None)
            model.set_root_nodes([root])
            self.set_model(model)

            self._setup_columns()

            if root.get_attr("expanded", True):
                #self.expand_to_path((0,))
                self.expand_to_path(Gtk.TreePath.new_from_indices((0,)))

        self.logger.debug("keepnote.gui.treeview.TreeView.set_notebook()  DONE\n")

    def save(self):
        """Fake function"""
        pass

    def edit_node(self, node):
        path = treemodel.get_path_from_node(
            self.model, node,
            self.rich_model.get_node_column_pos())
        GObject.idle_add(lambda: self.set_cursor_on_cell(
            Gtk.TreePath.new_from_indices(path), self.column, self.title_text, True))
        #GObject.idle_add(lambda: self.scroll_to_cell(path))

# vim: ft=python: set et ts=4 sw=4 sts=4:
