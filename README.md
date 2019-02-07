# [KeepNote3](http://keepnote.org)

This is an attempt to port the original [KeepNote](http://keepnote.org) on GTK+3 / Python 3

The original KeepNote is copyrighted by [Matt Rasmussen](matt.rasmus@gmail.com) and the source code is available on [GitHub](https://github.com/mdrasmus/keepnote)

As this project seems inactive since 2015, I decided to fork and rename it. By the power of the three, this fork is called **KeepNote3** (say *KeepNoteCube*)

KeepNote was originaly designed to be cross-platform (implemented in Python and PyGTK) and stores your notes in simple and easy to manipulate file formats (HTML and XML).

## Porting notes
* pyGTK (Python GTK+ 2.0 bindings) do not support Python 3
* PyGObject (Python GTK+ >=3.0 bindings) does support Python 2/3

Following these statements, we should first port Keepnote to GTK3,
using PyGObject with Python 2.x

Next, we will port to Python 3

### Part 1: Migrating to GTK+3 / PyGObject

Read the docs:
* [Porting from Static Bindings](https://pygobject.readthedocs.io/en/latest/guide/porting.html)  part of the PyGObject documentation, focusing on Python
* [PyGObject - Introspection Porting](https://wiki.gnome.org/action/show/Projects/PyGObject/IntrospectionPorting?action=show&redirect=PyGObject%2FIntrospectionPorting) on the GNOME Wiki, focusing on Python
* [GTK3 Porting guide](https://developer.sugarlabs.org/src/gtk3-porting-guide.md.html) from Sugar Toolkit developpers site

#### PyGObject converting script

[https://gitlab.gnome.org/GNOME/pygobject/raw/master/tools/pygi-convert.sh](https://gitlab.gnome.org/GNOME/pygobject/raw/master/tools/pygi-convert.sh)

	./pygi-convert.sh mymodule.py

#### Dependencies (Debian)
* python-gi


## Further information

- Install instructions: [INSTALL.md](INSTALL.md)
- Development instructions: [DEVELOP.md](DEVELOP.md)
- License information: [LICENSE](LICENSE) - MIT and GPLv2
- Change log of features and bug fixes: [CHANGES](CHANGES)
- Language translation information: [README.translations.txt](README.translations.txt)

