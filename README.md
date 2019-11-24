# revIOr

**revIOr** is the evolutionary successor to my older project, [jOculus][]. It is a light-text-markup
viewer with built-in support for [Markdown][] and [reStructuredText][], and supports other text
processors through its ability to use arbitrary command-line processors on your source files (it
must emit HTML, and use at your own risk, naturally).

It updates the display of a file whenever you save it (that is, whenever the file is updated on
disk), so you can edit your files using your favorite text editor and review the edits you make in
HTML (via WebKit) by simply saving the file.

A few default styles are included, but you can substitute your own .css stylesheets to view the
output exactly as it would on your website.


## How to use revIOr

Start revIOr by either launching it alone or with a filename:

  revIOr <*filename*>

Once it is started, you can use the buttons in the toolbar to perform a few useful functions.

* Click the open file button to open a new file.
* Click the edit file button to open your configured editor on the currently-displayed file.
* Zoom in or out by pressing the **-** or **+** buttons.
* Click the choose stylesheet button to choose a different stylesheet.
* Click the preferences button to open the preferences.


### Opening files

You can open a new file to view, or open the currently-viewed file in your editor.

To open a new file to view:

* Click the open file button.

To open the currently-viewed file in your configured editor:

* Click the edit file button.


### Changing the display


[joculus]: https://github.com/Abstrys/joculus
[markdown]: http://daringfireball.net/projects/markdown/
[restructuredtext]: http://docutils.sourceforge.net/rst.html
