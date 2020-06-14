"""Docstring writer for epytext docstrings."""

from .rest import RestWriter


class EpytextWriter(RestWriter):
    """Epytext docstring writer."""

    _directive_token = "@{0}:"
    _var_token = "@{0} {1}:"
    _field_token = "@{0}:"

    _attr_type = "type"

    def __init__(self, doc, indent, config, **kwargs):
        """
        Args:
            doc (Docstring): The docstring to write out.
            indent (str): The starting indent of the docstring.
            config (DocconvertConfiguration):
                The configuration options for conversion.
            **kwargs: Keyword arguments to pass on to super constructor.
        """
        super(EpytextWriter, self).__init__(doc, indent, config, **kwargs)
