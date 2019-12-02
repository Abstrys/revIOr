# revIOr_window: contains the RevIOrWindow class.
import sys, os, subprocess
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import Gio
from gi.repository import WebKit2
from abstrys.app_settings import AppSettings
from abstrys.revIOr.prefs_dialog import RevIOrPrefsDialog

DEFAULT_CONTENTS = """
<head>
    <style>
        body { margin-left: '0.5in'; }
    </style>
</head>
<body>
    <h2>Welcome to revIOr!</h2>

    <p>revIOr is a viewer for Markdown and ReStructuredText that <em>automatically updates its
    view</em> whenever the displayed file changes.</p>

    <h3>Basic operation</h3>

    <p>To <em>load a file</em>, click the <strong>Open File</strong> button in the toolbar.</p>

    <p>You can <em>zoom the view out or in</em> using the plus (<strong>+</strong>) and minus
    (<strong>-</strong>) keys on your keyboard. You can press the equals key (<strong>=</strong>) to
    return the view to normal.</p>
</body>
"""

ABOUT_TEXT = """
A reStructuredText and Markdown reviewer.

by Eron Hennessey <eronh@abstrys.com>

http://github.com/Abstrys/revIOr

Provided free of use under the terms of the BSD
license.
"""

APP_NAME = 'revIOr'
DEFAULT_STYLESHEET_DIR = '~/.%s/css' % APP_NAME

