"""Unit tests for utility functions."""

from docconvert import line_utils


def test_dedent_by_minimum():
    lines = ["        Line 1", "    Line 2", "        Line 3"]
    new_lines = line_utils.dedent_by_minimum(lines)
    assert new_lines == ["    Line 1", "Line 2", "    Line 3"]
    assert line_utils.dedent_by_minimum(new_lines) == [
        "    Line 1",
        "Line 2",
        "    Line 3",
    ]
