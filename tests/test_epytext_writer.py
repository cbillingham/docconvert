"""Unit tests for EpytextWriter."""

import docconvert


class TestEpytextWriter(object):
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
        writer = docconvert.writer.EpytextWriter(self.doc, "    ", self.config)
        assert writer.write() == [
            '    """This is a docstring.\n',
            "    @var attr1:\n",
            "    @type attr1: str\n",
            "    @var attr2: Description. More description.\n",
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
        writer = docconvert.writer.EpytextWriter(self.doc, "", self.config)
        assert writer.write() == [
            '"""\n',
            "@var attr1:\n",
            "@var attr2: Description. More description.\n",
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
        writer = docconvert.writer.EpytextWriter(self.doc, "", self.config)
        assert writer.write() == [
            '"""This is a docstring.\n',
            "@param arg1:\n",
            "@type arg1: str\n",
            "@param arg2: Description. More description.\n",
            "@type arg2: int\n",
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
        writer = docconvert.writer.EpytextWriter(self.doc, "", self.config)
        assert writer.write() == [
            '"""This is a docstring.\n',
            "@param arg1:\n",
            "@type arg1: optional\n",
            "@param arg2: Description. More description.\n",
            "@type arg2: int, optional\n",
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
        writer = docconvert.writer.EpytextWriter(self.doc, "", self.config)
        assert writer.write() == [
            '"""This is a docstring.\n',
            "@param arg1:\n",
            "@type arg1: str\n",
            "@keyword arg2: Description. More description.\n",
            "@type arg2: int\n",
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
        writer = docconvert.writer.EpytextWriter(self.doc, "", self.config)
        assert writer.write() == [
            '"""This is a docstring.\n',
            "@keyword arg1:\n",
            "@type arg1: str\n",
            "@keyword arg2: Description. More description.\n",
            "@type arg2: int\n",
            '"""\n',
        ]

    def test_write_raises(self):
        self.doc.add_element(("start_quote", '"""'))
        self.doc.add_raises("TypeError")
        self.doc.add_raises("KeyError", desc=["Description.", "More description."])
        self.doc.add_element(("end_quote", '"""'))
        writer = docconvert.writer.EpytextWriter(self.doc, "", self.config)
        assert writer.write() == [
            '"""\n',
            "@raises TypeError:\n",
            "@raises KeyError: Description. More description.\n",
            '"""\n',
        ]

    def test_write_returns(self):
        self.doc.add_element(("start_quote", '"""'))
        self.doc.add_return("str", desc=["Description.", "More description."])
        self.doc.add_element(("end_quote", '"""'))
        writer = docconvert.writer.EpytextWriter(self.doc, "", self.config)
        assert writer.write() == [
            '"""\n',
            "@returns: Description. More description.\n",
            "@rtype: str\n",
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
        writer = docconvert.writer.EpytextWriter(self.doc, "", self.config)
        assert writer.write() == [
            '"""\n',
            "@note: Description.\n",
            "    More description.\n",
            "@example: Description.\n",
            "@reference: Description.\n",
            "@warning: Description.\n",
            "@seealso: Description.\n",
            "@todo: Description.\n",
            '"""\n',
        ]
