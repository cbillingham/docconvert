"""The parser submodule."""

import enum

from .base import BaseParser
from .docstring import Docstring
from .epytext import EpytextParser
from .module import ModuleParser
from .rest import RestParser


class InputStyle(enum.Enum):
    GUESS = "guess"
    REST = "rest"
    EPYTEXT = "epytext"

    def __str__(self):
        return self.value


_PARSERS = {InputStyle.REST: RestParser, InputStyle.EPYTEXT: EpytextParser}


def get_parser(lines, input_style=None):
    """Get the correct parsing based on input docstring style.

    If no input_style is specified, loop through lines and return
    first parser that matches a line as a token.

    Args:
        lines (list(str)): The lines to parse.
        input_style (InputStyle or None): The input style if directly
            specified.

    Returns:
        parser.base.BaseParser: A docstring parser object to use.

    Raises:
        ValueError: If input style is not supported.
    """
    doc_parser = BaseParser
    input_style = input_style or InputStyle.GUESS
    try:
        input_style = InputStyle(input_style)
    except ValueError:
        raise ValueError("{0} not a supported parser style.".format(input_style))
    if input_style != InputStyle.GUESS:
        doc_parser = _PARSERS[input_style]
    else:
        for line in lines:
            line = line.strip().lower()
            for parser in _PARSERS.values():
                if parser.match(line):
                    doc_parser = parser
                    break
    return doc_parser
