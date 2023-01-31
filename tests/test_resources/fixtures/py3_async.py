"""Module docstring!"""
import asyncio


async def greet(arg1):
    """Generic short description

    Longer description of this function that does nothing

    :param arg1: Desc for arg1
    :type arg1: arg1_type
    :returns: Desc for return
    :rtype: `return_type`
    :raises: RaisesError
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

    async def method1(self, arg1, arg2, kwarg1=2):
        """Method short docstring.

        Testing for groups of args.

        :param arg1: Description for arg1.
        :type arg1: str
        :param arg2: Description for arg2.
        :type arg2: CustomClass
        :param kwarg1: Description for kwarg1.
        :type kwarg1: int
        """
        pass
