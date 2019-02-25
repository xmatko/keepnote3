# Migrating Keepnote from GTK3 and Python3

* pyGTK (Python GTK+ 2.0 bindings) do not support Python 3
* PyGObject (Python GTK+ >=3.0 bindings) does support Python 2/3

Following these statements, we should first port Keepnote to GTK3,
using PyGObject with Python 2.x

Next, we will port to Python 3

## Part 1: Migrating to GTK+3 / PyGObject

https://pygobject.readthedocs.io/en/latest/

* **[PyGObject API Refence](https://lazka.github.io/pgi-docs)**

**Howto's**

* [Porting from Static Bindings](https://pygobject.readthedocs.io/en/latest/guide/porting.html)  part of the PyGObject documentation, focusing on Python
* [PyGObject - Introspection Porting](https://wiki.gnome.org/action/show/Projects/PyGObject/IntrospectionPorting?action=show&redirect=PyGObject%2FIntrospectionPorting) on the GNOME Wiki, focusing on Python
* [GTK3 Porting guide](https://developer.sugarlabs.org/src/gtk3-porting-guide.md.html) from Sugar Toolkit developpers site


### PyGObject converting script

[https://gitlab.gnome.org/GNOME/pygobject/raw/master/tools/pygi-convert.sh](https://gitlab.gnome.org/GNOME/pygobject/raw/master/tools/pygi-convert.sh)

	./pygi-convert.sh mymodule.py


### Dependencies (Debian)
* python-gi
* python-gi-cairo
* python-gi-dev ?

### Misc
#### gettext
[https://stackoverflow.com/questions/10094335/how-to-bind-a-text-domain-to-a-local-folder-for-gettext-under-gtk3](https://stackoverflow.com/questions/10094335/how-to-bind-a-text-domain-to-a-local-folder-for-gettext-under-gtk3)

seen in keepnote.gui.__init__

#### lambda func
https://medium.com/@happymishra66/lambda-map-and-filter-in-python-4935f248593

#### Gtk.Builder connect signals to callback
* [Connect signal callback to each object individually](https://stackoverflow.com/questions/51953389/gtk-glade-and-python-connecting-handlers-from-multiple-classes-with-the-connect)

#### Gtk.GenericTreeView
* [Simple script demonstrating a custom Gtk.TreeModel for Gtk 3 (known as GenericTreeModel in PyGtk 2).](
https://gist.github.com/andialbrecht/4463278)
* [python - GenericTreeModel with PyGObject Introspection Gtk+ 3? - Stack Overflow](https://stackoverflow.com/questions/11025700/generictreemodel-with-pygobject-introspection-gtk-3)
* [gtk.GenericTreeModel](https://developer.gnome.org/pygtk/stable/class-pygtkgenerictreemodel.html))
* [14.11. Le TreeModel générique](http://mcclinews.free.fr/python/pygtktutfr/sec-GenericTreeModel.html)

https://stackoverflow.com/questions/11178743/gtk-3-0-how-to-use-a-gtk-treestore-with-custom-model-items

#### VBox/HBox
    GObject.GObject.__init__(self, orientation=Gtk.Orientation.VERTICAL, spacing=0)

## Python 3
### Dependencies (Debian)
* python3-gi
* python3-gi-cairo

## Docs

Using Sphinx: <https://gisellezeno.com/tutorials/sphinx-for-python-documentation.html>
