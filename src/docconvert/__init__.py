from . import configuration
from . import core
from . import dict_utils
from . import line_utils
from . import parser
from . import writer

__version__ = "1.2.0"
__version_info__ = tuple(int(i) for i in __version__.split(".") if i.isdigit())
