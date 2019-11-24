#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==============================================================================
#
# revIOr application code
#
# Copyright © 2019, Eron Hennessey / Abstrys
#
# This software is distributed under the BSD3 license, see LICENSE for details.
#
# ==============================================================================

import sys
import os.path
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('WebKit2', '4.0')
from gi.repository import Gtk
from gi.repository import GLib
import abstrys.revIOr.text_processors as text_processors
from abstrys.revIOr.window import RevIOrWindow

class RevIOr:
    """
    The revIOr application class.
    """

    DEFAULT_FILE_CHECK_INTERVAL = 500
    last_file_check = 0
    last_file_modify_time = 0
    po_win = None
    processor_list = None
    cur_file_path = None
    cur_processor = None

    def __init__(self):
        self.processor_list = [
            text_processors.MdToHtml(),
            text_processors.RstToHtml() ]


    def find_processor(self, file_ext):
        """
        Return the text processor for a given file extension.

        Use the TxtToHTML processor for unknown extensions.
        """
        print("Finding processor for " + file_ext)
        for text_processor in self.processor_list:
            if not text_processor.is_available():
                print("No processor found for %s files. Using the default (text) processor" % file_ext)
                return text_processors.TxtToHtml()
            if text_processor.handles_extension(file_ext):
                print("Using %s to process %s file." % (type(text_processor).__name__, file_ext))
                return text_processor
        # return the default if no match.
        return text_processors.TxtToHtml()


    def set_file(self, filename):
        self.cur_file_path = filename
        (root, ext) = os.path.splitext(self.cur_file_path)
        while ext.startswith('.'):
            ext = ext[1:]
        self.cur_processor = self.find_processor(ext)
        self.process_file()
        return True


    def process_file(self):
        if self.cur_file_path is None:
            print("No file currently loaded!")
            return False
        if self.cur_processor is None:
            print("No text processor for file type.")
            return False
        if not os.path.exists(self.cur_file_path):
            print("Current file path is invalid.")
            return False

        file_contents = None

        try:
            fd = open(self.cur_file_path, 'r')
            file_contents = fd.read()
            fd.close()
        except:
            print("Couldn't load file... will try again later.")
            return False

        processed_text = self.cur_processor.process_text(file_contents)
        self.po_win.set_contents(processed_text)
        self.po_win.set_title(self.cur_file_path)
        return True


    def check_file(self):
        """
        Check to see if the loaded file has been updated.
        """
        if self.cur_file_path is None:
            # don't bother checking if there's no file loaded!
            return True
        try:
            # check the file modification time
            cur_file_modify_time = os.path.getmtime(self.cur_file_path)
            if cur_file_modify_time > self.last_file_modify_time:
                if self.process_file():
                    self.last_file_modify_time = cur_file_modify_time
        except:
            print("Couldn't retrieve file %s! *This may be temporary*")
        return True


    def run(self):
        if len(sys.argv) > 2:
            sys.stderr.write("revIOr Error: too many arguments provided!")
            return 1

        self.po_win = RevIOrWindow(self)

        for arg in sys.argv[1:]:
            # there's one argument (so far) -- a filename.
            if not self.set_file(arg):
                sys.exit(1)
            self.last_file_modify_time = os.path.getmtime(arg)

        self.po_win.connect("delete-event", Gtk.main_quit)
        self.po_win.show_all()

        # The repeatedly-called timeout checks to see if the file modification
        # time has changed.
        GLib.timeout_add(self.DEFAULT_FILE_CHECK_INTERVAL, self.check_file)
        # Run the main loop.
        Gtk.main()
        self.po_win.close()


def main():
    app = RevIOr()
    app.run()

# if run directly from the command-line...
if __name__ == "__main__":
    main()

