"""EpyText docstring parser."""

import re

from .base import NotParsableError
from .rest import RestParser


class EpytextParser(RestParser):
    """Parser class for parsing epytext docstrings."""

    # example match: "@blah blah:" or "@blah:""
    _field_re = re.compile(r"^@([^\s:]+)\s*([^\s:]*)\s*:")

    _group_fields = ()

    _single_fields = RestParser._return_fields

    @classmethod
    def match(cls, line):
        """Checks if the specified line matches an epytext token.

        Args:
            line (str): Source docstring line.

        Returns:
            bool: Whether the line matches a rest token.
        """
        match = re.search(cls._field_re, line)
        if match:
            if match.group(2):
                return match.group(1) in cls._double_fields
            return (
                match.group(1) in cls._single_fields
                or match.group(1) in cls._directives
            )
        return False

    def parse_token(self):
        """Checks if current line matches any epytext token.

        If the line matches an epytext token, the function will parse it.

        Raises:
            NotParsableError: If the line cannot be parsed.
        """
        match = re.search(self._field_re, self.current_line)
        if match:
            field = match.group(1).lower()
            if match.group(2):
                matches_epy = field in self._double_fields
            else:
                matches_epy = field in self._single_fields

            if matches_epy:
                # get the right parse function and call it
                self._parse_map[field](match)
                return

            if match.group(1) in self._directives:
                self.parse_directive(match)
                return

        raise NotParsableError()

    def parse_arg(self, match):
        """Parses an epytext argument field.

        Args:
            match (re.MatchObject): The match object for the
                field expression.
        """
        arg = match.group(2)
        desc = self.parse_body(startpos=match.end())
        optional = arg.lstrip("*") in self._keywords
        self.doc.add_arg(arg, desc=desc, optional=optional)

    def parse_var(self, match):
        """Parses epytext variable fields.

        Args:
            match (re.MatchObject): The match object for the
                field expression.
        """
        var = match.group(2)
        desc = self.parse_body(startpos=match.end())
        self.doc.add_attribute(var, desc=desc)
