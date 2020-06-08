"""Unit tests for ModuleParser and TokenStream."""

import os
import sys
import tokenize

import docconvert
import pytest

# local
from . import test_resources


def get_fixture_lines(filename):
    """Loads the fixture python file and reads the lines.

    Args:
        filename (str): Fixture filename.

    Returns
        list(str): The lines of the fixture.
    """
    filepath = os.path.join(test_resources.FIXTURES, filename)
    with open(filepath, "r") as fixture:
        lines = fixture.readlines()
    return lines


def line_generator(lines):
    """Simple generator for testing LineIter."""
    for line in lines:
        yield line


class TestModuleParser(object):

    lines = get_fixture_lines("tokens.py")

    @classmethod
    def setup_class(cls):
        cls.parser = docconvert.parser.ModuleParser(cls.lines)
        cls.parser.parse()

    def test_parsing_tokens(self):
        assert len(self.parser.docstrings) == 9
        assert self.parser.docstrings[0].start == 1
        assert self.parser.docstrings[0].end == 2
        assert self.parser.docstrings[0].lines == ['"""Module docstring!"""\n']
        assert self.parser.docstrings[1].start == 7
        assert self.parser.docstrings[1].end == 17
        assert self.parser.docstrings[2].start == 33
        assert self.parser.docstrings[2].end == 45
        assert self.parser.docstrings[3].start == 50
        assert self.parser.docstrings[3].end == 51
        assert self.parser.docstrings[3].lines == ['u"""This is a docstring."""\n']
        assert self.parser.docstrings[4].start == 58
        assert self.parser.docstrings[4].end == 62
        assert self.parser.docstrings[4].lines == [
            '"""This is a multiline docstring.\n',
            "\n",
            "It is really long!\n",
            '"""\n',
        ]
        assert self.parser.docstrings[5].start == 65
        assert self.parser.docstrings[5].end == 66
        assert self.parser.docstrings[5].lines == [
            '    """Testing class docstring."""\n'
        ]
        assert self.parser.docstrings[6].start == 68
        assert self.parser.docstrings[6].end == 72
        assert self.parser.docstrings[7].start == 77
        assert self.parser.docstrings[7].end == 80
        assert self.parser.docstrings[8].start == 82
        assert self.parser.docstrings[8].end == 86
        assert self.parser.docstrings[8].lines == [
            '            """Testing nested function docstring.\n',
            "            :param arg1: Desc for arg1\n",
            "            :param kwarg1: Desc for kwarg1\n",
            '            """\n',
        ]

    def test_raw_docstring_args(self):
        assert self.parser.docstrings[0].args == []
        assert self.parser.docstrings[1].args == ["arg1", "arg2"]
        assert self.parser.docstrings[2].args == ["arg1"]

    def test_raw_docstring_keywords(self):
        assert self.parser.docstrings[0].keywords == []
        assert self.parser.docstrings[1].keywords == []
        assert self.parser.docstrings[2].keywords == ["kwarg1"]

    def test_raw_docstring_vararg(self):
        assert self.parser.docstrings[0].vararg is None
        assert self.parser.docstrings[1].vararg is None
        assert self.parser.docstrings[2].vararg == "args"

    def test_raw_docstring_kwarg(self):
        assert self.parser.docstrings[0].kwarg is None
        assert self.parser.docstrings[1].kwarg == "kwargs"
        assert self.parser.docstrings[2].kwarg == "kwargs"


@pytest.mark.skipif(sys.version_info < (3,), reason="requires python3")
class TestPy3ModuleParser(object):
    """Test module parser handles python3 annotations and argument order."""

    lines = get_fixture_lines("py3_tokens.py")

    @classmethod
    def setup_class(cls):
        cls.parser = docconvert.parser.ModuleParser(cls.lines)
        cls.parser.parse()

    def test_parser_handles_py3_tokens(self):
        assert len(self.parser.docstrings) == 2
        assert self.parser.docstrings[0].start == 0
        assert self.parser.docstrings[0].end == 1
        assert self.parser.docstrings[0].lines == ['"""Module docstring!"""\n']
        assert self.parser.docstrings[1].start == 15
        assert self.parser.docstrings[1].end == 25

    def test_args_with_annotations(self):
        assert self.parser.docstrings[0].args == []
        assert self.parser.docstrings[1].args == ["name", "age"]

    def test_keywords_with_annotations(self):
        assert self.parser.docstrings[0].keywords == []
        assert self.parser.docstrings[1].keywords == ["test"]

    def test_raw_docstring_vararg(self):
        assert self.parser.docstrings[0].vararg is None
        assert self.parser.docstrings[1].vararg == "args"

    def test_raw_docstring_kwarg(self):
        assert self.parser.docstrings[0].kwarg is None
        assert self.parser.docstrings[1].kwarg == "kwargs"


class TestTokenStream(object):

    lines = get_fixture_lines("tokens.py")

    @classmethod
    def setup_method(cls):
        cls._line_generator = line_generator(cls.lines)
        cls._token_generator = tokenize.generate_tokens(
            lambda: next(cls._line_generator)
        )
        cls.tokens = docconvert.parser.module.TokenStream(cls._token_generator)

    def test_next(self):
        assert self.tokens.current.kind == tokenize.NL
        self.tokens.next()
        assert self.tokens.current.kind == tokenize.STRING
        assert self.tokens.current.start == (2, 0)
        assert self.tokens.current.end == (2, 23)
        self.tokens.next()
        assert self.tokens.current.kind == tokenize.NEWLINE
        assert self.tokens.current.start == (2, 23)
        assert self.tokens.current.end == (2, 24)
        assert self.tokens.next().kind == tokenize.NEWLINE

    def test_skip(self):
        self.tokens.skip((tokenize.STRING, tokenize.NL, tokenize.NEWLINE))
        assert self.tokens.current.kind == tokenize.OP
        assert self.tokens.current.value == "@"
        assert self.tokens.current.start == (5, 0)
        assert self.tokens.current.end == (5, 1)
        assert self.tokens.current.source == "@bleh\n"

    def test_consume(self):
        while self.tokens.current.kind != tokenize.INDENT:
            self.tokens.consume(self.tokens.current.kind)
        assert self.tokens.current.kind == tokenize.INDENT
        assert self.tokens.current.start == (8, 0)
        assert self.tokens.current.end == (8, 4)
