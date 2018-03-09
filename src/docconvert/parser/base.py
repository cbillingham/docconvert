"""Base docstring parser."""

import copy
import re

from .. import line_utils
from .docstring import Docstring


class LineIter(object):
    """Iterator for iterating over lines."""

    def __init__(self, lines):
        """
        Args:
            lines (list(str)): List of source lines.
        """
        self.lines = lines
        self.line_num = 0

    def __next__(self, num_of_lines=1):
        """Gets the next lines and increments the current line.

        Args:
            num_of_lines (int): Number of lines to get.

        Returns:
            str or list(str): The current line if num_of_lines is 1 or
            list of lines otherwise. Returns an empty list if
            num_of_lines is less than 1.

        Raises:
            StopIteration: If the iterator is exhausted.
        """
        return self.next(num_of_lines)

    def __iter__(self):
        """Returns iterator object for iterating over the lines.

        Returns:
            LineIter: The iterator over the lines.
        """
        return self

    def has_next(self):
        """Checks if iterator is exhausted.

        Returns:
            bool: True if the iterator has more lines.
        """
        return self.line_num < len(self.lines)

    def next(self, num_of_lines=1):
        """Gets the next lines and increments the current line.

        Args:
            num_of_lines (int): Number of lines to get.

        Returns:
            str or list(str): The current line if num_of_lines is 1 or
            list of lines otherwise. Returns an empty list if
            num_of_lines is less than 1.

        Raises:
            StopIteration: If the iterator is exhausted.
        """
        if not self.has_next():
            raise StopIteration
        lines = []
        if num_of_lines > 0:
            current_index = self.line_num
            self.line_num = min(current_index + num_of_lines, len(self.lines))
            if num_of_lines == 1:
                lines = self.lines[current_index]
            else:
                lines = self.lines[current_index : self.line_num]
        return lines

    def peek(self, num_of_lines=1, start=None):
        """Gets the next lines without incrementing.

        Returns the last item of the list if start index is out of
        bounds or the iterator is exhausted.

        Args:
            num_of_lines (int): Number of lines to get.
            start (int): The index to start at. If None, start is the
                current line of the iterator.

        Returns:
            str or list(str): The current line if num_of_lines is 1 or
            list of lines otherwise. Returns an empty list if
            num_of_lines is less than 1.
        """
        lines = []
        if num_of_lines > 0:
            start_index = min(start or self.line_num, len(self.lines) - 1)
            if num_of_lines == 1:
                lines = self.lines[start_index]
            else:
                end_index = min(start_index + num_of_lines, len(self.lines))
                lines = self.lines[start_index:end_index]
        return lines


