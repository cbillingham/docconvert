"""Module docstring.

This module contains docstrings.

.. note:: Testing notes.
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

    :param arg1: Description for arg1. Longer description. Still part of
        the description. More description.
            Keep this indent because it's there for a reason.
    :type arg1: dict
    :param arg2: Description for arg2.
    :type arg2: list(str)
    :keyword kwarg1: Description for kwarg1.
    :type kwarg1: str
    :keyword kwarg2: Description for kwarg2.
    :type kwarg2: int
    :returns: Description for return.
    :rtype: dict(str, int) or None
    :raises RuntimeError: Description for raises.
    """
    pass


def func4(arg1, arg2, kwarg1=None, kwarg2='test'):
    """Testing other usable tokens.

    :parameter arg1: Description for arg1.
    :type arg1: bool
    :arg arg2: Description for arg2.
    :type arg2: list(str)
    :kwarg kwarg1: Description for kwarg1.
    :type kwarg1: int or None
    :kwparam kwarg2: Description for kwarg2.
    :type kwarg2: str
    :return: Description for return.
    :rtype: dict(str, int)
    :except ValueError:
    """
    pass


class SomeClass(object):
    """Testing class docstring.

    Should keep this :class:`CustomClass`.

    :var attribute1: Description for attribute1.
    :vartype attribute1: bool
    :var attribute2: Description for attribute2.
    :vartype attribute2: list(str)
    """

    def __init__(self):
        pass

    def method1(self, arg1, arg2, kwarg1=2):
        """Method short docstring.

        Testing for groups of args.

        :Parameters:
            arg1 : str
                Description for arg1.
            arg2 : CustomClass
                Description for arg2.
        :Keywords:
            kwarg1 : int
                Description for kwarg1.
        """
        pass


class CustomClass(object):
    """Testing class docstring.

    :Example:

        >>> import template
        >>> a = template.CustomClass(1)
        >>> a.method1(1)
        2

    .. note:: Can be useful to emphasize important feature.
    .. seealso:: :class:`CustomClass` can be used as well.
    .. warning:: ``arg2`` must be non-zero.
    .. todo:: Check that ``arg2`` is non zero.
    """

    def __init__(self, arg1, *args):
        """
        :param arg1: Description for arg1.
        :type arg1: str
        :param args: Variable args.
        """
        pass

    def method1(self, arg1, **kwargs):
        """Method short docstring.

        .. warning:: ``arg2`` must be non-zero.

        :Parameters:
            arg1 : str
                Description for arg1.
            kwargs :
                Variable keyword args.

        .. todo:: Checking more stuff.
        .. reference:: Some silly reference.

        :return: Description for return.
        :rtype: int

        :Raises:
            TypeError : Description for TypeError.
            ValueError : Description for ValueError.
        """
        pass
