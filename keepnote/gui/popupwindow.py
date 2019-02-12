
# GObject introspection imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GObject, Gtk


class PopupWindow (Gtk.Window):
    """A customizable popup window"""

    def __init__(self, parent):
        GObject.GObject.__init__(self, Gtk.WindowType.POPUP)
        self.set_type_hint(Gdk.WindowTypeHint.MENU)
        self.set_transient_for(parent.get_toplevel())
        self.set_flags(Gtk.CAN_FOCUS)
        self.add_events(Gdk.EventMask.KEY_PRESS_MASK |
                        Gdk.EventMask.KEY_RELEASE_MASK)

        self._parent = parent
        self._parent.get_toplevel().connect("configure-event",
                                            self._on_configure_event)

        # coordinates of popup
        self._x = 0
        self._y = 0
        self._y2 = 0

    def _on_configure_event(self, widget, event):
        self.move_on_parent(self._x, self._y, self._y2)

    def move_on_parent(self, x, y, y2):
        """Move popup relative to parent widget"""

        win = self._parent.get_parent_window()
        if win is None:
            return

        # remember coordinates
        self._x = x
        self._y = y
        self._y2 = y2

        # get screen dimensions
        screenh = Gdk.Screen.height()

        # account for window
        wx, wy = win.get_origin()
        x3 = wx
        y3 = wy

        # account for widget
        rect = self._parent.get_allocation()
        x3 += rect.x
        y3 += rect.y

        # get size of popup
        w, h = self.get_child().size_request()
        self.resize(w, h)

        # perform move
        if y + y3 + h < screenh:
            # drop down
            self.move(x + x3, y + y3)
        else:
            # drop up
            self.move(x + x3, y2 + y3 - h)
