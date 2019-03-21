"""

    KeepNote
    Color picker for the toolbar

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
from gi.repository import GObject, Gtk, Gdk, Pango
try:
    gi.require_foreign("cairo")
    import cairo
except ImportError:
    print("No pycairo integration :(")

# keepnote imports
import keepnote
_ = keepnote.translate


#=============================================================================
# constants

FONT_LETTER = "A"


DEFAULT_COLORS_FLOAT = [
    # lights
    (1, .6, .6),
    (1, .8, .6),
    (1, 1, .6),
    (.6, 1, .6),
    (.6, 1, 1),
    (.6, .6, 1),
    (1, .6, 1),

    # trues
    (1, 0, 0),
    (1, .64, 0),
    (1, 1, 0),
    (0, 1, 0),
    (0, 1, 1),
    (0, 0, 1),
    (1, 0, 1),

    # darks
    (.5, 0, 0),
    (.5, .32, 0),
    (.5, .5, 0),
    (0, .5, 0),
    (0, .5, .5),
    (0, 0, .5),
    (.5, 0, .5),

    # white, gray, black
    (1, 1, 1),
    (.9, .9, .9),
    (.75, .75, .75),
    (.5, .5, .5),
    (.25, .25, .25),
    (.1, .1, .1),
    (0, 0, 0),
]


#=============================================================================
# color conversions

def color_float_to_int8(color):
    return (int(255*color[0]), int(255*color[1]), int(255*color[2]))


def color_float_to_int16(color):
    return (int(65535*color[0]), int(65535*color[1]), int(65535*color[2]))


def color_int8_to_int16(color):
    return (256*color[0], 256*color[1], 256*color[2])


def color_int16_to_int8(color):
    return (color[0]//256, color[1]//256, color[2]//256)


def color_str_to_int8(colorstr):

    # "#AABBCC" ==> (170, 187, 204)
    return (int(colorstr[1:3], 16),
            int(colorstr[3:5], 16),
            int(colorstr[5:7], 16))


def color_str_to_int16(colorstr):

    # "#AABBCC" ==> (43520, 47872, 52224)
    return (int(colorstr[1:3], 16)*256,
            int(colorstr[3:5], 16)*256,
            int(colorstr[5:7], 16)*256)


def color_int16_to_str(color):
    return "#%02x%02x%02x" % (color[0]//256, color[1]//256, color[2]//256)


def color_int8_to_str(color):
    return "#%02x%02x%02x" % (color[0], color[1], color[2])

def color_str_to_float(colorstr):
    return (float(int(colorstr[1:3], 16)) / 256.0,
        float(int(colorstr[3:5], 16)) / 256.0,
        float(int(colorstr[5:7], 16)) / 256.0)

# convert to str
DEFAULT_COLORS = [color_int8_to_str(color_float_to_int8(color))
                  for color in DEFAULT_COLORS_FLOAT]


#=============================================================================
# color menus

class ColorTextImage (Gtk.Image):
    """Image widget that display a color box with and without text"""

    def __init__(self, width, height, letter, border=True):
        Gtk.Image.__init__(self)
        self.logger = logging.getLogger('keepnote')
        #self.logger.debug("keepnote.gui.colortool.ColorTextImage.__init__()")
        self.width = width
        self.height = height
        self.letter = letter
        self.border = border
        self.marginx = 0.0
        self.marginy = 0.0
        self._pixmap = None
        self._gc = None
        self.fg_color = "#000000"
        self.bg_color = "#FFFFFF"
        self._border_color = "#000000"
        self._exposed = False

        self.connect("parent-set", self.on_parent_set)
        self.connect("draw", self.on_expose_event)

    def on_parent_set(self, widget, old_parent):
        self._exposed = False

    def on_expose_event(self, widget, event):
        """Set up colors on exposure"""
        if not self._exposed:
            #self.logger.debug("keepnote.gui.colortool.ColorTextImage2.on_expose_event() :  _exposed")
            self._exposed = True
            self.init_colors()

    def init_colors(self):
        #self.logger.debug("keepnote.gui.colortool.ColorTextImage2.init_colors()")
        self._pixmap = cairo.ImageSurface(cairo.Format.ARGB32, self.width, self.height)
        self._gc = cairo.Context(self._pixmap)
        self.refresh()

    def set_fg_color(self, color, refresh=True):
        """Set the color of the color chooser"""
        #self.logger.debug("keepnote.gui.colortool.ColorTextImage2.set_fg_color() : %s" % str(color))
        self.fg_color = color
        if refresh:
            self.refresh()

    def set_bg_color(self, color, refresh=True):
        """Set the color of the color chooser"""
        #self.logger.debug("keepnote.gui.colortool.ColorTextImage2.set_bg_color() : %s" % str(color))
        self.bg_color = color
        if refresh:
            self.refresh()

    def refresh(self):
        if self._gc:
            self.logger.debug("keepnote.gui.colortool.ColorTextImage2.refresh() : %s" % str(self.bg_color))
            self._gc.rectangle(0, 0, self.width, self.height)
            color = color_str_to_float(self.bg_color)
            self._gc.set_source_rgba(color[0], color[1], color[2], 1.0)
            self._gc.fill()

            if self.border:
                self._gc.set_line_width(1)
                color = color_str_to_float(self._border_color)
                self._gc.set_source_rgba(color[0], color[1], color[2], 1.0)
                self._gc.rectangle(0, 0, self.width, self.height)
                self._gc.stroke()

            if self.letter:
                self._gc.select_font_face("Serif", cairo.FontSlant.NORMAL, cairo.FontWeight.BOLD)
                self._gc.set_font_size(self.width)
                self._gc.set_antialias(cairo.Antialias.SUBPIXEL)
                x_bearing, y_bearing, letter_width, letter_height = self._gc.text_extents(FONT_LETTER)[:4]
                self.marginx = ((float(self.width) - letter_width)/2.0) - x_bearing
                self.marginy = float(self.height) - ((self.height - letter_height)/2.0)
                '''
                self.logger.debug("LETTER X: frame_width=%f, letter_width=%f, x_bearing=%f, x_margin=%f" % 
                        (self.width, letter_width, x_bearing, self.marginx))
                self.logger.debug("LETTER Y: frame_height=%f, letter_height=%f, y_bearing=%f, y_margin=%f" % 
                        (self.height, letter_height, y_bearing, self.marginy))
                '''
                color = color_str_to_float(self.fg_color)
                self._gc.set_source_rgba(color[0], color[1], color[2], 1.0)
                self._gc.move_to(self.marginx, self.marginy)
                self._gc.show_text(FONT_LETTER)

            self.set_from_surface(self._pixmap)


class ColorMenu (Gtk.Menu):
    """Color picker menu"""

    def __init__(self, colors=DEFAULT_COLORS):
        Gtk.Menu.__init__(self)
        self.logger = logging.getLogger('keepnote')
        self.logger.debug("keepnote.gui.colortool.ColorMenu.__init__()")
        self.width = 7
        self.posi = 4
        self.posj = 0
        self.color_items = []

        no_color = Gtk.MenuItem("_Default Color")
        no_color.show()
        no_color.connect("activate", self.on_no_color)
        self.attach(no_color, 0, self.width, 0, 1)

        # new color
        new_color = Gtk.MenuItem("_New Color...")
        new_color.show()
        new_color.connect("activate", self.on_new_color)
        self.attach(new_color, 0, self.width, 1, 2)

        # grab color
        #new_color = Gtk.MenuItem("_Grab Color")
        #new_color.show()
        #new_color.connect("activate", self.on_grab_color)
        #self.attach(new_color, 0, self.width, 2, 3)

        # separator
        item = Gtk.SeparatorMenuItem()
        item.show()
        self.attach(item, 0, self.width,  3, 4)

        # default colors
        self.set_colors(colors)

    def on_new_color(self, menu):
        """Callback for new color"""
        dialog = ColorSelectionDialog("Choose color")
        dialog.set_modal(True)
        dialog.set_transient_for(self.get_toplevel())  # TODO: does this work?
        dialog.set_colors(self.colors)

        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            color = dialog.colorsel.get_current_color()
            color = color_int16_to_str((color.red, color.green, color.blue))
            self.set_colors(dialog.get_colors())

            # add new color to palette
            if color not in self.colors:
                self.colors.append(color)
                self.append_color(color)

            self.emit("set-colors", self.colors)
            self.emit("set-color", color)

        dialog.destroy()

    def on_no_color(self, menu):
        """Callback for no color"""
        self.emit("set-color", None)

    def on_grab_color(self, menu):
        pass
        # TODO: complete

    def clear_colors(self):
        """Clears color palette"""
        children = set(self.get_children())
        for item in reversed(self.color_items):
            if item in children:
                self.remove(item)
        self.posi = 4
        self.posj = 0
        self.color_items = []
        self.colors = []

    def set_colors(self, colors):
        """Sets color palette"""
        self.logger.debug("keepnote.gui.colortool.ColorMenu.set_colors(): %s" % str(colors))
        self.clear_colors()

        self.colors = list(colors)
        for color in self.colors:
            self.append_color(color, False)

        # TODO: add check for visible
        # make change visible
        self.unrealize()
        self.realize()

    def get_colors(self):
        """Returns color palette"""
        return self.colors

    def append_color(self, color, refresh=True):
        """Appends color to menu"""
        #self.logger.debug("keepnote.gui.colortool.ColorMenu.append_color()")
        self.add_color(self.posi, self.posj, color, refresh=refresh)
        self.posj += 1
        if self.posj >= self.width:
            self.posj = 0
            self.posi += 1

    def add_color(self, i, j, color, refresh=True):
        """Add color to location in the menu"""
        #self.logger.debug("keepnote.gui.colortool.ColorMenu.add_color() : %s" % str(color))
        if refresh:
            self.unrealize()

        child = Gtk.MenuItem("")
        child.remove(child.get_child())
        img = ColorTextImage(15, 15, False)
        img.set_bg_color(color)
        child.add(img)
        child.get_child().show()
        child.show()
        child.connect("activate", lambda w: self.emit("set_color", color))
        self.attach(child, j, j+1, i, i+1)
        self.color_items.append(child)

        if refresh:
            self.realize()


GObject.type_register(ColorMenu)
GObject.signal_new("set-color", ColorMenu, GObject.SignalFlags.RUN_LAST,
                   None, (object,))
GObject.signal_new("set-colors", ColorMenu, GObject.SignalFlags.RUN_LAST,
                   None, (object,))
GObject.signal_new("get-colors", ColorMenu, GObject.SignalFlags.RUN_LAST,
                   None, (object,))


#=============================================================================
# color selection ToolBarItem


class ColorTool (Gtk.MenuToolButton):
    """Abstract base class for a ColorTool"""

    def __init__(self, icon, default):
        Gtk.MenuToolButton.__init__(self, icon_widget=self.icon, label="")
        self.icon = icon
        self.color = None
        self.colors = DEFAULT_COLORS
        self.default = default
        self.default_set = True

        # menu
        self.menu = ColorMenu([])
        self.menu.connect("set-color", self.on_set_color)
        self.menu.connect("set-colors", self.on_set_colors)
        self.set_menu(self.menu)

        self.connect("clicked", self.use_color)
        self.connect("show-menu", self.on_show_menu)

    def on_set_color(self, menu, color):
        """Callback from menu when color is set"""
        raise Exception("unimplemented")

    def on_set_colors(self, menu, color):
        """Callback from menu when palette is set"""
        self.colors = list(self.menu.get_colors())
        self.emit("set-colors", self.colors)

    def set_colors(self, colors):
        """Sets palette"""
        self.colors = list(colors)
        self.menu.set_colors(colors)

    def get_colors(self):
        return self.colors

    def use_color(self, menu):
        """Callback for when button is clicked"""
        self.emit("set-color", self.color)

    def set_default(self, color):
        """Set default color"""
        self.default = color
        if self.default_set:
            self.icon.set_fg_color(self.default)

    def on_show_menu(self, widget):
        """Callback for when menu is displayed"""
        self.emit("get-colors")
        self.menu.set_colors(self.colors)


GObject.type_register(ColorTool)
GObject.signal_new("set-color", ColorTool, GObject.SignalFlags.RUN_LAST,
                   None, (object,))
GObject.signal_new("set-colors", ColorTool, GObject.SignalFlags.RUN_LAST,
                   None, (object,))
GObject.signal_new("get-colors", ColorTool, GObject.SignalFlags.RUN_LAST,
                   None, ())


class FgColorTool (ColorTool):
    """ToolItem for choosing the foreground color"""

    def __init__(self, width, height, default):
        self.icon = ColorTextImage(width, height, True, True)
        self.icon.set_fg_color(default)
        self.icon.set_bg_color("#ffffff")
        ColorTool.__init__(self, self.icon, default)

    def on_set_color(self, menu, color):
        """Callback from menu"""
        if color is None:
            self.default_set = True
            self.icon.set_fg_color(self.default)
        else:
            self.default_set = False
            self.icon.set_fg_color(color)

        self.color = color
        self.emit("set-color", color)


class BgColorTool (ColorTool):
    """ToolItem for choosing the backgroundground color"""

    def __init__(self, width, height, default):
        self.icon = ColorTextImage(width, height, False, True)
        self.icon.set_bg_color(default)
        ColorTool.__init__(self, self.icon, default)

    def on_set_color(self, menu, color):
        """Callback from menu"""
        if color is None:
            self.default_set = True
            self.icon.set_bg_color(self.default)
        else:
            self.default_set = False
            self.icon.set_bg_color(color)

        self.color = color
        self.emit("set-color", color)


#=============================================================================
# color selection dialog and palette


class ColorSelectionDialog (Gtk.ColorSelectionDialog):

    def __init__(self, title="Choose color"):
        Gtk.ColorSelectionDialog.__init__(self, title)
        self.colorsel.set_has_opacity_control(False)

        # hide default gtk palette
        self.colorsel.set_has_palette(False)

        # structure of ColorSelection widget
        # colorsel = VBox(HBox(selector, VBox(Table, VBox(Label, palette),
        #                                     my_palette)))
        # palette = Table(Frame(DrawingArea), ...)
        #
        #vbox = (self.colorsel.get_children()[0]
        #        .get_children()[1].get_children()[1])
        #palette = vbox.get_children()[1]

        vbox = self.colorsel.get_children()[0].get_children()[1]

        # label
        label = Gtk.Label(label=_("Pallete:"))
        label.set_alignment(0, .5)
        label.show()
        vbox.pack_start(label, expand=False, fill=True, padding=0)

        # palette
        self.palette = ColorPalette(DEFAULT_COLORS)
        self.palette.connect("pick-color", self.on_pick_palette_color)
        self.palette.show()
        vbox.pack_start(self.palette, expand=False, fill=True, padding=0)

        # palette buttons
        hbox = Gtk.HButtonBox()
        hbox.show()
        vbox.pack_start(hbox, expand=False, fill=True, padding=0)

        # new color
        button = Gtk.Button("new", stock=Gtk.STOCK_NEW)
        button.set_relief(Gtk.ReliefStyle.NONE)
        button.connect("clicked", self.on_new_color)
        button.show()
        hbox.pack_start(button, expand=False, fill=False, padding=0)

        # delete color
        button = Gtk.Button("delete", stock=Gtk.STOCK_DELETE)
        button.set_relief(Gtk.ReliefStyle.NONE)
        button.connect("clicked", self.on_delete_color)
        button.show()
        hbox.pack_start(button, expand=False, fill=False, padding=0)

        # reset colors
        button = Gtk.Button(stock=Gtk.STOCK_UNDO)
        (button.get_children()[0].get_child()
         .get_children()[1].set_text_with_mnemonic("_Reset"))
        button.set_relief(Gtk.ReliefStyle.NONE)
        button.connect("clicked", self.on_reset_colors)
        button.show()
        hbox.pack_start(button, expand=False, fill=False, padding=0)

        # colorsel signals
        def func(w):
            color = self.colorsel.get_current_color()
            self.palette.set_color(
                color_int16_to_str((color.red, color.green, color.blue)))
        self.colorsel.connect("color-changed", func)

    def set_colors(self, colors):
        """Set palette colors"""
        self.palette.set_colors(colors)

    def get_colors(self):
        """Get palette colors"""
        return self.palette.get_colors()

    def on_pick_palette_color(self, widget, color):
        self.colorsel.set_current_color(Gdk.Color(color))

    def on_new_color(self, widget):
        color = self.colorsel.get_current_color()
        self.palette.new_color(
            color_int16_to_str((color.red, color.green, color.blue)))

    def on_delete_color(self, widget):
        self.palette.remove_selected()

    def on_reset_colors(self, widget):
        self.palette.set_colors(DEFAULT_COLORS)


class ColorPalette (Gtk.IconView):
    def __init__(self, colors=DEFAULT_COLORS, nrows=1, ncols=7):
        Gtk.IconView.__init__(self)
        self._model = Gtk.ListStore(GdkPixbuf.Pixbuf, object)
        self._cell_size = [30, 20]

        self.set_model(self._model)
        self.set_reorderable(True)
        self.set_property("columns", 7)
        self.set_property("spacing", 0)
        self.set_property("column-spacing", 0)
        self.set_property("row-spacing", 0)
        self.set_property("item-padding", 1)
        self.set_property("margin", 1)
        self.set_pixbuf_column(0)

        self.connect("selection-changed", self._on_selection_changed)

        self.set_colors(colors)

        # TODO: could ImageColorText become a DrawingArea widget?

    def clear_colors(self):
        """Clears all colors from palette"""
        self._model.clear()

    def set_colors(self, colors):
        """Sets colors in palette"""
        self.clear_colors()
        for color in colors:
            self.append_color(color)

    def get_colors(self):
        """Returns colors in palette"""
        colors = []
        self._model.foreach(
            lambda m, p, i: colors.append(m.get_value(i, 1)))
        return colors

    def append_color(self, color):
        """Append color to palette"""
        width, height = self._cell_size

        # make pixbuf
        pixbuf = GdkPixbuf.Pixbuf(
            GdkPixbuf.Colorspace.RGB, False, 8, width, height)
        self._draw_color(pixbuf, color, 0, 0, width, height)

        self._model.append([pixbuf, color])

    def remove_selected(self):
        """Remove selected color"""
        for path in self.get_selected_items():
            self._model.remove(self._model.get_iter(path))

    def new_color(self, color):
        """Adds a new color"""
        self.append_color(color)
        n = self._model.iter_n_children(None)
        self.select_path((n-1,))

    def set_color(self, color):
        """Sets the color of the selected cell"""
        width, height = self._cell_size

        it = self._get_selected_iter()
        if it:
            pixbuf = self._model.get_value(it, 0)
            self._draw_color(pixbuf, color, 0, 0, width, height)
            self._model.set_value(it, 1, color)

    def _get_selected_iter(self):
        """Returns the selected cell (TreeIter)"""
        for path in self.get_selected_items():
            return self._model.get_iter(path)
        return None

    def _on_selection_changed(self, view):
        """Callback for when selection changes"""
        it = self._get_selected_iter()
        if it:
            color = self._model.get_value(it, 1)
            self.emit("pick-color", color)

    def _draw_color(self, pixbuf, color, x, y, width, height):
        """Draws a color cell"""
        border_color = "#000000"

        # create pixmap
        pixmap = Gdk.Pixmap(None, width, height, 24)
        cmap = pixmap.get_colormap()
        gc = pixmap.new_gc()
        color1 = cmap.alloc_color(color)
        color2 = cmap.alloc_color(border_color)

        # draw fill
        gc.foreground = color1  # Gdk.Color(* color)
        pixmap.draw_rectangle(gc, True, 0, 0, width, height)

        # draw border
        gc.foreground = color2  # Gdk.Color(* border_color)
        pixmap.draw_rectangle(gc, False, 0, 0, width-1, height-1)

        pixbuf.get_from_drawable(pixmap, cmap, 0, 0, 0, 0, width, height)


GObject.type_register(ColorPalette)
GObject.signal_new("pick-color", ColorPalette, GObject.SignalFlags.RUN_LAST,
                   None, (object,))

# vim: ft=python: set et ts=4 sw=4 sts=4:
