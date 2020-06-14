"""Docstring writer for Google docstrings."""

from .base import BaseWriter


class GoogleWriter(BaseWriter):
    """Google docstring writer."""

    _args_header = "Args"
    _keywords_header = "Keyword Args"
    _directive_title = {
        "example": "Example",
        "note": "Note",
        "seealso": "See Also",
        "warning": "Warning",
        "reference": "References",
        "todo": "Todo",
    }

    def __init__(self, doc, indent, config, **kwargs):
        """
        Args:
            doc (Docstring): The docstring to write out.
            indent (str): The starting indent of the docstring.
            config (DocconvertConfiguration):
                The configuration options for conversion.
            **kwargs: Keyword arguments to pass on to super constructor.
        """
        super(GoogleWriter, self).__init__(doc, indent, config, **kwargs)

    def write_section_header(self, header):
        """Writes a google section header to output lines.

        Args:
            header (str): Header to write out.
        """
        is_first_section = len(self.output) == 1 and self.output[-1].endswith(
            self._quotes + "\n"
        )
        if not is_first_section and self.output[-1] != "\n":
            self.write_line("")
        self.write_line("{0}:".format(header.title()))

    def write_directive(self, element):
        """Writes a google directive section to output lines.

        Args:
            element (tuple): The docstring element.
        """
        self.write_section_header(self._directive_title[element[0]])
        for line in element[1]:
            self.write_line(line, indent=1)

    def write_args(self, element):
        """Writes an args section in google style to output lines.

        Args:
            element (tuple): The docstring element.
        """
        args, keywords = [], []
        for arg in self.doc.arg_fields.values():
            if self.config.output.separate_keywords and arg.optional:
                keywords.append(arg)
            else:
                args.append(arg)
        if args:
            self.write_section_header(self._args_header)
            for arg in args:
                self.write_var(arg)
        if keywords:
            self.write_section_header(self._keywords_header)
            for keyword in keywords:
                self.write_var(keyword, use_optional=False)

    def write_var(self, var, use_optional=True):
        """Write a single variable definition in google style.

        Args:
            var (parser.docstring.Field): The docstring var to write.
            use_optional (bool): Whether to add "optional" in the type
                if the argument is optional.
        """
        name = var.name
        if name == self._vararg:
            name = "*" + name
        if var.name == self._kwarg:
            name = "**" + name

        optional = ""
        if use_optional and self.config.output.use_optional and var.optional:
            optional = "optional"
        kind = var.kind if self.config.output.use_types else ""
        kind = self.remove_back_ticks(kind)
        kind = ", ".join(filter(None, (kind, optional)))
        if kind:
            kind = " ({0})".format(kind)

        header = "{0}{1}".format(name, kind)
        if var.desc:
            self.write_desc(var.desc, header=(header + ":"))
        else:
            self.write_line(header, indent=1)

    def write_attributes(self, element):
        """Write an attributes section in google style to output lines.

        Args:
            element (tuple): The docstring element.
        """
        self.write_section_header("Attributes")
        for var in self.doc.attribute_fields.values():
            self.write_var(var, use_optional=False)

    def write_raises(self, element):
        """Write a raises section in google style to output lines.

        Args:
            element (tuple): The docstring element.
        """
        self.write_section_header("Raises")
        for var in self.doc.raise_fields:
            kind = self.remove_back_ticks(var.kind)
            if var.desc:
                header = "{0}:".format(kind) if kind else None
                self.write_desc(var.desc, header=header)
            else:
                self.write_line(kind, indent=1)

    def write_returns(self, element):
        """Write a return section in google style to output lines.

        Args:
            element (tuple): The docstring element.
        """
        self.write_section_header("Returns")
        kind = self.remove_back_ticks(self.doc.return_field.kind)
        if self.doc.return_field.desc:
            header = "{0}:".format(kind) if kind else None
            self.write_desc(self.doc.return_field.desc, header=header, hanging=False)
        else:
            self.write_line(kind, indent=1)
