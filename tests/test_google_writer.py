"""Unit tests for GoogleWriter."""

import docconvert


class TestGoogleWriter(object):
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
        writer = docconvert.writer.GoogleWriter(self.doc, "    ", self.config)
        assert writer.write() == [
            '    """This is a docstring.\n',
            "\n",
            "    Attributes:\n",
            "        attr1 (str)\n",
            "        attr2: Description. More description.\n",
            '    """\n',
        ]

    def test_write_attributes_without_types(self):
        self.doc.add_element(("start_quote", '"""'))
        self.doc.add_attribute("attr1", kind="str")
        self.doc.add_attribute(
            "attr2", kind="int", desc=["Description.", "More description."]
        )
        self.doc.add_element(("end_quote", '"""'))
        self.config.output.google.use_types = False
        writer = docconvert.writer.GoogleWriter(self.doc, "", self.config)
        assert writer.write() == [
            '"""\n',
            "Attributes:\n",
            "    attr1\n",
            "    attr2: Description. More description.\n",
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
        writer = docconvert.writer.GoogleWriter(self.doc, "", self.config)
        assert writer.write() == [
            '"""This is a docstring.\n',
            "\n",
            "Args:\n",
            "    arg1 (str)\n",
            "    arg2 (int): Description. More description.\n",
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
        writer = docconvert.writer.GoogleWriter(self.doc, "", self.config)
        assert writer.write() == [
            '"""This is a docstring.\n',
            "\n",
            "Args:\n",
            "    arg1 (optional)\n",
            "    arg2 (int, optional): Description. More description.\n",
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
        self.config.output.google.use_keyword_section = True
        writer = docconvert.writer.GoogleWriter(self.doc, "", self.config)
        assert writer.write() == [
            '"""This is a docstring.\n',
            "\n",
            "Args:\n",
            "    arg1 (str)\n",
            "\n",
            "Keyword Args:\n",
            "    arg2 (int): Description. More description.\n",
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
        self.config.output.google.use_keyword_section = True
        self.config.output.use_optional = True
        writer = docconvert.writer.GoogleWriter(self.doc, "", self.config)
        assert writer.write() == [
            '"""This is a docstring.\n',
            "\n",
            "Keyword Args:\n",
            "    arg1 (str)\n",
            "    arg2 (int): Description. More description.\n",
            '"""\n',
        ]

    def test_write_raises(self):
        self.doc.add_element(("start_quote", '"""'))
        self.doc.add_raises("TypeError")
        self.doc.add_raises("KeyError", desc=["Description.", "More description."])
        self.doc.add_element(("end_quote", '"""'))
        writer = docconvert.writer.GoogleWriter(self.doc, "", self.config)
        assert writer.write() == [
            '"""\n',
            "Raises:\n",
            "    TypeError\n",
            "    KeyError: Description. More description.\n",
            '"""\n',
        ]

    def test_write_returns(self):
        self.doc.add_element(("start_quote", '"""'))
        self.doc.add_return("str", desc=["Description.", "More description."])
        self.doc.add_element(("end_quote", '"""'))
        writer = docconvert.writer.GoogleWriter(self.doc, "", self.config)
        assert writer.write() == [
            '"""\n',
            "Returns:\n",
            "    str: Description. More description.\n",
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
        writer = docconvert.writer.GoogleWriter(self.doc, "", self.config)
        assert writer.write() == [
            '"""\n',
            "Note:\n",
            "    Description.\n",
            "    More description.\n",
            "\n",
            "Example:\n",
            "    Description.\n",
            "\n",
            "References:\n",
            "    Description.\n",
            "\n",
            "Warning:\n",
            "    Description.\n",
            "\n",
            "See Also:\n",
            "    Description.\n",
            "\n",
            "Todo:\n",
            "    Description.\n",
            '"""\n',
        ]
