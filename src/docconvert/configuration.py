"""Configuration for docconvert options."""

import json
import logging

from . import parser
from . import writer
from .writer.base import BackTickRemovalOption


_LOGGER = logging.getLogger(__name__)

PEP8_MAX = 72
"""Default pep8 max docstring line length."""

DEFAULT_CONFIG = {
    "input_style": parser.InputStyle.GUESS,
    "output_style": writer.OutputStyle.GOOGLE,
    "accepted_shebangs": ["python"],
    "output": {
        "first_line": True,
        "replace_quotes": "",
        "standard_indent": "    ",
        "tab_length": 4,
        "realign": True,
        "max_line_length": PEP8_MAX,
        "use_optional": False,
        "remove_type_back_ticks": BackTickRemovalOption.TRUE,
        "use_types": True,
        "separate_keywords": False,
    },
}
"""Default Docconvert configuration settings.

This dictionary is loaded as the default global configuration. Check
the source for the current defaults.
"""


class DocconvertConfiguration(object):
    """Stores Docconvert configuration options in nested levels.

    Attributes:
        level (str): The name of this configuration level.
    """

    @classmethod
    def create_default(cls, **kwargs):
        """Create a default configuration.

        This configuration is loaded with the default Docconvert
        settings from :py:data:`DEFAULT_CONFIG`.

        Args:
            **kwargs: Keyword args to pass to initializer.

        Returns:
            DocconvertConfiguration: A Docconvert configuration loaded
            with the default settings.
        """
        config = cls(**kwargs)
        config.update(DEFAULT_CONFIG)
        return config

    def __init__(self, level="global"):
        """
        Args:
            level (str): The name of the current level of configuration.
                Defaults to 'global'.
        """
        self.level = level

    def update(self, new_mapping):
        """Updates the current config with values from new_mapping.

        Args:
            new_mapping (dict): New configuration values to update with.
        """
        for option, value in new_mapping.items():
            if isinstance(value, dict):
                if hasattr(self, option):
                    sublevel_config = getattr(self, option)
                else:
                    sublevel_config = DocconvertConfiguration(level=option)
                sublevel_config.update(value)
                value = sublevel_config
            setattr(self, option, value)

    def update_from_json(self, filepath):
        """Update configuration with values from a config json file.

        Args:
            filepath (str): Path to the config json file to load.
        """
        new_config_options = _get_dict_from_json(filepath)
        self.update(new_config_options)


def _get_dict_from_json(filepath):
    """Load a dict from a json file.

    Args:
        filepath (str): Path to the config json file to load.

    Returns:
        dict: Dictionary loaded from the specified json file.

    Raises:
        IOError: If the filepath is not proper json.
        OSError: If the filepath does not exist.
    """
    try:
        with open(filepath, "r") as json_file:
            return json.loads(json_file.read())
    except (IOError, OSError):
        _LOGGER.error("Unable to open configuration file '%s'", filepath)
        raise
