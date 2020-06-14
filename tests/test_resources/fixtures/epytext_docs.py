"""Module docstring.

This module contains docstrings.

@note: Testing notes.
    This is still part of the notes.
"""


def func1():
    """Generic short description."""
    pass


def func2():
    b"""Generic short description."""
    pass


def func3(arg1, arg2, kwarg1="Test", kwarg2=0):
    """Generic short description.

    Longer description of this function that does nothing.

    @param arg1: Description for arg1. Longer description. Still part of
        the description. More description.
            Keep this indent because it's there for a reason.
    @type arg1: dict
    @param arg2: Description for arg2.
    @type arg2: list(str)
    @param kwarg1: Description for kwarg1.
    @type kwarg1: str
    @param kwarg2: Description for kwarg2.
    @type kwarg2: int
    @returns: Description for return.
    @rtype: dict(str, int) or None
    @raises RuntimeError: Description for raises.
    """
    pass


def func4(arg1, arg2, kwarg1=None, kwarg2='test'):
    """Testing other usable tokens.

    @param arg1: Description for arg1.
    @type arg1: bool
    @param arg2: Description for arg2.
    @type arg2: list(str)
    @param kwarg1: Description for kwarg1.
    @type kwarg1: int or None
    @param kwarg2: Description for kwarg2.
    @type kwarg2: str
    @returns: Description for return.
    @rtype: dict(str, int)
    @raises ValueError:
    """
    pass


class SomeClass(object):
    """Testing class docstring.

    Should keep this :class:`CustomClass`.

    @var attribute1: Description for attribute1.
    @type attribute1: bool
    @var attribute2: Description for attribute2.
    @type attribute2: list(str)
    """

    def __init__(self):
        pass

    def method1(self, arg1, arg2, kwarg1=2):
        """Method short docstring.

        Testing for groups of args.

        @param arg1: Description for arg1.
        @type arg1: str
        @param arg2: Description for arg2.
        @type arg2: CustomClass
        @param kwarg1: Description for kwarg1.
        @type kwarg1: int
        """
        pass


class CustomClass(object):
    """Testing class docstring.

    @example:

        >>> import template
        >>> a = template.CustomClass(1)
        >>> a.method1(1)
        2

    @note: Can be useful to emphasize important feature.
    @seealso: :class:`CustomClass` can be used as well.
    @warning: ``arg2`` must be non-zero.
    @todo: Check that ``arg2`` is non zero.
    """

    def __init__(self, arg1, *args):
        """
        @param arg1: Description for arg1.
        @type arg1: str
        @param args: Variable args.
        """
        pass

    def method1(self, arg1, **kwargs):
        """Method short docstring.

        @warning: ``arg2`` must be non-zero.

        @param arg1: Description for arg1.
        @type arg1: str
        @param kwargs: Variable keyword args.

        @todo: Checking more stuff.
        @reference: Some silly reference.

        @returns: Description for return.
        @rtype: int

        @raises TypeError:
        @raises ValueError:
        """
        pass
