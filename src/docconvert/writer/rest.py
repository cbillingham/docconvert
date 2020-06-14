"""Docstring writer for reST docstrings."""

from .base import BaseWriter


class RestWriter(BaseWriter):
    """ReST docstring writer."""

    _directive_token = ".. {0}::"
    _var_token = ":{0} {1}:"
    _field_token = ":{0}:"

    _attr_type = "vartype"

    def __init__(self, doc, indent, config, **kwargs):
        """
        Args:
            doc (Docstring): The docstring to write out.
            indent (str): The starting indent of the docstring.
            config (DocconvertConfiguration):
                The configuration options for conversion.
            **kwargs: Keyword arguments to pass on to super constructor.
        """
        super(RestWriter, self).__init__(doc, indent, config, **kwargs)

    def write_directive(self, element):
        """Write a directive section in reST style.

        Args:
            element (tuple): The docstring element.
        """
        header = self._directive_token.format(element[0])
        for i, line in enumerate(element[1]):
            if i == 0:
                self.write_desc([line], header=header, indent=0)
            else:
                self.write_line(line, indent=1)

    def write_var(self, var, field, type_field="type", use_optional=True):
        """Write a single variable definition in reST style.

        Args:
            var (parser.docstring.Field): The docstring var to write.
            field (str): The field name of the var to write.
            type_field (str): The field type of the var to write.
            use_optional (bool): Whether to add "optional" in the type
                if the argument is optional.
        """
        optional = ""
        if use_optional and self.config.output.use_optional and var.optional:
            optional = "optional"
        kind = var.kind if self.config.output.use_types else ""
        kind = self.remove_back_ticks(kind)
        kind = ", ".join(filter(None, (kind, optional)))

        header = self._var_token.format(field, var.name)
        self.write_desc(var.desc, header=header, indent=0)

        if kind:
            header = self._var_token.format(type_field, var.name)
            self.write_desc([kind], header=header, indent=0)

    def write_args(self, element):
        """Write an args section in reST style.

        Args:
            element (tuple): The docstring element.
        """
        args, keywords = [], []
        for arg in self.doc.arg_fields.values():
            if self.config.output.separate_keywords and arg.optional:
                keywords.append(arg)
            else:
                args.append(arg)
        for arg in args:
            self.write_var(arg, "param")
        for keyword in keywords:
            self.write_var(keyword, "keyword", use_optional=False)

    def write_attributes(self, element):
        """Write an attribute section in reST style.

        Args:
            element (tuple): The docstring element.
        """
        for var in self.doc.attribute_fields.values():
            self.write_var(var, "var", type_field=self._attr_type, use_optional=False)

    def write_raises(self, element):
        """Write a raises section in reST style.

        Args:
            element (tuple): The docstring element.
        """
        for var in self.doc.raise_fields:
            kind = self.remove_back_ticks(var.kind)
            header = self._var_token.format("raises", kind)
            self.write_desc(var.desc, header=header, indent=0)

    def write_returns(self, element):
        """Write a returns section in reST style.

        Args:
            element (tuple): The docstring element.
        """
        kind = self.remove_back_ticks(self.doc.return_field.kind)
        if self.doc.return_field.desc:
            header = self._field_token.format("returns")
            self.write_desc(self.doc.return_field.desc, header=header, indent=0)
        if kind:
            header = self._field_token.format("rtype")
            self.write_desc([kind], header=header, indent=0)
