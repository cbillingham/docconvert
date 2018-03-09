"""Utility functions for modifying and querying lines of strings."""


def get_indent(line):
    """Helper function for getting length of indent for line.

    Args:
        line (str): The line to check.

    Returns:
        int: The length of the indent
    """
    for idx, char in enumerate(line):
        if not char.isspace():
            return idx
    return len(line)


def is_indented(line, indent=1, exact=False):
    """Checks if the line is indented.

    By default, a line with indent equal to or greater passes.

    Args:
        line (str): The line to check.
        indent (int): The length of indent to check.
        exact (bool): Whether the indent must be exact.

    Returns:
        bool: True if the line has the indent.
    """
    for idx, char in enumerate(line):
        if idx >= indent:
            if exact:
                return not char.isspace()
            return True
        elif not char.isspace():
            return False
    return False


def dedent(line, indent):
    """Dedents a line by specified amount.

    Args:
        line (str): The line to check.
        indent (int): The length of indent to remove.

    Returns:
        str: The dedented line.
    """
    return line[indent:]


def dedent_by_minimum(lines):
    """Dedents a group of lines by the minimum indent.

    Args:
        lines (list(str)): The source lines of a section.

    Returns:
        list(str): The dedented lines.
    """
    dedent_len = 0
    if lines:
        dedent_len = min((get_indent(line) for line in lines if line))
    return [dedent(line, dedent_len) for line in lines]
