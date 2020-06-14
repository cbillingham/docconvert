"""Unit tests for BaseWriter."""

import docconvert
import pytest


class MyWriter(docconvert.writer.BaseWriter):
    """Subclass of abstract class BaseWriter to use in tests."""

    def write_directive(self, element):
        self.write_line("directive")

    def write_args(self, element):
        self.write_line("args")

    def write_attributes(self, element):
        self.write_line("attributes")

    def write_raises(self, element):
        self.write_line("raises")

    def write_returns(self, element):
        self.write_line("return")


class TestBaseWriter(object):
    @classmethod
    def setup_method(cls):
        cls.doc = docconvert.parser.Docstring()
        cls.config = docconvert.configuration.DocconvertConfiguration.create_default()

    def test_write_line(self):
        writer = MyWriter(self.doc, "", self.config)
        writer.write_line("A test line.")
        assert writer.output == ["A test line.\n"]

    def test_write_empty_line(self):
        writer = MyWriter(self.doc, "    ", self.config)
        writer.write_line("", indent=1)
        assert writer.output == ["\n"]

    def test_write_line_with_section_indent(self):
        writer = MyWriter(self.doc, "      ", self.config)
        writer.write_line("A test line.")
        assert writer.output == ["      A test line.\n"]

    def test_write_line_with_indent(self):
        self.config.output.first_line = False
        writer = MyWriter(self.doc, "    ", self.config)
        writer.write_line("A test line.", indent=1)
        writer.write_line("A test line.", indent=3)
        assert writer.output == [
            "        A test line.\n",
            "                A test line.\n",
        ]

    def test_write_line_with_tab_indent(self):
        self.config.output.first_line = False
        self.config.output.standard_indent = "\t"
        writer = MyWriter(self.doc, "\t", self.config)
        writer.write_line("A test line.", indent=1)
        writer.write_line("A test line.", indent=4)
        assert writer.output == ["\t\tA test line.\n", "\t\t\t\t\tA test line.\n"]

    def test_write_line_with_custom_indent(self):
        self.config.output.first_line = False
        self.config.output.standard_indent = "  "
        writer = MyWriter(self.doc, "    ", self.config)
        writer.write_line("A test line.")
        writer.write_line("A test line.", indent=1)
        writer.write_line("A test line.", indent=2)
        assert writer.output == [
            "    A test line.\n",
            "      A test line.\n",
            "        A test line.\n",
        ]

    def test_write_raw_second_line_is_adjacent(self):
        writer = MyWriter(self.doc, "", self.config)
        writer.write_line('"""')
        writer.write_raw("A test line.")
        assert writer.output == ['"""A test line.\n']

    def test_write_line_append(self):
        writer = MyWriter(self.doc, "", self.config)
        writer.write_line('"""')
        writer.write_line("A test line.", append=True)
        writer.write_line(" Part of the first line.", append=True)
        assert writer.output == ['"""A test line. Part of the first line.\n']

    def test_write_raw_string(self):
        self.config.output.first_line = False
        writer = MyWriter(self.doc, "", self.config)
        writer.write_raw("A test line.")
        assert writer.output == ["A test line.\n"]

    def test_write_raw_list(self):
        self.config.output.first_line = False
        writer = MyWriter(self.doc, "", self.config)
        writer.write_raw(["A test line.", "Another line."])
        assert writer.output == ["A test line.\n", "Another line.\n"]

    def test_is_longer_than_max(self):
        writer = MyWriter(self.doc, "    ", self.config)
        assert writer._max_length == 68
        assert writer._is_longer_than_max("n" * 67) is False
        assert writer._is_longer_than_max("n" * 69) is True

    def test_is_longer_than_max_with_indent(self):
        writer = MyWriter(self.doc, "    ", self.config)
        assert writer._is_longer_than_max("n" * 67) is False
        assert writer._is_longer_than_max("n" * 67, indent=1) is True

    def test_is_longer_than_max_with_custom(self):
        self.config.output.max_line_length = 10
        writer = MyWriter(self.doc, "", self.config)
        assert writer._is_longer_than_max("n" * 10) is False
        assert writer._is_longer_than_max("n" * 11) is True

    def test_write_desc(self):
        self.config.output.first_line = False
        writer = MyWriter(self.doc, "", self.config)
        desc = [
            "This is a description. This is a really long description.",
            "More description.",
            "More long description.",
            "    Indented description should not be reformatted.",
        ]
        writer.write_desc(desc)
        assert writer.output == [
            "    This is a description. This is a really long description. More\n",
            "        description. More long description.\n",
            "            Indented description should not be reformatted.\n",
        ]

    def test_write_desc_with_tab_indent(self):
        self.config.output.first_line = False
        self.config.output.standard_indent = "\t"
        writer = MyWriter(self.doc, "", self.config)
        desc = [
            "This is a description. This is a really long description.",
            "More description.",
            "More long description.",
            "\tIndented description should not be reformatted.",
        ]
        writer.write_desc(desc)
        assert writer.output == [
            "\tThis is a description. This is a really long description. More\n",
            "\t\tdescription. More long description.\n",
            "\t\t\tIndented description should not be reformatted.\n",
        ]

    def test_write_desc_with_header(self):
        self.config.output.first_line = False
        writer = MyWriter(self.doc, "", self.config)
        desc = [
            "This is a description. This is a really long description.",
            "More description.",
            "More long description.",
            "",
            "Line break in description should not be reformatted.",
        ]
        writer.write_desc(desc, header="Header:")
        assert writer.output == [
            "    Header: This is a description. This is a really long description.\n",
            "        More description. More long description.\n",
            "\n",
            "        Line break in description should not be reformatted.\n",
        ]

    def test_write_desc_with_long_header_over_max(self):
        self.config.output.first_line = False
        writer = MyWriter(self.doc, "", self.config)
        desc = [
            "This is a description. This is a really long description.",
            "More description.",
            "More long description.",
        ]
        header = "This is a really, really long header, past the max, that should be on its own line:"
        writer.write_desc(desc, header=header)
        assert writer.output == [
            "    This is a really, really long header, past the max, that should be on its own line:\n",
            "        This is a description. This is a really long description. More\n",
            "        description. More long description.\n",
        ]

    def test_write_desc_without_realign(self):
        self.config.output.first_line = False
        self.config.output.realign = False
        writer = MyWriter(self.doc, "", self.config)
        desc = [
            "This is a description. This is a really long description.",
            "More description.",
            "More long description.",
        ]
        writer.write_desc(desc, indent=0)
        assert writer.output == [
            "This is a description. This is a really long description.\n",
            "    More description.\n",
            "    More long description.\n",
        ]

    def test_write_desc_without_hanging(self):
        self.config.output.first_line = False
        writer = MyWriter(self.doc, "", self.config)
        desc = [
            "This is a description. This is a really long description.",
            "More description.",
            "More long description.",
            "    Indented description should not be reformatted.",
        ]
        writer.write_desc(desc, indent=0, hanging=False)
        assert writer.output == [
            "This is a description. This is a really long description. More\n",
            "description. More long description.\n",
            "    Indented description should not be reformatted.\n",
        ]

    def test_write(self):
        self.doc.add_element(("start_quote", 'b"""'))
        self.doc.add_element(("raw", ["This is a docstring."]))
        self.doc.add_element(("args",))
        self.doc.add_element(("attributes",))
        self.doc.add_element(("raises",))
        self.doc.add_element(("return",))
        self.doc.add_element(("note",))
        self.doc.add_element(("end_quote", '"""'))
        writer = MyWriter(self.doc, "", self.config)
        assert writer.write() == [
            'b"""This is a docstring.\n',
            "args\n",
            "attributes\n",
            "raises\n",
            "return\n",
            "directive\n",
            '"""\n',
        ]
        assert writer._current_element == 7

    def test_write_oneline_with_custom_quotes(self):
        self.doc.add_element(("start_quote", 'b"""'))
        self.doc.add_element(("raw", ["This is a docstring."]))
        self.doc.add_element(("end_quote", '"""'))
        self.config.output.replace_quotes = "'''"
        writer = MyWriter(self.doc, "", self.config)
        assert writer.write() == ["b'''This is a docstring.'''\n"]

    def test_write_throws_invalid_element_for_unrecognized(self):
        self.doc.add_element(("start_quotes", 'b"""'))
        self.doc.add_element(("end_quote", '"""'))
        writer = MyWriter(self.doc, "", self.config)
        with pytest.raises(docconvert.writer.base.InvalidDocstringElementError):
            writer.write()
