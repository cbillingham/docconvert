"""Unit tests for BaseParser and LineIter."""

import docconvert
import pytest


class TestBaseParser(object):

    lines = [
        '        bU"""This is a docstring.    ',
        "        ",
        "        .. note:: This is a note.",
        "            Still part of a note.",
        '        """  # test extra stuff',
        "        # more extra stuff",
    ]

    def test_classmethod_match(self):
        for line in ("", ".. note: Test", "blah blah blah"):
            assert docconvert.parser.BaseParser.match(line) is False

    def test_strip_start_end(self):
        parser = docconvert.parser.BaseParser(self.lines)
        assert parser.lines.lines == [
            "        This is a docstring.    ",
            "        ",
            "        .. note:: This is a note.",
            "            Still part of a note.",
        ]
        assert parser._lines_after_docstring == [
            "# test extra stuff",
            "        # more extra stuff",
        ]

    def test_current_line(self):
        parser = docconvert.parser.BaseParser(self.lines)
        assert parser.current_line == "This is a docstring."
        parser.lines.next()
        assert parser.current_line == ""
        parser.lines.next()
        assert parser.current_line == ".. note:: This is a note."
        parser.lines.next()
        assert parser.current_line == "    Still part of a note."

    def test_parse(self):
        parser = docconvert.parser.BaseParser(self.lines)
        parser.parse()
        assert parser.doc.elements == [
            ("start_quote", 'bU"""'),
            ("raw", "This is a docstring."),
            ("raw", ""),
            ("note", ["This is a note.", "Still part of a note."]),
            ("end_quote", '"""'),
            ("raw", ["# test extra stuff", "        # more extra stuff"]),
        ]

    def test_unmatched_line_throws_not_parsable_error(self):
        not_matching_token_lines = [
            '"""',
            ". note:: This is a note",
            ".. note: This is a note",
            "blah blah",
            "Returns:",
            "@parameter:",
            '"""',
        ]
        parser = docconvert.parser.BaseParser(not_matching_token_lines)
        while parser.lines.has_next():
            with pytest.raises(docconvert.parser.base.NotParsableError):
                parser.parse_token()
            parser.lines.next()

    def test_parses_default_directive_tokens_correctly(self):
        matching_token_lines = [
            '""".. note:: This is a note',
            ".. warning:: This is a warning",
            ".. warn:: This is a warning",
            ".. see:: This is a seealso",
            ".. seealso:: This is a seealso",
            ".. reference:: This is a reference",
            ".. ref:: This is a reference",
            ".. todo:: This is a todo",
            ".. example:: This is an example",
            '.. examples:: This is an example"""',
        ]
        parser = docconvert.parser.BaseParser(matching_token_lines)
        parser.parse()
        assert parser.doc.elements == [
            ("start_quote", '"""'),
            ("note", ["This is a note"]),
            ("warning", ["This is a warning"]),
            ("warning", ["This is a warning"]),
            ("seealso", ["This is a seealso"]),
            ("seealso", ["This is a seealso"]),
            ("reference", ["This is a reference"]),
            ("reference", ["This is a reference"]),
            ("todo", ["This is a todo"]),
            ("example", ["This is an example"]),
            ("example", ["This is an example"]),
            ("end_quote", '"""'),
        ]

    def test_parse_body(self):
        parser = docconvert.parser.BaseParser(self.lines)
        body = parser.parse_body()
        assert body == ["This is a docstring."]
        parser.lines.next()
        body = parser.parse_body(startpos=9)
        assert body == ["This is a note.", "Still part of a note."]


class TestLineIter(object):

    lines = ["Line 1", "Line 2", "Line 3", "Line 4", "Line 5"]

    @classmethod
    def setup_method(cls):
        cls.iterator = docconvert.parser.base.LineIter(cls.lines)

    def test_has_next(self):
        assert self.iterator.has_next() is True
        self.iterator.next()
        assert self.iterator.has_next() is True
        self.iterator.next(4)
        assert self.iterator.has_next() is False

    def test_next(self):
        assert self.iterator.next() == "Line 1"
        assert self.iterator.next(4) == ["Line 2", "Line 3", "Line 4", "Line 5"]
        with pytest.raises(StopIteration):
            self.iterator.next()
        self.iterator = docconvert.parser.base.LineIter(self.lines)
        assert self.iterator.next(2) == ["Line 1", "Line 2"]
        assert self.iterator.next(2) == ["Line 3", "Line 4"]
        # Even though only one element is left it should be in a
        # list because n > 1
        assert self.iterator.next(2) == ["Line 5"]
        with pytest.raises(StopIteration):
            self.iterator.next()

    def test_peek(self):
        assert self.iterator.peek() == "Line 1"
        assert self.iterator.peek(4) == ["Line 1", "Line 2", "Line 3", "Line 4"]
        assert self.iterator.peek(2, start=2) == ["Line 3", "Line 4"]
        self.iterator.next(4)
        assert self.iterator.peek(1) == "Line 5"
        # Even though only one element is left it should be in a
        # list because n > 1
        assert self.iterator.peek(3) == ["Line 5"]
        self.iterator.next(1)
        assert self.iterator.peek(1) == "Line 5"
        assert self.iterator.peek(2) == ["Line 5"]

    def test_iterator(self):
        line_num = 1
        for line in self.iterator:
            assert line == "Line {0}".format(line_num)
            line_num += 1
