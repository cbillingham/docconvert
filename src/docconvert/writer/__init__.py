"""The writer submodule."""

import enum

from .base import BaseWriter
from .google import GoogleWriter


class OutputStyle(enum.Enum):
    GOOGLE = "google"

    def __str__(self):
        return self.value


_WRITERS = {OutputStyle.GOOGLE: GoogleWriter}


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
        raise ValueError("{0} not a supported writer style.".format(output_style))
    return _WRITERS[output_style]
