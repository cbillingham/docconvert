"""Module docstring.

This module contains docstrings.

Notes
-----
Testing notes.
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

    Parameters
    ----------
    arg1 : dict
        Description for arg1. Longer description. Still part of the
        description. More description.
            Keep this indent because it's there for a reason.
    arg2 : list(str)
        Description for arg2.
    kwarg1 : str
        Description for kwarg1.
    kwarg2 : int
        Description for kwarg2.

    Returns
    -------
    dict(str, int) or None
        Description for return.

    Raises
    ------
    RuntimeError
        Description for raises.
    """
    pass


def func4(arg1, arg2, kwarg1=None, kwarg2='test'):
    """Testing other usable tokens.

    Parameters
    ----------
    arg1 : bool
        Description for arg1.
    arg2 : list(str)
        Description for arg2.
    kwarg1 : int or None
        Description for kwarg1.
    kwarg2 : str
        Description for kwarg2.

    Returns
    -------
    dict(str, int)
        Description for return.

    Raises
    ------
    ValueError
    """
    pass


class SomeClass(object):
    """Testing class docstring.

    Should keep this :class:`CustomClass`.

    Attributes
    ----------
    attribute1 : bool
        Description for attribute1.
    attribute2 : list(str)
        Description for attribute2.
    """

    def __init__(self):
        pass

    def method1(self, arg1, arg2, kwarg1=2):
        """Method short docstring.

        Testing for groups of args.

        Parameters
        ----------
        arg1 : str
            Description for arg1.
        arg2 : CustomClass
            Description for arg2.
        kwarg1 : int
            Description for kwarg1.
        """
        pass


class CustomClass(object):
    """Testing class docstring.

    Examples
    --------

    >>> import template
    >>> a = template.CustomClass(1)
    >>> a.method1(1)
    2

    Notes
    -----
    Can be useful to emphasize important feature.

    See Also
    --------
    :class:`CustomClass` can be used as well.

    Warnings
    --------
    ``arg2`` must be non-zero.

    Todo
    ----
    Check that ``arg2`` is non zero.
    """

    def __init__(self, arg1, *args):
        """
        Parameters
        ----------
        arg1 : str
            Description for arg1.
        *args
            Variable args.
        """
        pass

    def method1(self, arg1, **kwargs):
        """Method short docstring.

        Warnings
        --------
        ``arg2`` must be non-zero.

        Parameters
        ----------
        arg1 : str
            Description for arg1.
        **kwargs
            Variable keyword args.

        Todo
        ----
        Checking more stuff.

        References
        ----------
        Some silly reference.

        Returns
        -------
        int
            Description for return.

        Raises
        ------
        TypeError
        ValueError
        """
        pass
