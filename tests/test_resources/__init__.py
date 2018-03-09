"""Resources submodule for tests"""

import os

_HERE = os.path.dirname(os.path.abspath(__file__))

FIXTURES = os.path.join(_HERE, "fixtures/")
EXAMPLE_CONFIG = os.path.join(_HERE, "../../example_config.json")
INVALID_CONFIG = os.path.join(_HERE, "invalid_config.json")
