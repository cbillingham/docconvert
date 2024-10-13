"""Base docstring writer."""

import abc
import enum
import functools
import re
import textwrap

import six

from .. import dict_utils
from .. import line_utils


@six.add_metaclass(abc.ABCMeta)
class BaseWriter(object):
    """Base class for writing elements of docstring into format.

    This class is meant to be subclassed for each type of docstring.

    Attributes:
        doc (Docstring): The docstring to write.
        config (DocconvertConfiguration):
            The configuration options for conversion.
        output (list(str)): The generated output lines as a result of
            writing the new docstring.
    """

    _directives = ("example", "note", "seealso", "warning", "reference", "todo")
    _supports_epytext_convert = True

    def __init__(self, doc, indent, config, kwarg="", vararg=""):
        """
        Args:
            doc (Docstring): The docstring to write out.
            indent (str): The starting indent of the docstring.
            config (DocconvertConfiguration):
                The configuration options for conversion.
            kwarg (str): The name of the kwarg for this docstring's
                function if it had one.
            vararg (str): The name of the vararg for this docstrings's
                function if it had one.
        """
        self.doc = doc
        self.config = config
        self._section_indent = indent
        self._vararg = vararg
        self._kwarg = kwarg

        self._write_map = dict_utils.setup_map(
            [
                (self._directives, self.write_directive),
                ("args", self.write_args),
                ("attributes", self.write_attributes),
                ("raises", self.write_raises),
                ("return", self.write_returns),
            ]
        )
        self.output = []
        self._elements_written = 0
        self._quotes = ""
        self._current_element = 0

        self._indent = self.config.output.standard_indent
        self._using_tabs = "\t" in self._indent
        self._max_length = self._calculate_max_line_length(
            self.config.output.max_line_length
        )

        # Setup regex for backtick removal if enabled
        backtick_option = BackTickRemovalOption.from_bool_or_str(
            self.config.output.remove_type_back_ticks
        )
        self.backtick_regex = None
        if backtick_option == BackTickRemovalOption.TRUE:
            self.backtick_regex = re.compile(r"(?<!:)`(?P<text>[^\s`]+)`")
        elif backtick_option == BackTickRemovalOption.DIRECTIVES:
            self.backtick_regex = re.compile(r"[^\s`]*`(?P<text>[^\s`]+)`")

        # Setup regex for epytext markup convert if supported and enabled
        self.epytext_markup_regex = None
        self.remove_epytext_types = False
        if self._supports_epytext_convert:
            epytext_option = EpytextMarkupConvertOption.from_bool_or_str(
                self.config.output.convert_epytext_markup
            )
            if epytext_option != EpytextMarkupConvertOption.FALSE:
                self.epytext_markup_regex = re.compile(r"([IBMC])\{(?P<text>[^\}]*)\}")
            if epytext_option == EpytextMarkupConvertOption.TYPES:
                self.remove_epytext_types = True

    def _calculate_max_line_length(self, max_length):
        """Calculates maximum line length for realigning.

        Maximum line length is the max length minus the length of
        the prefix indent.

        Args:
            max_length (int): The defined maximum line length.

        Returns:
            int: The shifted maximum line length taking into account
            the docstring section indent.
        """
        prefix_indent_length = len(self._section_indent)
        if self._using_tabs:
            prefix_indent_length *= self.config.output.tab_length
        return max_length - prefix_indent_length

    def _is_longer_than_max(self, line, indent=0):
        """Checks if line is longer than max line length.

        Args:
            line (str): The line to check.
            indent (int): The amount to indent the line.

        Returns:
            bool: Whether the line is longer than the max line length.
        """
        length = (indent * len(self.config.output.standard_indent)) + len(line)
        return length > self._max_length

    def _reformat_lines(self, lines, indent, hanging=True):
        """Indents lines and realigns based on max line length.

        If configuration realign is set, finds lines up to first indent
        or line break, joins them with a single space and re-wraps them
        based on the max line length.

        Args:
            lines (list(str)): The lines to realign.
            indent (int): The indent of the first line.
            hanging (bool): Whether or not lines under the first line
                have a hanging indent.

        Returns:
            list(str): The reformatted lines.
        """
        wrap_length = self._max_length
        # If we are using tabs, we must change wrap length because tabs
        # are only counted as length 1 in python string.
        if self._using_tabs:
            # Consider wrap length for subsequent indents as well.
            prefix_tab_length = (indent + int(hanging)) * self.config.output.tab_length
            wrap_length = self._max_length - prefix_tab_length

        replace_to = 0
        new_lines = []
        initial_indent = indent
        realigning = self.config.output.realign
        for i, line in enumerate(lines):
            if i == 1 and hanging:
                indent += 1
            if not line or line_utils.is_indented(line):
                realigning = False
            if not realigning:
                new_lines.append((indent * self._indent) + line)
            else:
                replace_to = i + 1
        if replace_to:
            realign = " ".join(lines[:replace_to])
            subsequent_indent = indent if hanging else initial_indent
            realigned_lines = textwrap.wrap(
                realign,
                wrap_length,
                initial_indent=(initial_indent * self._indent),
                subsequent_indent=(subsequent_indent * self._indent),
            )
            new_lines = realigned_lines + new_lines
        return new_lines

    def write_line(self, line, indent=0, append=False, force=False):
        """Write a line with the proper indentation.

        Args:
            line (str): The line to write.
            indent (int): The number of indents.
            append (bool): Append to the previous line instead.
            force (bool): Force the line to be written by skipping over
                any checks. Defaults to False.
        """
        indent = self._section_indent + (indent * self._indent)
        if not line or line.isspace():
            # skip over all empty lines after the beginning quotes
            # skip over empty lines that come after newlines
            after_quote = self._elements_written == 1
            after_newline = self.output and self.output[-1] == "\n"
            if not force and (after_quote or after_newline):
                return
            line = ""
            indent = ""
        line = line.rstrip()
        if append:
            self.output[-1] = "{0}{1}\n".format(self.output[-1].rstrip(), line)
        else:
            self.output.append("{0}{1}\n".format(indent, line))
        self._elements_written += 1

    def write_raw(self, lines):
        """Write raw element to output lines.

        Args:
            lines (list(str) or str): A list of raw lines or a single
                line to write out.
        """
        if not isinstance(lines, list):
            lines = [lines]
        for line in lines:
            # Append second line adjacent to quotes if first_line specified in config
            append = self._elements_written == 1 and self.config.output.first_line
            line = self.convert_epytext_markup(line)
            self.write_line(line, append=append)

    def write_desc(self, desc, header=None, indent=1, hanging=True):
        """Write out a description, reformatting if specified.

        If configuration ``realign`` is set, finds lines up to
        first indent or line break, joins them with a single space
        and re-wraps them based on the max line length.

        Args:
            header (str or None): Header to go before description.
            desc (list(str)): Description lines to wrap.
            indent (int): The indent to write to.
            hanging (bool): Whether or not lines under the first line
                have a hanging indent.
        """
        # Convert any lines before realigning so we are converting source
        desc = [self.convert_epytext_markup(line) for line in desc]
        if header:
            if self._is_longer_than_max(header, indent):
                self.write_line(header, indent)
                next_indent = indent + 1 if hanging else indent
                desc = self._reformat_lines(desc, next_indent, hanging=False)
            else:
                desc.insert(0, header)
                desc = self._reformat_lines(desc, indent, hanging=hanging)
        else:
            desc = self._reformat_lines(desc, indent, hanging=hanging)
        for line in desc:
            self.write_line(line)

    @abc.abstractmethod
    def write_directive(self, element):
        """Write a directive section.

        Args:
            element (tuple): The docstring element.

        Note:
            Override this function in subclass.
        """
        pass

    @abc.abstractmethod
    def write_args(self, element):
        """Write an args section.

        Args:
            element (tuple): The docstring element.

        Note:
            Override this function in subclass.
        """
        pass

    @abc.abstractmethod
    def write_attributes(self, element):
        """Write an attribute section.

        Args:
            element (tuple): The docstring element.

        Note:
            Override this function in subclass.
        """
        pass

    @abc.abstractmethod
    def write_raises(self, element):
        """Write a raises section.

        Args:
            element (tuple): The docstring element.

        Note:
            Override this function in subclass.
        """
        pass

    @abc.abstractmethod
    def write_returns(self, element):
        """Write a returns section.

        Args:
            element (tuple): The docstring element.

        Note:
            Override this function in subclass.
        """
        pass

    def write_quotes(self, kind, quotes):
        """Writes out beginning or ending quotes of docstring.

        If configuration ``replace_quotes`` is configured this will
        replace quotes with the new value.

        Args:
            kind (str): The quote kind. Either ``"start_quote"`` or
                ``"end_quote"``.
            quotes (str): The quote value to write out.
        """
        if self.config.output.replace_quotes:
            quotes = re.sub(
                r"\"\"\"|'''|\"|'", self.config.output.replace_quotes, quotes
            )
        self._quotes = quotes
        one_line_doc = kind == "end_quote" and len(self.output) == 1
        self.write_line(quotes, append=one_line_doc)

    def write(self):
        """Writes all elements in docstring to output lines.

        Returns:
            list(str): The resulting lines of the newly written
                docstring.

        Raises:
            InvalidDocstringElementError: When an unrecognisable element
                is found in the docstring.
        """
        self.output = []
        for i, element in enumerate(self.doc.elements):
            self._current_element = i
            kind = element[0]
            if kind in ("start_quote", "end_quote"):
                self.write_quotes(kind, element[1])
            elif kind in self._write_map:
                self._write_map[kind](element)
            elif kind == "raw" and len(element) == 2:
                self.write_raw(element[1])
            else:
                raise InvalidDocstringElementError(
                    "Invalid element {0}. `{1}` is not "
                    "a recognized element type.".format(element, kind)
                )
        return self.output

    def remove_back_ticks(self, text):
        """Removes back ticks from text.

        Removal depends on configuration of ``remove_type_back_ticks``.
        See :py:class:`BackTickRemovalOption`.

        Args:
            text (str): The text to remove back ticks from.

        Returns:
            str: The string with replaceable back ticks removed.
        """
        if not text or not self.backtick_regex:
            return text
        return re.sub(self.backtick_regex, r"\g<text>", text)

    def _replace_epytext_markup(self, match, in_type=False):
        """Helper used in re.sub to replace epytext markup matches."""
        text = match.group(2)
        if match.group(1) == "I":
            return "*{}*".format(text)
        elif match.group(1) == "B":
            return "**{}**".format(text)
        elif match.group(1) == "M":
            return ":math:`{}`".format(text)
        elif match.group(1) == "C":
            if not in_type or not self.remove_epytext_types:
                return "``{}``".format(text)
        return text

    def convert_epytext_markup(self, text, in_type=False):
        """Converts epytext markup syntax to reST syntax.

        Removal depends on configuration of ``convert_epytext_markup``.
        See :py:class:`EpytextMarkupConvertOption`.

        Args:
            text (str): The text to convert.
            in_type (bool): Whether the text is in a type definition.

        Returns:
            str: The string with markup converted.
        """
        if not text or not self.epytext_markup_regex:
            return text
        replace = functools.partial(self._replace_epytext_markup, in_type=in_type)
        return re.sub(self.epytext_markup_regex, replace, text)


