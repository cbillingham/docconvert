"""Unit tests for NumpyWriter."""

import docconvert


class TestNumpyWriter(object):
    @classmethod
    def setup_method(cls):
        cls.doc = docconvert.parser.Docstring()
        cls.config = docconvert.configuration.DocconvertConfiguration.create_default()

    def test_write_attributes(self):
        self.doc.add_element(("start_quote", '"""'))
        self.doc.add_element(("raw", ["This is a docstring."]))
        self.doc.add_attribute("attr1", kind="str")
        self.doc.add_attribute("attr2", desc=["Description.", "More description."])
        self.doc.add_element(("end_quote", '"""'))
        writer = docconvert.writer.NumpyWriter(self.doc, "    ", self.config)
        assert writer.write() == [
            '    """This is a docstring.\n',
            "\n",
            "    Attributes\n",
            "    ----------\n",
            "    attr1 : str\n",
            "    attr2\n",
            "        Description. More description.\n",
            '    """\n',
        ]

    def test_write_attributes_without_types(self):
        self.doc.add_element(("start_quote", '"""'))
        self.doc.add_attribute("attr1", kind="str")
        self.doc.add_attribute(
            "attr2", kind="int", desc=["Description.", "More description."]
        )
        self.doc.add_element(("end_quote", '"""'))
        self.config.output.use_types = False
        writer = docconvert.writer.NumpyWriter(self.doc, "", self.config)
        assert writer.write() == [
            '"""\n',
            "Attributes\n",
            "----------\n",
            "attr1\n",
            "attr2\n",
            "    Description. More description.\n",
            '"""\n',
        ]

    def test_write_args(self):
        self.doc.add_element(("start_quote", '"""'))
        self.doc.add_element(("raw", ["This is a docstring."]))
        self.doc.add_arg("arg1", kind="str")
        self.doc.add_arg(
            "arg2",
            kind="int",
            desc=["Description.", "More description."],
            optional=True,
        )
        self.doc.add_element(("end_quote", '"""'))
        writer = docconvert.writer.NumpyWriter(self.doc, "", self.config)
        assert writer.write() == [
            '"""This is a docstring.\n',
            "\n",
            "Parameters\n",
            "----------\n",
            "arg1 : str\n",
            "arg2 : int\n",
            "    Description. More description.\n",
            '"""\n',
        ]

    def test_write_args_with_optional(self):
        self.doc.add_element(("start_quote", '"""'))
        self.doc.add_element(("raw", ["This is a docstring."]))
        self.doc.add_arg("arg1", optional=True)
        self.doc.add_arg(
            "arg2",
            kind="int",
            desc=["Description.", "More description."],
            optional=True,
        )
        self.doc.add_element(("end_quote", '"""'))
        self.config.output.use_optional = True
        writer = docconvert.writer.NumpyWriter(self.doc, "", self.config)
        assert writer.write() == [
            '"""This is a docstring.\n',
            "\n",
            "Parameters\n",
            "----------\n",
            "arg1 : optional\n",
            "arg2 : int, optional\n",
            "    Description. More description.\n",
            '"""\n',
        ]

    def test_write_args_with_keywords_section(self):
        self.doc.add_element(("start_quote", '"""'))
        self.doc.add_element(("raw", ["This is a docstring."]))
        self.doc.add_arg("arg1", kind="str")
        self.doc.add_arg(
            "arg2",
            kind="int",
            desc=["Description.", "More description."],
            optional=True,
        )
        self.doc.add_element(("end_quote", '"""'))
        self.config.output.separate_keywords = True
        writer = docconvert.writer.NumpyWriter(self.doc, "", self.config)
        assert writer.write() == [
            '"""This is a docstring.\n',
            "\n",
            "Parameters\n",
            "----------\n",
            "arg1 : str\n",
            "\n",
            "Keyword Arguments\n",
            "-----------------\n",
            "arg2 : int\n",
            "    Description. More description.\n",
            '"""\n',
        ]

    def test_write_args_with_keywords_section_with_optional(self):
        self.doc.add_element(("start_quote", '"""'))
        self.doc.add_element(("raw", ["This is a docstring."]))
        self.doc.add_arg("arg1", kind="str", optional=True)
        self.doc.add_arg(
            "arg2",
            kind="int",
            desc=["Description.", "More description."],
            optional=True,
        )
        self.doc.add_element(("end_quote", '"""'))
        self.config.output.separate_keywords = True
        self.config.output.use_optional = True
        writer = docconvert.writer.NumpyWriter(self.doc, "", self.config)
        assert writer.write() == [
            '"""This is a docstring.\n',
            "\n",
            "Keyword Arguments\n",
            "-----------------\n",
            "arg1 : str\n",
            "arg2 : int\n",
            "    Description. More description.\n",
            '"""\n',
        ]

    def test_write_raises(self):
        self.doc.add_element(("start_quote", '"""'))
        self.doc.add_raises("TypeError")
        self.doc.add_raises("KeyError", desc=["Description.", "More description."])
        self.doc.add_element(("end_quote", '"""'))
        writer = docconvert.writer.NumpyWriter(self.doc, "", self.config)
        assert writer.write() == [
            '"""\n',
            "Raises\n",
            "------\n",
            "TypeError\n",
            "KeyError\n",
            "    Description. More description.\n",
            '"""\n',
        ]

    def test_write_returns(self):
        self.doc.add_element(("start_quote", '"""'))
        self.doc.add_return("str", desc=["Description.", "More description."])
        self.doc.add_element(("end_quote", '"""'))
        writer = docconvert.writer.NumpyWriter(self.doc, "", self.config)
        assert writer.write() == [
            '"""\n',
            "Returns\n",
            "-------\n",
            "str\n",
            "    Description. More description.\n",
            '"""\n',
        ]

    def test_write_directives(self):
        self.doc.add_element(("start_quote", '"""'))
        self.doc.add_element(("note", ["Description.", "More description."]))
        self.doc.add_element(("example", ["Description."]))
        self.doc.add_element(("reference", ["Description."]))
        self.doc.add_element(("warning", ["Description."]))
        self.doc.add_element(("seealso", ["Description."]))
        self.doc.add_element(("todo", ["Description."]))
        self.doc.add_element(("end_quote", '"""'))
        writer = docconvert.writer.NumpyWriter(self.doc, "", self.config)
        assert writer.write() == [
            '"""\n',
            "Notes\n",
            "-----\n",
            "Description.\n",
            "More description.\n",
            "\n",
            "Examples\n",
            "--------\n",
            "Description.\n",
            "\n",
            "References\n",
            "----------\n",
            "Description.\n",
            "\n",
            "Warnings\n",
            "--------\n",
            "Description.\n",
            "\n",
            "See Also\n",
            "--------\n",
            "Description.\n",
            "\n",
            "Todo\n",
            "----\n",
            "Description.\n",
            '"""\n',
        ]

    def test_newline_added_before_raw(self):
        self.doc.add_element(("start_quote", '"""'))
        self.doc.add_element(("note", ["Description.", "More description."]))
        self.doc.add_element(("raw", ["Some raw text.", "Some more raw text."]))
        self.doc.add_element(("todo", ["Description."]))
        self.doc.add_element(("raw", ["", ""]))
        self.doc.add_element(("seealso", ["Description."]))
        self.doc.add_element(("raw", ["", ""]))
        self.doc.add_element(("raw", ["", ""]))
        self.doc.add_element(("raw", ["", "Some raw text."]))
        self.doc.add_element(("end_quote", '"""'))
        writer = docconvert.writer.NumpyWriter(self.doc, "", self.config)
        assert writer.write() == [
            '"""\n',
            "Notes\n",
            "-----\n",
            "Description.\n",
            "More description.\n",
            "\n",
            "\n",
            "Some raw text.\n",
            "Some more raw text.\n",
            "\n",
            "Todo\n",
            "----\n",
            "Description.\n",
            "\n",
            "See Also\n",
            "--------\n",
            "Description.\n",
            "\n",
            "\n",
            "Some raw text.\n",
            '"""\n',
        ]
