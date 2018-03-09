"""Module docstring!"""
a = 1
b = 2


@bleh
@blah
def greet(
    name: str,
    age: int,
    *args,
    test='oh yeah',
    **kwargs
    ) -> ({a: 1, b: 2}
    ):
    """Generic short description

    Longer description of this function that does nothing

    :param arg1: Desc for arg1
    :type arg1: arg1_type
    :returns: Desc for return
    :rtype: `return_type`
    :raises: RaisesError
    """
    pass


def greet2(name: str, age: int, *args, test='oh yeah', **kwargs) -> {a: 1, b: 2}: return 1
"""This should not be considered a docstring.

:param arg1: Desc for arg1
:type arg1: arg1_type
"""