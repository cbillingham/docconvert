"""Unit tests for Docstring."""

import docconvert


class TestDocstring(object):
    def test_element_ordering(self):
        docstring = docconvert.parser.Docstring()
        docstring.add_element(("raw", "Docstring."))
        docstring.add_return(kind="int")
        docstring.add_raises(kind="ValueError")
        docstring.add_arg("arg", kind="str")
        docstring.add_element(("note", ["First note.", "Second Note."]))
        assert docstring.elements == [
            ("raw", "Docstring."),
            ("return",),
            ("raises",),
            ("args",),
            ("note", ["First note.", "Second Note."]),
        ]

    def test_args(self):
        docstring = docconvert.parser.Docstring()
        docstring.add_arg_type("arg1", "Object")
        docstring.add_arg("arg2", kind="str")
        docstring.add_arg("arg3", desc=["Description."], optional=True)
        docstring.add_arg_type("arg3", "int")
        assert docstring.elements == [("args",)]
        first_arg = docstring.arg_fields.popitem(last=False)
        assert first_arg[0] == "arg1"
        assert first_arg[1].kind == "Object"
        assert docstring.arg_fields["arg2"].kind == "str"
        assert docstring.arg_fields["arg2"].optional == False
        assert docstring.arg_fields["arg3"].kind == "int"
        assert docstring.arg_fields["arg3"].desc == ["Description."]
        assert docstring.arg_fields["arg3"].optional == True

    def test_attributes(self):
        docstring = docconvert.parser.Docstring()
        docstring.add_attribute_type("attr1", "Object")
        docstring.add_attribute("attr2", kind="str")
        docstring.add_attribute("attr3", desc=["Description."])
        docstring.add_attribute_type("attr3", "int")
        assert docstring.elements == [("attributes",)]
        first_attribute = docstring.attribute_fields.popitem(last=False)
        assert first_attribute[0] == "attr1"
        assert first_attribute[1].kind == "Object"
        assert docstring.attribute_fields["attr2"].kind == "str"
        assert docstring.attribute_fields["attr2"].optional == False
        assert docstring.attribute_fields["attr3"].kind == "int"
        assert docstring.attribute_fields["attr3"].desc == ["Description."]

    def test_raises(self):
        docstring = docconvert.parser.Docstring()
        docstring.add_raises("ValueError")
        docstring.add_raises("RuntimeError", desc=["Description."])
        assert docstring.elements == [("raises",)]
        assert docstring.raise_fields[0].kind == "ValueError"
        assert docstring.raise_fields[0].desc == []
        assert docstring.raise_fields[1].kind == "RuntimeError"
        assert docstring.raise_fields[1].desc == ["Description."]

    def test_returns(self):
        docstring = docconvert.parser.Docstring()
        docstring.add_return_type("int")
        docstring.add_return(desc=["Description."])
        assert docstring.elements == [("return",)]
        assert docstring.return_field.kind == "int"
        assert docstring.return_field.desc == ["Description."]
        docstring.add_return_type("str")
        assert docstring.return_field.kind == "str"
