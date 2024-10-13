"""Make sure we are parsing nodes after assigns correctly."""

class TestClass(object):
    """My test class.

    Testing module parsing bug for func docstring with assignment before.
    """

    #: unique key for my class
    KEY = "my_class"

    @classmethod
    def test_a(cls, name=None, **kwargs):
        """
        Class method with docstring.

        :param name: Optional name to use.
        :type name: str or None
        :rtype: str
        """
        if name:
            return name + "_test_a"
        else:
            return "test_a"