class BackTickRemovalOption(enum.Enum):
    """Option for removing back ticks from types.

    Option has three modes:

        - **FALSE**: No back ticks will be removed.
        - **TRUE**: Back ticks will be removed, except from sphinx
          directives. For example:

          - ```list` of `str``` becomes ``list of str``
          - ``:py:class:`Test``` stays as ``:py:class:`Test```
          - ``lot`s of `bool`s`` becomes ``lot`s of bools``

        - **DIRECTIVES**: All back ticks, including directives, will be
          removed. For example:

          - ```list` of `str``` becomes ``list of str``
          - ``:py:class:`Test``` becomes ``Test``
          - ``lot`s of `bool`s`` becomes ``lot`s of bools``
    """

    FALSE = "false"
    TRUE = "true"
    DIRECTIVES = "directives"

    @classmethod
    def from_bool_or_str(cls, value):
        """Function to handle getting enum from boolean arguments.

        Args:
            value (str or bool): The value of the option. Boolean values
                will be converted to a string value.

        Returns:
            BackTickRemovalOption: The removal option enum value.
        """
        if value is True:
            value = "true"
        if value is False:
            value = "false"
        return cls(value)


class EpytextMarkupConvertOption(enum.Enum):
    """Option for converting epytext inline markup in docstrings.

    Option has three modes:

        - **FALSE**: No epytext brackets will be converted
        - **TRUE**: Epytext brackets will be converted to reST formats.
          For example:

          - ``I{text}`` becomes ``*text*``
          - ``B{text}`` becomes ``**text**``
          - ``C{source code}`` becomes ``` ``source code`` ```
          - ``M{m*x+b}`` becomes ``:math:`m*x+b```

        - **TYPES**: Epytext brackets will be converted to reST formats.
          Source code markup will be completely removed from type strings.
          For example:

          - ``I{text}`` becomes ``*text*``
          - ``B{text}`` becomes ``**text**``
          - ``C{source code}`` becomes ``source code``
    """

    FALSE = "false"
    TRUE = "true"
    TYPES = "types"

    @classmethod
    def from_bool_or_str(cls, value):
        """Function to handle getting enum from boolean arguments.

        Args:
            value (str or bool): The value of the option. Boolean values
                will be converted to a string value.

        Returns:
            EpytextBracketConvertOption: The removal option enum value.
        """
        if value is True:
            value = "true"
        if value is False:
            value = "false"
        return cls(value)


class InvalidDocstringElementError(Exception):
    """Custom exception for unrecognised docstring elements."""
