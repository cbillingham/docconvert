"""Utility functions for setting up mappings of data."""


def setup_map(items):
    """Flattens a list of tuple pairs into a dict.

    Args:
        items (list(tuple)): A list of 2-tuples, where each tuple is
            either a (str, function) or a (tuple(str), function).

    Returns:
        dict(str, function): A mapping of string to function.
    """
    mapping = {}
    for sublist, func in items:
        if isinstance(sublist, tuple):
            for field in sublist:
                mapping[field] = func
        else:
            mapping[sublist] = func
    return mapping
