"""Data structures for passing around docstring specific data."""

from collections import OrderedDict


class Field(object):
    """Field class for wrapping arg, attribute, exception, and return data.

    Attributes:
        name (str): The field name (e.g. arg1, kwargs)
        kind (str or None): The field variable type (e.g. str, int,
            ValueError)
        desc (str or None): The field description.
        optional (bool): Whether the field is optional. Used
            for keyword arguments.
    """

    def __init__(self, name, kind=None, desc=None, optional=False):
        """
        Args:
            name (str): The field name (e.g. arg1, kwargs)
            kind (str or None): The field variable type (e.g. str, int,
                ValueError)
            desc (str or None): The field description.
            optional (bool): Whether the field is optional. Used
                for keyword arguments.
        """
        self.name = name
        self.kind = kind or ""
        self.desc = desc or []
        self.optional = optional

    def __repr__(self):
        """The string representation of a Field object.

        Returns:
            str: The string representation of the Field object.
        """
        return "Field(name={0!r}, kind={1!r}, desc={2!r}, optional={3!r})".format(
            self.name, self.kind, self.desc, self.optional
        )

    def update(self, **kwargs):
        """Updates a Field with specified keywords.

        If a keyword value is None, it is skipped, and the value is not
        updated.

        Args:
            **kwargs: The attributes to update.
        """
        for key, value in kwargs.items():
            if value is not None:
                setattr(self, key, value)


class Docstring(object):
    """Class for storing docstring elements in a style-independent way.

    Attributes:
        elements (list(tuple)): A list of tuple elements in the order
            they appear in the docstring. Elements are a 1 or 2-tuple
            that look like (TYPE, DATA). ::

                [('raw', 'Docstring'),
                 ('args',)
                 ('note', ['A note'])
                 ('return',)]

            | DATA must be a ``str`` or a ``list(str)``.
            | TYPE must be a ``str``. Valid TYPEs are:

                - **attributes** (special section, no DATA)
                - **args** (special section, no DATA)
                - **raises** (special section, no DATA)
                - **return** (special section, no DATA)
                - raw
                - note
                - example
                - warning
                - reference
                - todo
                - seealso
                - start_quotes
                - end_quotes

            Elements with TYPE attributes, args, raises, return are
            special section elements as they contain no DATA. They are
            only indicators of where those sections exists in the
            docstring order.

        arg_fields (dict(str, Field)): A dict of arg fields.
        attribute_fields (dict(str, Field)): A dict of attribute fields.
        raise_fields (list(Field)): A list of exception fields.
        return_field (Field or None): The return field if the docstring
            has one.
    """

    def __init__(self):
        """Docstring initializer."""
        self.elements = []
        self.arg_fields = OrderedDict()
        self.attribute_fields = OrderedDict()
        self.raise_fields = []
        self.return_field = None

    def __repr__(self):
        """The string representation of a Docstring object.

        Returns:
            str: The string representation of the Docstring object.
        """
        result = (
            "Docstring("
            "elements={0!r}, "
            "arg_fields={1!r}, "
            "attribute_fields={2!r}, "
            "raise_fields={3!r}, "
            "return_field={4!r}"
            ")"
        )
        return result.format(
            self.elements,
            self.arg_fields,
            self.attribute_fields,
            self.raise_fields,
            self.return_field,
        )

    def add_element(self, element):
        """Add an element to the docstring.

        Args:
            element (tuple): A 1 or 2-tuple docstring element of
                (TYPE, DATA). For example, ``('args',)`` or
                ``('note', ['Docstring'])``.

                TYPE must be a ``str``.
                DATA must be a ``str`` or a ``list(str)``.
        """
        self.elements.append(element)

    def add_arg(self, arg, kind=None, desc=None, optional=False):
        """Add an argument to the docstring.

        Args:
            arg (str): The name of the argument variable to add.
            kind (str): The type of the argument.
            desc (list(str)): The description of the argument.
            optional (bool): True if the argument is an optional keyword.
        """
        name = arg.lstrip("*")
        if not self.arg_fields:
            self.elements.append(("args",))
        if name in self.arg_fields:
            self.arg_fields[name].update(kind=kind, desc=desc, optional=optional)
        else:
            self.arg_fields[name] = Field(name, kind, desc, optional)

    def add_attribute(self, var, kind=None, desc=None):
        """Add an attribute to the docstring.

        Args:
            var (str): The name of the attribute variable to add.
            kind (str): The type of the attribute.
            desc (list(str)): The description of the attribute.
        """
        if not self.attribute_fields:
            self.elements.append(("attributes",))
        if var in self.attribute_fields:
            self.attribute_fields[var].update(kind=kind, desc=desc)
        else:
            self.attribute_fields[var] = Field(var, kind, desc)

    def add_return(self, kind=None, desc=None):
        """Add a return to the docstring.

        Args:
            kind (str): The type of the return.
            desc (list(str)): The description of the return.
        """
        if not self.return_field:
            self.elements.append(("return",))
            self.return_field = Field("", kind, desc, False)
        else:
            self.return_field.update(kind=kind, desc=desc)

    def add_raises(self, kind, desc=None):
        """Adds a raises error to the docstring.

        Args:
            kind (str): The type of the error raised.
            desc (list(str)): The description of the error raised.
        """
        if not self.raise_fields:
            self.elements.append(("raises",))
        self.raise_fields.append(Field("", kind, desc))

    def add_arg_type(self, name, kind):
        """Adds a type to an argument in the docstring.

        Args:
            name (str): The name of the argument.
            kind (str): The type of the argument.
        """
        name = name.lstrip("*")
        if name in self.arg_fields:
            self.arg_fields[name].update(kind=kind)
        else:
            self.add_arg(name, kind=kind)

    def add_attribute_type(self, name, kind):
        """Adds a type to an attribute in the docstring.

        Args:
            name (str): The name of the attribute.
            kind (str): The type of the attribute.
        """
        if name in self.attribute_fields:
            self.attribute_fields[name].update(kind=kind)
        else:
            self.add_attribute(name, kind=kind)

    def add_return_type(self, kind):
        """Adds a type to the return of the docstring.

        Args:
            kind (str): The type of the return.
        """
        if self.return_field:
            self.return_field.update(kind=kind)
        else:
            self.add_return(kind=kind)