class RevIOrWindow(Gtk.Window):
    """The main RevIOr window."""

    # the revIOr application
    oculus = None

    # UI elements
    toolbar = None
    view_box = None
    html_view = None
    html_text = None
    zoom_label = None

    # settings
    settings = None
    zoom_level = 1.0
    zoom_step = 0.01
    zoom_level_min = 0.25
    zoom_level_max = 4.0


    def __init__(self, oculus):
        """Initialize the window."""
        self.oculus = oculus
        self.settings = AppSettings(APP_NAME)

        Gtk.Window.__init__(self, title="%s - *no file loaded*" % APP_NAME)
        self.setup_document_view()
        self.setup_toolbar()
        self.set_window_size_pos()
        self.connect('key_press_event', self.on_key_press_event)


    def check_stylesheet_dir(self):
        """
        Return the stylesheet directory (either set in settings, or the default).

        If the default stylesheet directory doesn't exist yet, then create it and populate it!
        """
        stylesheet_dir_path = self.settings.get('stylesheet_dir')
        if stylesheet_dir_path is None:
            stylesheet_dir_path = os.path.join(self.settings.check_settings_dir(), 'css')
            # create the directory and populate it if the dir doesn't exist.
            if not os.path.isdir(stylesheet_dir_path):
                import pkg_resources, shutil
                css_src_dir = pkg_resources.resource_filename('abstrys.revIOr', 'css')
                shutil.copytree(css_src_dir, stylesheet_dir_path)
        return stylesheet_dir_path

                    
    def close(self):
        self.settings.save()


    def create_stock_toolbar_button(self, stock_item_id, button_handler,
            tooltip_text=None):
        b = Gtk.ToolButton.new_from_stock(stock_item_id)
        b.connect("clicked", button_handler)
        if tooltip_text is not None:
            b.set_tooltip_text(tooltip_text)
        return b


    def create_zoom_level_label(self):
        b = Gtk.ToolItem()
        l = Gtk.Label("zoom: 100%")
        # noinspection PyAttributeOutsideInit
        self.zoom_level_label = l
        b.add(l)
        return b


    def create_expanding_separator(self):
        s = Gtk.SeparatorToolItem()
        s.set_expand(True)
        return s


    def update_zoom_level(self):
        self.html_view.set_zoom_level(self.zoom_level)
        self.zoom_level_label.set_text("zoom: %d%%" % (self.zoom_level * 100))


    def setup_toolbar(self):
        tb = Gtk.Toolbar()
        self.view_box.pack_start(tb, expand=False, fill=True, padding=0)
        self.toolbar = tb

        tb.insert(self.create_stock_toolbar_button('gtk-open', self.cmd_open_file,
            "View a different file"), -1)

        tb.insert(self.create_stock_toolbar_button('gtk-edit', self.cmd_edit_file,
            "Edit the current file"), -1)

        tb.insert(self.create_expanding_separator(), -1)

        tb.insert(self.create_stock_toolbar_button('gtk-zoom-out', self.cmd_zoom_out,
            "Zoom out of the display (decrease text/image size)"), -1)

        tb.insert(self.create_zoom_level_label(), -1)

        tb.insert(self.create_stock_toolbar_button('gtk-zoom-in', self.cmd_zoom_in,
            "Zoom into the display (increase text/image size)."), -1)

        tb.insert(self.create_expanding_separator(), -1)

        tb.insert(self.create_stock_toolbar_button('gtk-page-setup', self.cmd_choose_stylesheet,
            "Choose a stylesheet"), -1)

        tb.insert(self.create_stock_toolbar_button('gtk-preferences', self.cmd_set_preferences,
            "Set preferences"), -1)

        tb.insert(self.create_stock_toolbar_button('gtk-about', self.cmd_show_about,
            "About %s" % APP_NAME), -1)



    def setup_document_view(self):
        self.view_box = Gtk.Box.new(Gtk.Orientation.VERTICAL, 0)
        self.html_view = WebKit2.WebView()

        ws = WebKit2.Settings()
        ws.set_auto_load_images(True)
        self.html_view.set_settings(ws)

        self.set_contents(DEFAULT_CONTENTS)

        self.view_box.pack_start(self.html_view, expand=True, fill=True, padding=0)
        self.add(self.view_box)


    def set_title(self, text):
        """Set the window title."""
        title_text = "%s - %s" % (APP_NAME, text)
        Gtk.Window.set_title(self, title_text)


    def set_window_size_pos(self):
        # if the user has a different window size that's preferred, use that.
        window_size = [425, 550] # 8.5x11 aspect ratio
        set_width = self.settings.get('width', window_size[0])
        set_height = self.settings.get('height', window_size[1])
        self.set_default_size(set_width, set_height)
        self.settings.update({'width': set_width, 'height': set_height})


    def set_contents(self, html_text):
        """Set the contents of the window to the text provided by html_text."""
        if html_text is None:
            return
        self.html_text = html_text
        self.html_view.load_html(self.html_text, None)


    def cmd_open_file(self, widget):
        """Open a file."""
        dlg = Gtk.FileChooserDialog(title="Choose a file to display",
                parent=self, action=Gtk.FileChooserAction.OPEN,
                buttons=(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                    Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        tf = Gtk.FileFilter()
        tf.set_name('Text files')
        tf.add_mime_type('text/plain')
        tf.add_pattern('*.rst')
        tf.add_pattern('*.md')
        tf.add_pattern('*.txt')
        dlg.add_filter(tf)
        af = Gtk.FileFilter()
        af.set_name('All files')
        af.add_pattern('*.*')
        dlg.add_filter(af)
        dlg.set_current_folder('.')
        response = dlg.run()
        if response == Gtk.ResponseType.OK:
            self.oculus.set_file(dlg.get_filename())
        dlg.destroy()


    def cmd_edit_file(self, widget):
        print("Edit File button pressed!")
        if self.oculus.cur_file_path == None:
            dlg = Gtk.MessageDialog(self, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, "Whoah, there.")
            dlg.format_secondary_text("No file is currently loaded! Can't edit nothin'...!")
            dlg.run()
            dlg.destroy()
        else:
            if hasattr(os, 'startfile'):
                    os.startfile(self.oculus.cur_file_path)
            elif sys.platform == 'linux':
                    subprocess.call(['xdg-open', self.oculus.cur_file_path])
            elif sys.platform == 'darwin':
                    subprocess.call(['open', self.oculus.cur_file_path]) 


    def cmd_show_about(self, widget):
        print("About button pressed!")
        dlg = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "About revIOr")
        dlg.format_secondary_text(ABOUT_TEXT)
        dlg.run()
        dlg.destroy()


    def cmd_choose_stylesheet(self, widget):
        print("Choose Stylesheet button pressed!")
        # if there is a default stylesheet location set, use that. Otherwise, use the default
        # location.
        stylesheet_dir_path = self.check_stylesheet_dir()

        dlg = Gtk.FileChooserDialog(title="Choose a stylesheet",
                parent=self, action=Gtk.FileChooserAction.OPEN,
                buttons=(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                    Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        tf = Gtk.FileFilter()
        tf.set_name('CSS files')
        tf.add_mime_type('text/css')
        tf.add_pattern('*.css')
        dlg.add_filter(tf)
        dlg.set_current_folder(stylesheet_dir_path)
        response = dlg.run()
        if response == Gtk.ResponseType.OK:
            self.settings['stylesheet'] = dlg.get_filename()
        dlg.destroy()


    def cmd_set_preferences(self, widget):
        print("Edit Preferences button pressed!")
        dlg = RevIOrPrefsDialog(self, self.settings)
        response = dlg.run()
        dlg.destroy()


    def cmd_zoom_out(self, widget):
        if widget is None:
            self.zoom_level -= self.zoom_step
        else:
            self.zoom_level -= self.zoom_step * 10

        if self.zoom_level < self.zoom_level_min:
            self.zoom_level = self.zoom_level_min
        self.update_zoom_level()


    def cmd_zoom_in(self, widget):
        if widget is None:
            self.zoom_level += self.zoom_step
        else:
            self.zoom_level += self.zoom_step * 10

        if self.zoom_level > self.zoom_level_max:
            self.zoom_level = self.zoom_level_max
        self.update_zoom_level()


    def cmd_zoom_normal(self, widget):
        self.zoom_level = 1.0
        self.update_zoom_level()


    def on_key_press_event(self, widget, event):
        """Handle key_press events."""
        keyname = Gdk.keyval_name(event.keyval)
        # zoom buttons.
        if keyname == 'minus':
            self.cmd_zoom_out(None)
        elif keyname == 'plus':
            self.cmd_zoom_in(None)
        elif keyname == 'equal':
            self.cmd_zoom_normal(None)


