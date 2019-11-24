# Text processors for revIOr
#
# The base processor is TxtToHtml. It returns the entire input text in a single
# <pre> block. The base processor also implements the following methods, which
# are inherited by all other processors but are not re-implemented by them.
#
# add_file_extension - adds a new file extension to the list that are covered
#                      by this processor.
#
# remove_file_extension - removes a file extension from the list that are
#                         covered by this proceessor.
#
# handles_file_extension - returns True if the processor handles the provided
#                          file extension. False otherwise.
#
# is_available - returns True if the text processor has the requirements to run
#                (usually an imported library is needed). This simply returns
#                the value of self.prereq_loaded.
#
# Each text processor implements the following functions:
#
# get_requirements_txt - returns a string that describes what the requirements for
#                        running the processor are (so it can be displayed in a UI
#                        or on the command-line.
#
# get_requirements_html - returns an HTML-ized version of the text from
#                         get_requirements_txt. This can have links and other markup.
#
# process_text - returns the text converted into HTML.

import codecs

class TxtToHtml:
    """The most basic text -> HTML processor. Converts plain text into a big
    <pre> block."""
    DEFAULT_FILE_EXTENSIONS = ["txt", "text"]
    prereq_loaded = True
    file_extensions = None

    def __init__(self, file_extensions = None):
        if file_extensions is not None:
            self.file_extensions = file_extensions
        else:
            self.file_extensions = self.DEFAULT_FILE_EXTENSIONS


    # don't re-implement any of these in derived classes.
    def add_file_extension(self, ext_spec):
        self.file_extensions.append(ext_spec)

    def rm_file_extension(self, ext_spec):
        self.file_extensions.remove(ext_spec)

    def handles_extension(self, ext_spec):
        return ext_spec in self.file_extensions

    def is_available(self):
        return self.prereq_loaded

    # the following methods are designed to be re-implemented. Go for it!

    def get_requirements_txt(self):
        return 'None needed.'

    def get_requirements_html(self):
        return '<p><em>None needed.</em></p>'

    def process_text(self, input_text):
        """Converts input_text to HTML."""
        return '<pre>\n%s\n</pre>' % input_text


class RstToHtml(TxtToHtml):
    """Converts ReStructuredText to HTML using docutils."""

    def __init__(self):
        TxtToHtml.__init__(self, ['rst','rest'])
        try:
            from docutils.core import publish_string
            self.prereq_loaded = True
        except:
            print("Couldn't import docutils! All you'll get is plain text...")
            self.prereq_loaded = False

    def get_requirements_txt(self):
        return """To process reStructuredText, you either need to install the docutils package, or
        set up an external processor."""

    def get_requirements_html(self):
        return """<p>To process reStructuredText, you either need to install the <a
        href="http://docutils.sourceforge.net">docutils</a> package, or set up an external
        processor.</p>"""

    def process_text(self, input_text):
        if self.prereq_loaded:
            from docutils.core import publish_string
            return codecs.decode(publish_string(input_text, writer_name='html'), 'utf-8')
        else:
            return TxtToHTML.process_text(self, input_text)


class MdToHtml(TxtToHtml):
    """
    Converts Markdown to HTML using the commonmark py module.
    """

    def __init__(self, file_extensions = None):
        TxtToHtml.__init__(self, ['md', 'mdown'])
        try:
            import commonmark
            self.prereq_loaded = True
        except:
            print("Couldn't import commonmark! All you'll get is plain text...")
            self.prereq_loaded = False

    def get_requirements_txt(self):
        return """To process Markdown, you either need to install the commonmark Python package, or
        set up an external processor."""

    def get_requirements_html(self):
        return """<p>To process Markdown, you either need to install the <a
        href="https://github.com/readthedocs/commonmark.py">commonmark</a> Python package, or set up
        an external processor.</p>"""

    def process_text(self, input_text):
        if self.prereq_loaded:
            import commonmark
            return commonmark.commonmark(input_text)
        else:
            return TxtToHTML.process_text(self, input_text)

# class ExternalProcessorToHtml(TxtToHtml):
#     """Converts text to HTML using an external processor."""
#     ext_command = None
#     ext_command_args = None
# 
#     def __init__(self, file_extensions, ext_command, ext_command_args = None):
#         """Takes the list of file extensions that are handled by the external
#         processor, the external processor command and a list of arguments.
# 
#         The command-line should take the text to process on stdin, and emit the
#         text on stdout.
# 
#         Optional arguments can be passed in via the ext_command_args string."""
#         TxtToHtml.__init__(self, file_extensions)
#         self.ext_command = ext_command
#         self.ext_command_args = ext_command_args.split(' ')
# 
#     def get_requirements_txt(self):
#         return """To process Markdown, you either need to install the markdown
#         Python package, or set up an external processor."""
# 
#     def get_requirements_html(self):
#         return """To process Markdown, you either need to install the <a
#         href="http://pythonhosted.org/Markdown/">markdown</a> Python package,
#         or set up an external processor."""
# 
#     def process_text(self, input_text):
#         try:
#             output_text = markdown.markdown(input_text)
#         except:
#             output_text = "Help!"
#         return output_text
# 
