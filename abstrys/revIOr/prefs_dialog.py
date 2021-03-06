# prefs_dialog: The preferences dialog for the revIOr application.
# by Eron Hennessey

from gi.repository import Gtk
from abstrys.app_settings import AppSettings

class RevIOrPrefsDialog(Gtk.Dialog):

    def __init__(self, parent, settings):
        Gtk.Dialog.__init__(self, "revIOr Preferences", parent, 0, (Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK))

        if type(settings) is not AppSettings:
            dlg = Gtk.MessageDialog(self, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, "Whoah, there.")
            dlg.format_secondary_text("RevIOrPrefsDialog -- wrong settings object passed!")
            dlg.run()
            dlg.destroy()

        self.settings = settings

        # add a box for laying out the controls.
        self.listbox = Gtk.ListBox()
        self.get_content_area().add(self.listbox)
        
        # save_position_on_exit - True or False.
        row = Gtk.ListBoxRow()
        box = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, spacing=20)
        row.add(box)
        label = Gtk.Label("Save window position on exit", xalign=0)
        self.control_save_window_pos = Gtk.CheckButton.new()
        self.control_save_window_pos.set_active(self.settings.get('save_window_pos', False)) 
        box.pack_start(label, True, True, 0)
        box.pack_start(self.control_save_window_pos, False, True, 0)
        self.listbox.add(row)

        # save_size_on_exit - True or False
        row = Gtk.ListBoxRow()
        box = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, spacing=20)
        row.add(box)
        label = Gtk.Label("Save window size on exit", xalign=0)
        self.control_save_window_size = Gtk.CheckButton.new()
        self.control_save_window_size.set_active(self.settings.get('save_window_size', False))
        box.pack_start(label, True, True, 0)
        box.pack_start(self.control_save_window_size, False, True, 0)
        self.listbox.add(row)

        cur_size = parent.get_size()
        min_size = parent.get_preferred_size()[0]

        # default_width - the default width of the window
        row = Gtk.ListBoxRow()
        box = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, spacing=20)
        row.add(box)
        label = Gtk.Label("Starting window width", xalign=0)
        self.control_start_width = Gtk.SpinButton.new_with_range(min_size.height, 2000, 1)
        self.control_start_width.set_value(cur_size[0])
        box.pack_start(label, True, True, 0)
        box.pack_start(self.control_start_width, False, True, 0)
        self.listbox.add(row)

        # default_height - the default height of the window
        row = Gtk.ListBoxRow()
        box = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, spacing=20)
        row.add(box)
        label = Gtk.Label("Starting window height", xalign=0)
        self.control_start_height = Gtk.SpinButton.new_with_range(min_size.width, 1000, 1)
        self.control_start_height.set_value(cur_size[1])
        box.pack_start(label, True, True, 0)
        box.pack_start(self.control_start_height, False, True, 0)
        self.listbox.add(row)

        # editor - the editor to use when "edit file" is pressed.
        row = Gtk.ListBoxRow()
        box = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, spacing=20)
        row.add(box)
        label = Gtk.Label("Text editor for opening files", xalign=0)
        self.control_text_editor = Gtk.AppChooserButton.new("text/plain")
        # todo: choose the configured text editor (if any) and make that the current setting.
        box.pack_start(label, True, True, 0)
        box.pack_start(self.control_text_editor, False, True, 0)
        self.listbox.add(row)

        # stylesheet_dir - where the stylesheets are loaded from.
        row = Gtk.ListBoxRow()
        box = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, spacing=20)
        row.add(box)
        label = Gtk.Label("Stylesheet directory", xalign=0)
        self.control_stylesheet_dir = Gtk.FileChooserButton.new("choose a directory", Gtk.FileChooserAction.SELECT_FOLDER)
        self.control_stylesheet_dir.set_current_folder(self.settings.get('stylesheet_dir', '.'))
        box.pack_start(label, True, True, 0)
        box.pack_start(self.control_stylesheet_dir, False, True, 0)
        self.listbox.add(row)

        self.show_all()


    def update_settings(self):
        # update the setttings and save them.
        self.settings['start_width'] = self.control_start_width.get_value()
        self.settings['start_height'] = self.control_start_height.get_value()
        self.settings['save_window_pos'] = self.control_save_window_pos.get_active()
        self.settings['save_window_size'] = self.control_save_window_size.get_active()
        self.settings['text_editor'] = self.control_text_editor.get_app_info().get_commandline()
        self.settings['stylesheet_dir'] = self.control_stylesheet_dir.get_filename()
        self.settings.save()
        return self.settings

