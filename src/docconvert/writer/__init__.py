"""The writer submodule."""

import enum

from .base import BaseWriter
from .google import GoogleWriter
from .numpy import NumpyWriter
from .rest import RestWriter
from .epytext import EpytextWriter


class OutputStyle(enum.Enum):
    GOOGLE = "google"
    NUMPY = "numpy"
    REST = "rest"
    EPYTEXT = "epytext"

    def __str__(self):
        return self.value


_WRITERS = {
    OutputStyle.GOOGLE: GoogleWriter,
    OutputStyle.NUMPY: NumpyWriter,
    OutputStyle.REST: RestWriter,
    OutputStyle.EPYTEXT: EpytextWriter,
}


def get_writer(output_style):
    """Get the correct writer based on output docstring style.

    Args:
        output_style (OutputStyle): The output style to write to.

    Returns:
        writer.base.BaseWriter: The docstring writer class to use.

    Raises:
        ValueError: If output style is not supported.
    """
    try:
        output_style = OutputStyle(output_style)
    except ValueError:
        raise ValueError("{0!r} not a supported writer style.".format(output_style))
    return _WRITERS[output_style]
