"""Unit tests for configuration submodule."""

import docconvert
import pytest

# local
from . import test_resources


class TestConfig(object):
    def test_get_config(self):
        config = docconvert.configuration.DocconvertConfiguration()
        config.update_from_json(test_resources.EXAMPLE_CONFIG)
        assert config.output_style == "google"
        assert config.output.tab_length == 4
        assert config.output.remove_type_back_ticks == "true"
        assert config.output.use_types is True

    def test_invalid_config(self):
        config = docconvert.configuration.DocconvertConfiguration()
        with pytest.raises((IOError, OSError)):
            config.update_from_json(test_resources.INVALID_CONFIG)
