
"""Module docstring!"""


@bleh
@blah
def func1(arg1, arg2, **kwargs):
    """Generic short description

    Longer description of this function that does nothing

    :param arg1: Desc for arg1
    :type arg1: arg1_type
    :returns: Desc for return
    :rtype: `return_type`
    :raises: RaisesError
    """
    pass


def func2():
    pass
"""This should not be a docstring"""


# test strangely-formatted, but valid function
def func3(
    arg1,
    kwarg1="""TESTING
    r""",
    *args,
    **kwargs
    ):
    """Generic short description

    Longer description of this function that does nothing

    :param arg1: Desc for arg1
    :type arg1: arg1_type
    :keyword kwarg1: Desc for kwarg1
    :type arg2: kwarg1_type
    :returns: Desc for return
    :rtype: `return_type`
    :raises: RaisesError
    """  # testing weird valid stuff
    # more weird lines"""
    pass


ASSIGN_ONE_LINE = 5
"""This is a docstring."""


ASSIGN_MULTI_LINE = [
    1,
    2,
    3,
]
"""This is a multiline docstring.

It is really long!
"""