class BaseParser(object):
    """Base class for breaking up lines of a docstring into components.

    This class is meant to be subclassed for each type of docstring. By
    default, this class will parse a specified list of recognized
    restructured text directives.

    Attributes:
        doc (docstring.Docstring): The docstring that was parsed from
            the raw docstring lines after running :py:meth:`parse()`.
    """

    # example match: ".. blah::"
    _directive_re = re.compile(r"^\.\. ([^\s:]+)\s*::")
    _directives = {
        "note": "note",
        "warning": "warning",
        "warn": "warning",
        "see": "seealso",
        "seealso": "seealso",
        "reference": "reference",
        "ref": "reference",
        "todo": "todo",
        "example": "example",
        "examples": "example",
    }

    @classmethod
    def match(cls, line):
        """Checks if the specified line matches a token.

        This static method is used by
        :py:func:`docconvert.parser.get_parser()` to guess parsers for
        docstrings that had no explicit input style specified.

        Note:
            This method should be overridden in subclasses in order
            to take advantage of automatic input style recognition.

        Args:
            line (str): Source docstring line.

        Returns:
            bool: Whether the line matches a rest token.
        """
        return False

    def __init__(self, lines, keywords=None):
        """
        Args:
            lines (list(str)): List of source lines.
            keywords (list(str)): List of keyword arguments in the
                function definition that this docstring belongs to.
                Used for distinguishing keywords from arguments.

        Raises:
            ValueError: If lines is an empty list.
        """
        self._starting_docstring = Docstring()
        self._lines_after_docstring = []
        self.doc = Docstring()
        if not lines:
            raise ValueError("Cannot create docstring parser with empty list.")
        lines = self._strip_start(lines)
        lines = self._strip_end(lines)
        self.lines = LineIter(lines)
        self._keywords = keywords or []

    @property
    def current_line(self):
        """str: The current line stripped of section indent."""
        line = self.lines.peek()
        if line.isspace():
            line = ""
        elif line_utils.is_indented(line, self.indent):
            line = line_utils.dedent(line, self.indent).rstrip()
        else:
            line.strip()
        return line

    def _strip_start(self, lines):
        """Strips the starting tokens and saves that information.

        Strips the starting quotes from the first line, gets the section
        indent length, and adds the quotes to the result docstring.

        Args:
            lines (list(str)): The source lines.

        Returns:
            list(str): The lines with the start quotes stripped.

        Raises:
            ValueError: If there are not any starting quotes in the
                docstring lines.
        """
        start_tokens_re = re.compile(r"(\s*)([urbURB]*)(\"\"\"|'''|\"|')")
        start_tokens = re.search(start_tokens_re, lines[0])
        if not start_tokens:
            raise ValueError("Docstring lines must be valid python string.")
        self.raw_indent = start_tokens.group(1)
        self.indent = len(self.raw_indent)
        self.quotes = start_tokens.group(3)
        self._starting_docstring.add_element(
            ("start_quote", "".join(start_tokens.group(2, 3)))
        )
        lines = copy.copy(lines)
        lines[0] = self.raw_indent + lines[0][start_tokens.end() :]
        return lines

    def _strip_end(self, lines):
        """Finds the end quote and strips any lines after it.

        Args:
            lines (list(str)): The source lines.

        Returns:
            list(str): The lines with end quote and following
            data stripped.
        """
        lines = copy.copy(lines)
        line_num = len(lines) - 1
        while line_num >= 0:
            line = lines[line_num].rstrip()
            if self.quotes in line:
                end_quotes = re.search(self.quotes, line)
                before_quotes = line[: end_quotes.start()]
                lines[line_num] = before_quotes
                if not before_quotes or before_quotes.isspace():
                    lines.pop(line_num)
                    line_num -= 1
                after_quotes = line[end_quotes.end() :].lstrip()
                if after_quotes:
                    self._lines_after_docstring.append(after_quotes)
                break
            line_num -= 1
        line_num += 1
        if line_num < len(lines):
            self._lines_after_docstring.extend(lines[line_num:])
            lines = lines[:line_num]
        return lines

    def _is_token_indent(self):
        """Checks if the current line had a token indent."""
        line = self.lines.peek()
        return line_utils.is_indented(line, self.indent, exact=True)

    def parse_token(self):
        """Checks if current line matches any of the recognized tokens.

        If the line matches a token, the function will parse it.

        Note:
            This is the main method to overwrite in subclasses. Make
            sure to raise :py:exc:`NotParsableError` if line isn't a
            recognizable token.

        Raises:
            NotParsableError: If the line cannot be parsed.
        """
        match = re.search(self._directive_re, self.current_line)
        if match and match.group(1) in self._directives:
            self.parse_directive(match)
            return
        raise NotParsableError()

    def parse_body(self, indent=1, startpos=0):
        """Parses a description body for a token.

        Loops through all the next lines until it reaches an indent
        that marks the end of the description body and returns those
        lines.

        Args:
            indent (int): The indent length that marks a line as still
                being part of the description.
            startpos (int): The position to start at on the first line.

        Returns:
            list(str): The text lines of the description body.
        """
        empty_lines = 0
        body = []
        first_line = self.current_line[startpos:].lstrip()
        self.lines.next()
        while self.lines.has_next():
            line = self.current_line
            if not line:
                empty_lines += 1
            elif line_utils.is_indented(line, indent):
                for _ in range(empty_lines):
                    body.append("")
                empty_lines = 0
                body.append(line)
            else:
                self.lines.line_num -= empty_lines
                break
            self.lines.next()
        body = line_utils.dedent_by_minimum(body)
        if first_line:
            body.insert(0, first_line)
        return body

    def parse_directive(self, match):
        """Parses a directive token and adds elements to the docstring.

        Args:
            match (re.MatchObject): The match object for the
                directive expression.
        """
        directive = self._directives[match.group(1)]
        body = self.parse_body(startpos=match.end())
        self.doc.add_element((directive, body))

    def parse(self):
        """Loops through all lines and parses recognized tokens.

        If a line is not recognized, it is added into the docstring
        as a raw line.
        """
        self.doc = copy.copy(self._starting_docstring)

        while self.lines.has_next():
            if self.current_line:
                start_tokens = re.search(r"^\s*", self.lines.peek())
                self.indent = len(start_tokens.group(0))
                break
            else:
                self.doc.add_element(("raw", self.current_line))
                self.lines.next()

        while self.lines.has_next():
            if self._is_token_indent():
                try:
                    self.parse_token()
                except NotParsableError:
                    self.doc.add_element(("raw", self.current_line))
                    self.lines.next()
            else:
                self.doc.add_element(("raw", self.current_line))
                self.lines.next()
        self.doc.add_element(("end_quote", self.quotes))
        if self._lines_after_docstring:
            self.doc.add_element(("raw", self._lines_after_docstring))


class NotParsableError(Exception):
    """Custom exception for unrecognised lines."""

    pass
