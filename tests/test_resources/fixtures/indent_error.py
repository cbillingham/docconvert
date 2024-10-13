"""Test for github issue #11. Make sure we handle this valid syntax.

Tokenize throws an IndentationError, but this is because we haven't
given it the full indentation context of lines above, instead starting
the tokenize generation at a line in the middle of the file. We can
safely ignore this and stop iteration.
"""

from contextlib import contextmanager

@contextmanager
def my_resource(*args, **kwds):
    resource = "test"
    try:
        yield resource
    finally:
        resource = None


def test_x():
    with my_resource() as resource:
        class TestClass: ...
    test = "x"


class MyClass(object):
    class MyNestedClass(object):
        def test_y(): ...
    test = "y"
