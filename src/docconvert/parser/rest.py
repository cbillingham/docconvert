"""RestructuredText docstring parser."""

import re

from .. import dict_utils
from .. import line_utils
from .base import BaseParser
from .base import NotParsableError


class RestParser(BaseParser):
    """Parser class for parsing restructured text docstrings."""

    # example match: ":blah blah blah:" or ":blah blah:" or ":blah:"
    _field_re = re.compile(r"^:\s*([^\s:]+)\s*([^\s:]*)\s*([^\s:]*)\s*:")
    _arg_fields = (
        "param",
        "parameter",
        "arg",
        "argument",
        "key",
        "keyword",
        "kwarg",
        "kwparam",
    )
    _type_fields = ("type", "vartype")
    _raises_fields = ("raise", "raises", "except", "exception")
    _return_fields = ("return", "returns", "rtype", "returntype")
    _var_fields = ("var", "variable", "ivar", "ivariable", "cvar", "cvariable")
    _group_fields = (
        "parameters",
        "keywords",
        "attributes",
        "exceptions",
        "raises",
        "variables",
        "ivariables",
        "cvariables",
        "example",
        "examples",
    )
    _triple_fields = _arg_fields + _var_fields
    _double_fields = _arg_fields + _type_fields + _raises_fields + _var_fields
    _single_fields = _group_fields + _return_fields

    @classmethod
    def _match_rest(cls, line):
        """Runs a match regex on the line to find reST tokens.

        Args:
            line (str): Source docstring line.

        Returns:
            bool, re.MatchObject or None: Whether the line matches a
            reST token and the match object if it exists.
        """
        match = re.search(cls._field_re, line)
        matches_rest = False
        if match:
            field = match.group(1).lower()
            if match.group(2) and match.group(3):
                matches_rest = field in cls._triple_fields
            elif match.group(2):
                matches_rest = field in cls._double_fields
            else:
                matches_rest = field in cls._single_fields
        return matches_rest, match

    @classmethod
    def match(cls, line):
        """Checks if the specified line matches a reST token.

        Args:
            line (str): Source docstring line.

        Returns:
            bool: Whether the line matches a reST token.
        """
        matches_rest, _ = cls._match_rest(line)
        return matches_rest

    def __init__(self, lines, **kwargs):
        """
        Args:
            lines (list(str)): List of source lines.
            **kwargs: Variable list of keyword to pass to super class
                initializer.
        """
        super(RestParser, self).__init__(lines, **kwargs)
        self._parse_map = dict_utils.setup_map(
            [
                (self._group_fields, self.parse_group),
                (self._type_fields, self.parse_type),
                (self._return_fields, self.parse_return),
                (self._var_fields, self.parse_var),
                (self._raises_fields, self.parse_raise),
                (self._arg_fields, self.parse_arg),
            ]
        )

    def parse_token(self):
        """Checks if current line matches any of the reST tokens.

        If the line matches a reST token, the function will parse it.

        Raises:
            NotParsableError: If the line cannot be parsed.
        """
        matches_rest, match = self._match_rest(self.current_line)
        if matches_rest:
            # get the right parse function and call it
            field = match.group(1).lower()
            self._parse_map[field](match)
            return

        match = re.search(self._directive_re, self.current_line)
        if match and match.group(1) in self._directives:
            self.parse_directive(match)
            return
        raise NotParsableError()

    def parse_arg(self, match):
        """Parses a reST argument field.

        Args:
            match (re.MatchObject): The match object for the
                field expression.
        """
        kind = None
        arg = match.group(2)
        if match.group(3):
            kind = match.group(2)
            arg = match.group(3)
        desc = self.parse_body(startpos=match.end())
        optional = arg.lstrip("*") in self._keywords
        self.doc.add_arg(arg, kind, desc, optional)

    def parse_type(self, match):
        """Parses a reST type field.

        If field is explicitly marked 'vartype', type will be added for
        var of matching name. If field is 'type', it will check if an
        arg or var matches and add the type. If no match exists, it is
        assumed to be an arg.

        Args:
            match (re.MatchObject): The match object for the
                field expression.
        """
        field = match.group(1).lower()
        arg = match.group(2).lstrip("*")
        kind = " ".join(self.parse_body(startpos=match.end()))
        is_attribute = (
            arg in self.doc.attribute_fields and arg not in self.doc.arg_fields
        )
        if field == "vartype" or is_attribute:
            self.doc.add_attribute_type(arg, kind)
        else:
            self.doc.add_arg_type(arg, kind)

    def parse_return(self, match):
        """Parses return and return type fields.

        Args:
            match (re.MatchObject): The match object for the
                field expression.
        """
        field = match.group(1).lower()
        body = self.parse_body(startpos=match.end())
        if field in ("rtype", "returntype"):
            kind = " ".join(body)
            self.doc.add_return_type(kind)
        else:
            self.doc.add_return(desc=body)

    def parse_var(self, match):
        """Parses reST variable fields.

        Args:
            match (re.MatchObject): The match object for the
                field expression.
        """
        kind = None
        var = match.group(2)
        if match.group(3):
            kind = match.group(2)
            var = match.group(3)
        desc = self.parse_body(startpos=match.end())
        self.doc.add_attribute(var, kind, desc)

    def parse_raise(self, match):
        """Parses reST raises fields.

        Args:
            match (re.MatchObject): The match object for the
                field expression.
        """
        # parse group if match is for raises group
        if not match.group(2):
            self.parse_group(match)
            return
        kind = match.group(2)
        desc = self.parse_body(startpos=match.end())
        self.doc.add_raises(kind, desc)

    def parse_group(self, match):
        """Parses reST group consolidated field.

        ReST consolidated fields are supported by epydoc as outlined in
        `Epydoc Fields`_.

        Args:
            match (re.MatchObject): The match object for the
                field expression.

        .. _`Epydoc Fields`: http://epydoc.sourceforge.net/fields.html#rst
        """
        group = match.group(1).lower()
        if group in ("example", "examples"):
            body = self.parse_body(startpos=match.end())
            self.doc.add_element(("example", body))
            return
        self.lines.next()
        while self.lines.has_next() and line_utils.is_indented(self.current_line):
            line = self.current_line
            indent = line_utils.get_indent(line)
            split = line.split(":", 1)
            name = split.pop(0).strip()
            kind = split.pop(0).strip() if split else None
            body = self.parse_body(indent + 1, startpos=len(line))
            if group in ("attributes", "variables", "ivariables", "cvariables"):
                self.doc.add_attribute(name, kind, body)
            elif group in ("exceptions", "raises"):
                self.doc.add_raises(name, body)
            else:
                optional = name.lstrip("*") in self._keywords
                self.doc.add_arg(name, kind, body, optional)
