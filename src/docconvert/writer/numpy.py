"""Docstring writer for Numpy docstrings."""

from .google import GoogleWriter


class NumpyWriter(GoogleWriter):
    """Numpy docstring writer."""

    _args_header = "Parameters"
    _keywords_header = "Keyword Arguments"
    _directive_title = {
        "example": "Examples",
        "note": "Notes",
        "seealso": "See Also",
        "warning": "Warnings",
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
        super(NumpyWriter, self).__init__(doc, indent, config, **kwargs)

    def get_previous_element(self):
        """Get the previously written element.

        Finds the first previous element that was already written
        that is not a raw element with blank lines.

        Returns:
            tuple: The previous element.
        """
        prev = self._current_element - 1
        element = None
        while prev >= 0:
            element = self.doc.elements[prev]
            if element[0] == "raw":
                if any(line.strip() for line in element[1]):
                    break
            else:
                break
            prev -= 1
        return element

    def write_section_header(self, header):
        """Writes a numpy section header to output lines.

        Args:
            header (str): Header to write out.
        """
        is_first_section = len(self.output) == 1 and self.output[-1].endswith(
            self._quotes + "\n"
        )
        if not is_first_section and self.output[-1] != "\n":
            self.write_line("")
        self.write_line(header.title(), append=False)
        self.write_line("-" * len(header))  # underline

    def write_directive(self, element):
        """Writes a numpy directive section to output lines.

        Args:
            element (tuple): The docstring element.
        """
        self.write_section_header(self._directive_title[element[0]])
        for line in element[1]:
            self.write_line(line)

    def write_var(self, var, use_optional=True):
        """Write a single variable definition in numpy style.

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
            kind = " : {0}".format(kind)

        name = "{0}{1}".format(name, kind)
        self.write_line(name)
        if var.desc:
            self.write_desc(var.desc, hanging=False)

    def write_raises(self, element):
        """Write a raises section in numpy style to output lines.

        Args:
            element (tuple): The docstring element.
        """
        self.write_section_header("Raises")
        for var in self.doc.raise_fields:
            kind = self.remove_back_ticks(var.kind)
            if kind:
                self.write_line(kind)
            if var.desc:
                self.write_desc(var.desc, hanging=False)

    def write_returns(self, element):
        """Write a return section in google style to output lines.

        Args:
            element (tuple): The docstring element.
        """
        self.write_section_header("Returns")
        kind = self.remove_back_ticks(self.doc.return_field.kind)
        # Return type is not optional for numpy docstrings
        if not kind:
            kind = "unknown"
        self.write_line(kind)
        if self.doc.return_field.desc:
            self.write_desc(self.doc.return_field.desc, hanging=False)

    def write_raw(self, lines):
        """Write raw element to output lines.

        Overwritten to ensure that newlines exist after numpy sections
        because numpy sections are not indented. Numpy requires two
        blank lines to differentiate untitled sections.

        Args:
            lines (list(str) or str): A list of raw lines or a single
                line to write out.
        """
        if not isinstance(lines, list):
            lines = [lines]
        # Check if any of the lines contain real text
        not_space = any(line.strip() for line in lines)
        previous_element = self.get_previous_element()
        if not_space and previous_element:
            # If the previous element was a section ensure that 2 newlines
            # are written before any raw lines that contain text
            if previous_element[0] in self._write_map:
                self.write_line("")
                self.write_line("", force=True)

        for line in lines:
            # Append second line adjacent to quotes if first_line specified in config
            append = self._elements_written == 1 and self.config.output.first_line
            self.write_line(line, append=append)
