# AppSettings class - holds app settings for whatever app you desire.
#
# by Eron Hennessey
#
import sys, os
import json

SETTINGS_FILE_NAME = "settings.json"

class AppSettings(dict):
    """
    Holds app settings and can also load and save them.

    The settings file is always named like this:

        ~/.<app_name>/settings.json

    Where <app_name> is the same value you pass to AppSettings() when creating the object.
    """

    def __init__(self, app_name):
        """Initialize the AppSettings object with the app name. The settings
        are identified by it."""
        super().__init__()
        self.app_name = app_name
        self.loaded = False
        self.load()


    def check_settings_dir(self):
        settings_dir_path = os.path.join(os.path.expanduser('~'), "." + self.app_name)
        if not os.path.isdir(settings_dir_path):
            print("%s: Settings directory doesn't exist. Creating %s..." %
               (self.app_name, settings_dir_path))
            os.mkdir(settings_dir_path)
        return settings_dir_path


    def _open_settings_file(self, mode):
        # Open the settings file with the given mode (usually either 'rb' or
        # 'wb')
        settings_dir_path = self.check_settings_dir()
        settings_file_path = os.path.join(settings_dir_path, SETTINGS_FILE_NAME)
        return open(settings_file_path, mode)


    def load(self):
        """
        Loads the settings from the store (wherever that is).

        If the settings don't exist, that's OK, it'll be created on save().
        """
        try:
            settings_file = self._open_settings_file('r')
            self.update(json.load(settings_file))
            self.loaded = True
            settings_file.close()
        except:
            # it's fine if the file isn't there yet. Just don't initialize anything.
            pass


    def save(self):
        """Saves the settings to the store (wherever that is)."""
        settings_file = self._open_settings_file('w')
        json.dump(self, settings_file)
        settings_file.close()

