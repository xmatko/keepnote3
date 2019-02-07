# Migrating Keepnote from GTK3 and Python3

* pyGTK (Python GTK+ 2.0 bindings) do not support Python 3
* PyGObject (Python GTK+ >=3.0 bindings) does support Python 2/3

Following these statements, we should first port Keepnote to GTK3,
using PyGObject with Python 2.x

Next, we will port to Python 3

## Part 1: Migrating to GTK+3 / PyGObject

Read the docs:
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

**Note**: pour python 3 (later)
* python3-gi
* python3-gi-cairo
