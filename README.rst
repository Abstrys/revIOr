######
revIOr
######

**revIOr** is the evolutionary successor to my older project, jOculus_. It is a light-text-markup
viewer with built-in support for Markdown_ and reStructuredText_, and supports other text processors
through its ability to use arbitrary command-line processors on your source files (it must emit
HTML, and use at your own risk, naturally).

It updates the display of a file whenever you save it (that is, whenever the file is updated on
disk), so you can edit your files using your favorite text editor and review the edits you make in
HTML (via WebKit) by simply saving the file.

A few default styles are included, but you can substitute your own ``.css`` stylesheets to view the
output exactly as it would on your website.

It's decidedly *alpha* right now, but it works in a rudimentary way.

@hat's *not* working (yet):

* The *open file* function.  I usually just open the file in my editor *first*, and *then* run
  revIOr on it.

* I need to create a theme for commonmark-processed Markdown, and my themes could be better.


How to install it
=================

For now, you must install from source if you want to try it. There are also a few prerequisites:

* Python3
* PyGObject
* WebKit2 (GTK)

On Fedora, for example, you can run::

     sudo dnf install gobject-introspection python3-gobject \
       python3-gobject-devel webkit2gtk3

Python's `commonmark` library is necessary to decode Markdown. To install it::

     pip3 install commonmark


How to use revIOr
=================

Start revIOr by either launching it alone or with a filename::

  revIOr <filename>

Once it is started, you can use the buttons in the toolbar to perform a few useful functions.

* Click the **open file** button to open a new file.
* Click the **edit file** button to open your configured editor on the currently-displayed file.
* Zoom in or out by pressing the **-** or **+** buttons.
* Click the **choose stylesheet** button to choose a different stylesheet.
* Click the **preferences** button to open the preferences.

Opening files
-------------

You can open a new file to view, or open the currently-viewed file in your editor.

To open a new file to view:

* Click the open file button.

To open the currently-viewed file in your configured editor:

* Click the edit file button.

Changing the display
--------------------


.. _joculus: https://github.com/Abstrys/joculus
.. _markdown: http://daringfireball.net/projects/markdown/
.. _restructuredtext: http://docutils.sourceforge.net/rst.html

