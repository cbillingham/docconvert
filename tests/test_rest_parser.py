"""Unit tests for RestParser."""

import docconvert
import pytest


class TestRestParser(object):
    def test_type_field(self):
        docstring_lines = [
            '""":type arg1: str',
            ":arg int arg2:",
            ":var attribute2:",
            ":type arg2: str",
            ":type attribute2: my_module.MyClass",
            '"""',
        ]
        parser = docconvert.parser.RestParser(docstring_lines)
        parser.parse()
        assert parser.doc.elements == [
            ("start_quote", '"""'),
            ("args",),
            ("attributes",),
            ("end_quote", '"""'),
        ]
        assert parser.doc.arg_fields["arg1"].kind == "str"
        assert parser.doc.arg_fields["arg2"].kind == "str"
        assert parser.doc.attribute_fields["attribute2"].kind == "my_module.MyClass"

    def test_vartype_field(self):
        docstring_lines = ['""":vartype attribute1: int', '"""']
        parser = docconvert.parser.RestParser(docstring_lines)
        parser.parse()
        assert parser.doc.elements == [
            ("start_quote", '"""'),
            ("attributes",),
            ("end_quote", '"""'),
        ]
        assert parser.doc.attribute_fields["attribute1"].kind == "int"

    def test_arg_field(self):
        docstring_lines = [
            '""":arg arg1: Description for arg1.',
            "    More description for arg1.",
            "        More indented description for arg1.",
            '"""',
        ]
        parser = docconvert.parser.RestParser(docstring_lines)
        parser.parse()
        assert parser.doc.elements == [
            ("start_quote", '"""'),
            ("args",),
            ("end_quote", '"""'),
        ]
        assert parser.doc.arg_fields["arg1"].name == "arg1"
        assert parser.doc.arg_fields["arg1"].kind == ""
        assert parser.doc.arg_fields["arg1"].desc == [
            "Description for arg1.",
            "More description for arg1.",
            "    More indented description for arg1.",
        ]

    def test_param_field(self):
        docstring_lines = ['""":param int arg2: Description for arg2.', '"""']
        parser = docconvert.parser.RestParser(docstring_lines)
        parser.parse()
        assert parser.doc.arg_fields["arg2"].name == "arg2"
        assert parser.doc.arg_fields["arg2"].kind == "int"
        assert parser.doc.arg_fields["arg2"].desc == ["Description for arg2."]
        assert parser.doc.arg_fields["arg2"].optional is False

    def test_parameter_field(self):
        docstring_lines = ['""":parameter int arg3: Description for arg3.', '"""']
        parser = docconvert.parser.RestParser(docstring_lines)
        parser.parse()
        assert parser.doc.arg_fields["arg3"].name == "arg3"
        assert parser.doc.arg_fields["arg3"].kind == "int"
        assert parser.doc.arg_fields["arg3"].desc == ["Description for arg3."]
        assert parser.doc.arg_fields["arg3"].optional is False

    def test_argument_field(self):
        docstring_lines = ['""":argument int arg4: Description for arg4.', '"""']
        parser = docconvert.parser.RestParser(docstring_lines)
        parser.parse()
        assert parser.doc.arg_fields["arg4"].name == "arg4"
        assert parser.doc.arg_fields["arg4"].kind == "int"
        assert parser.doc.arg_fields["arg4"].desc == ["Description for arg4."]
        assert parser.doc.arg_fields["arg4"].optional is False

    def test_key_field(self):
        docstring_lines = ['""":key int arg5: Description for arg5.', '"""']
        parser = docconvert.parser.RestParser(docstring_lines, keywords=["arg5"])
        parser.parse()
        assert parser.doc.arg_fields["arg5"].name == "arg5"
        assert parser.doc.arg_fields["arg5"].kind == "int"
        assert parser.doc.arg_fields["arg5"].desc == ["Description for arg5."]
        assert parser.doc.arg_fields["arg5"].optional is True

    def test_keyword_field(self):
        docstring_lines = ['""":keyword int arg6: Description for arg6.', '"""']
        parser = docconvert.parser.RestParser(docstring_lines, keywords=["arg6"])
        parser.parse()
        assert parser.doc.arg_fields["arg6"].name == "arg6"
        assert parser.doc.arg_fields["arg6"].kind == "int"
        assert parser.doc.arg_fields["arg6"].desc == ["Description for arg6."]
        assert parser.doc.arg_fields["arg6"].optional is True

    def test_kwarg_field(self):
        docstring_lines = ['""":kwarg int arg7: Description for arg7.', '"""']
        parser = docconvert.parser.RestParser(docstring_lines, keywords=["arg7"])
        parser.parse()
        assert parser.doc.arg_fields["arg7"].name == "arg7"
        assert parser.doc.arg_fields["arg7"].kind == "int"
        assert parser.doc.arg_fields["arg7"].desc == ["Description for arg7."]
        assert parser.doc.arg_fields["arg7"].optional is True

    def test_kwparam_field(self):
        docstring_lines = ['""":kwparam **kwargs: Description for kwargs.', '"""']
        parser = docconvert.parser.RestParser(docstring_lines, keywords=["kwargs"])
        parser.parse()
        assert parser.doc.arg_fields["kwargs"].name == "kwargs"
        assert parser.doc.arg_fields["kwargs"].desc == ["Description for kwargs."]
        assert parser.doc.arg_fields["kwargs"].optional is True

    def test_var_field(self):
        docstring_lines = [
            '""":var attribute1: Description for attribute1.',
            "    More description for attribute1.",
            "        More indented description for attribute1.",
            '"""',
        ]
        parser = docconvert.parser.RestParser(docstring_lines)
        parser.parse()
        assert parser.doc.elements == [
            ("start_quote", '"""'),
            ("attributes",),
            ("end_quote", '"""'),
        ]
        assert parser.doc.attribute_fields["attribute1"].name == "attribute1"
        assert parser.doc.attribute_fields["attribute1"].kind == ""
        assert parser.doc.attribute_fields["attribute1"].desc == [
            "Description for attribute1.",
            "More description for attribute1.",
            "    More indented description for attribute1.",
        ]

    def test_variable_field(self):
        docstring_lines = [
            '""":variable int attribute2: Description for attribute2.',
            '"""',
        ]
        parser = docconvert.parser.RestParser(docstring_lines)
        parser.parse()
        assert parser.doc.attribute_fields["attribute2"].name == "attribute2"
        assert parser.doc.attribute_fields["attribute2"].kind == "int"
        assert parser.doc.attribute_fields["attribute2"].desc == [
            "Description for attribute2."
        ]

    def test_ivar_field(self):
        docstring_lines = [
            '""":ivar int attribute3: Description for attribute3.',
            '"""',
        ]
        parser = docconvert.parser.RestParser(docstring_lines)
        parser.parse()
        assert parser.doc.attribute_fields["attribute3"].name == "attribute3"
        assert parser.doc.attribute_fields["attribute3"].kind == "int"
        assert parser.doc.attribute_fields["attribute3"].desc == [
            "Description for attribute3."
        ]

    def test_ivariable_field(self):
        docstring_lines = [
            '""":ivariable int attribute4: Description for attribute4.',
            '"""',
        ]
        parser = docconvert.parser.RestParser(docstring_lines)
        parser.parse()
        assert parser.doc.attribute_fields["attribute4"].name == "attribute4"
        assert parser.doc.attribute_fields["attribute4"].kind == "int"
        assert parser.doc.attribute_fields["attribute4"].desc == [
            "Description for attribute4."
        ]

    def test_cvar_field(self):
        docstring_lines = [
            '""":cvar int attribute5: Description for attribute5.',
            '"""',
        ]
        parser = docconvert.parser.RestParser(docstring_lines)
        parser.parse()
        assert parser.doc.attribute_fields["attribute5"].name == "attribute5"
        assert parser.doc.attribute_fields["attribute5"].kind == "int"
        assert parser.doc.attribute_fields["attribute5"].desc == [
            "Description for attribute5."
        ]

    def test_cvariable_field(self):
        docstring_lines = [
            '""":cvariable int attribute6: Description for attribute6.',
            '"""',
        ]
        parser = docconvert.parser.RestParser(docstring_lines)
        parser.parse()
        assert parser.doc.attribute_fields["attribute6"].name == "attribute6"
        assert parser.doc.attribute_fields["attribute6"].kind == "int"
        assert parser.doc.attribute_fields["attribute6"].desc == [
            "Description for attribute6."
        ]

    def test_raise_field(self):
        docstring_lines = [
            '""":raise ValueError: Description for ValueError.',
            "    More description for ValueError.",
            '"""',
        ]
        parser = docconvert.parser.RestParser(docstring_lines)
        parser.parse()
        assert parser.doc.elements == [
            ("start_quote", '"""'),
            ("raises",),
            ("end_quote", '"""'),
        ]
        assert parser.doc.raise_fields[0].kind == "ValueError"
        assert parser.doc.raise_fields[0].desc == [
            "Description for ValueError.",
            "More description for ValueError.",
        ]

    def test_raises_field(self):
        docstring_lines = ['""":raises TypeError: Description for TypeError.', '"""']
        parser = docconvert.parser.RestParser(docstring_lines)
        parser.parse()
        assert parser.doc.raise_fields[0].kind == "TypeError"
        assert parser.doc.raise_fields[0].desc == ["Description for TypeError."]

    def test_except_field(self):
        docstring_lines = [
            '""":except RuntimeError: Description for RuntimeError.',
            '"""',
        ]
        parser = docconvert.parser.RestParser(docstring_lines)
        parser.parse()
        assert parser.doc.raise_fields[0].kind == "RuntimeError"
        assert parser.doc.raise_fields[0].desc == ["Description for RuntimeError."]

    def test_exception_field(self):
        docstring_lines = [
            '""":exception KeywordError: Description for KeywordError.',
            '"""',
        ]
        parser = docconvert.parser.RestParser(docstring_lines)
        parser.parse()
        assert parser.doc.raise_fields[0].kind == "KeywordError"
        assert parser.doc.raise_fields[0].desc == ["Description for KeywordError."]

    def test_return_field(self):
        docstring_lines = [
            '""":return: Description for return.',
            "    More description for return.",
            ":returntype: int",
            '"""',
        ]
        parser = docconvert.parser.RestParser(docstring_lines)
        parser.parse()
        assert parser.doc.elements == [
            ("start_quote", '"""'),
            ("return",),
            ("end_quote", '"""'),
        ]
        assert parser.doc.return_field.kind == "int"
        assert parser.doc.return_field.desc == [
            "Description for return.",
            "More description for return.",
        ]

    def test_returns_field(self):
        docstring_lines = ['""":returns: Description for return.', ":rtype: int", '"""']
        parser = docconvert.parser.RestParser(docstring_lines)
        parser.parse()
        assert parser.doc.return_field.kind == "int"
        assert parser.doc.return_field.desc == ["Description for return."]

    def test_directive_fields(self):
        docstring_lines = [
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
        parser = docconvert.parser.RestParser(docstring_lines)
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

    def test_group_parameters_field(self):
        docstring_lines = [
            '"""',
            ":Parameters:",
            "    arg1 :",
            "        Description for arg1.",
            "        More description for arg1.",
            "            More indented description for arg1.",
            "    arg2 : str",
            "        Description for arg2.",
            '"""',
        ]
        parser = docconvert.parser.RestParser(docstring_lines)
        parser.parse()
        assert parser.doc.elements == [
            ("start_quote", '"""'),
            ("raw", ""),
            ("args",),
            ("end_quote", '"""'),
        ]
        assert parser.doc.arg_fields["arg1"].name == "arg1"
        assert parser.doc.arg_fields["arg1"].kind == ""
        assert parser.doc.arg_fields["arg1"].desc == [
            "Description for arg1.",
            "More description for arg1.",
            "    More indented description for arg1.",
        ]
        assert parser.doc.arg_fields["arg2"].name == "arg2"
        assert parser.doc.arg_fields["arg2"].kind == "str"
        assert parser.doc.arg_fields["arg2"].desc == ["Description for arg2."]
        assert parser.doc.arg_fields["arg2"].optional is False

    def test_group_keywords_field(self):
        docstring_lines = [
            '"""',
            ":Keywords:",
            "    arg3 : int",
            "        Description for arg3.",
            "    arg4 : str",
            '"""',
        ]
        parser = docconvert.parser.RestParser(
            docstring_lines, keywords=["arg3", "arg4"]
        )
        parser.parse()
        assert parser.doc.elements == [
            ("start_quote", '"""'),
            ("raw", ""),
            ("args",),
            ("end_quote", '"""'),
        ]
        assert parser.doc.arg_fields["arg3"].name == "arg3"
        assert parser.doc.arg_fields["arg3"].kind == "int"
        assert parser.doc.arg_fields["arg3"].desc == ["Description for arg3."]
        assert parser.doc.arg_fields["arg3"].optional is True
        assert parser.doc.arg_fields["arg4"].name == "arg4"
        assert parser.doc.arg_fields["arg4"].kind == "str"
        assert parser.doc.arg_fields["arg4"].desc == []
        assert parser.doc.arg_fields["arg4"].optional is True

    def test_group_attributes_field(self):
        docstring_lines = [
            '"""',
            ":Attributes:",
            "    attribute1 :",
            "        Description for attribute1.",
            "        More description for attribute1.",
            "            More indented description for attribute1.",
            "    attribute2 : str",
            '"""',
        ]
        parser = docconvert.parser.RestParser(docstring_lines)
        parser.parse()
        assert parser.doc.elements == [
            ("start_quote", '"""'),
            ("raw", ""),
            ("attributes",),
            ("end_quote", '"""'),
        ]
        assert parser.doc.attribute_fields["attribute1"].name == "attribute1"
        assert parser.doc.attribute_fields["attribute1"].kind == ""
        assert parser.doc.attribute_fields["attribute1"].desc == [
            "Description for attribute1.",
            "More description for attribute1.",
            "    More indented description for attribute1.",
        ]
        assert parser.doc.attribute_fields["attribute2"].name == "attribute2"
        assert parser.doc.attribute_fields["attribute2"].kind == "str"
        assert parser.doc.attribute_fields["attribute2"].desc == []

    def test_group_variables_field(self):
        docstring_lines = [
            '"""',
            ":Variables:",
            "    attribute3",
            "    attribute4 : str",
            '"""',
        ]
        parser = docconvert.parser.RestParser(docstring_lines)
        parser.parse()
        assert parser.doc.attribute_fields["attribute3"].name == "attribute3"
        assert parser.doc.attribute_fields["attribute3"].kind == ""
        assert parser.doc.attribute_fields["attribute4"].name == "attribute4"
        assert parser.doc.attribute_fields["attribute4"].kind == "str"

    def test_group_ivariables_field(self):
        docstring_lines = [
            '"""',
            ":Ivariables:",
            "    attribute5",
            "    attribute6 : str",
            '"""',
        ]
        parser = docconvert.parser.RestParser(docstring_lines)
        parser.parse()
        assert parser.doc.attribute_fields["attribute5"].name == "attribute5"
        assert parser.doc.attribute_fields["attribute5"].kind == ""
        assert parser.doc.attribute_fields["attribute6"].name == "attribute6"
        assert parser.doc.attribute_fields["attribute6"].kind == "str"

    def test_group_cvariables_field(self):
        docstring_lines = [
            '"""',
            ":Cvariables:",
            "    attribute7",
            "    attribute8 : str",
            '"""',
        ]
        parser = docconvert.parser.RestParser(docstring_lines)
        parser.parse()
        assert parser.doc.attribute_fields["attribute7"].name == "attribute7"
        assert parser.doc.attribute_fields["attribute7"].kind == ""
        assert parser.doc.attribute_fields["attribute8"].name == "attribute8"
        assert parser.doc.attribute_fields["attribute8"].kind == "str"

    def test_group_exceptions_field(self):
        docstring_lines = [
            '"""',
            ":Exceptions:",
            "    ValueError :",
            "        Description for ValueError.",
            "    RuntimeError :",
            "        Description for RuntimeError.",
            '"""',
        ]
        parser = docconvert.parser.RestParser(docstring_lines)
        parser.parse()
        assert parser.doc.elements == [
            ("start_quote", '"""'),
            ("raw", ""),
            ("raises",),
            ("end_quote", '"""'),
        ]
        assert parser.doc.raise_fields[0].kind == "ValueError"
        assert parser.doc.raise_fields[0].desc == ["Description for ValueError."]
        assert parser.doc.raise_fields[1].kind == "RuntimeError"
        assert parser.doc.raise_fields[1].desc == ["Description for RuntimeError."]

    def test_group_raises_field(self):
        docstring_lines = [
            '"""',
            ":Raises:",
            "    KeywordError",
            "    TypeError :",
            '"""',
        ]
        parser = docconvert.parser.RestParser(docstring_lines)
        parser.parse()
        assert parser.doc.raise_fields[0].kind == "KeywordError"
        assert parser.doc.raise_fields[0].desc == []
        assert parser.doc.raise_fields[1].kind == "TypeError"
        assert parser.doc.raise_fields[1].desc == []

    def test_group_example_field(self):
        docstring_lines = [
            '"""',
            ":Example: Description for example.",
            "    More description for example.",
            "        More indented description for example.",
            '"""',
        ]
        parser = docconvert.parser.RestParser(docstring_lines)
        parser.parse()
        assert parser.doc.elements == [
            ("start_quote", '"""'),
            ("raw", ""),
            (
                "example",
                [
                    "Description for example.",
                    "More description for example.",
                    "    More indented description for example.",
                ],
            ),
            ("end_quote", '"""'),
        ]

    def test_group_examples_field(self):
        docstring_lines = [
            '"""',
            ":Examples:",
            "    This is example 1:",
            "        Example 1!",
            "    This is example 2:",
            "        Example 2!",
            '"""',
        ]
        parser = docconvert.parser.RestParser(docstring_lines)
        parser.parse()
        assert parser.doc.elements == [
            ("start_quote", '"""'),
            ("raw", ""),
            (
                "example",
                [
                    "This is example 1:",
                    "    Example 1!",
                    "This is example 2:",
                    "    Example 2!",
                ],
            ),
            ("end_quote", '"""'),
        ]

    def test_unmatched_line_throws_not_parsable_error(self):
        docstring_lines = [
            '"""',
            ". note:: This is a note",
            ".. note: This is a note",
            "blah blah",
            "Returns:",
            "@parameter arg1:",
            '"""',
        ]
        parser = docconvert.parser.RestParser(docstring_lines)
        while parser.lines.has_next():
            with pytest.raises(docconvert.parser.base.NotParsableError):
                parser.parse_token()
            parser.lines.next()

    def test_indented_more_than_quotes(self):
        docstring_lines = [
            '"""',
            "    :returns: Description for return.",
            "    :rtype: int",
            '"""',
        ]
        parser = docconvert.parser.RestParser(docstring_lines)
        parser.parse()
        assert parser.doc.return_field.kind == "int"
        assert parser.doc.return_field.desc == ["Description for return."]
