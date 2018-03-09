"""Docconvert main functions.

Functions for reading configs, finding python files, and batch
converting multiple files using multiple processes.
"""

import copy
import difflib
import logging
import multiprocessing
import os
import signal

from . import configuration
from . import parser
from . import writer


_LOGGER = logging.getLogger(__name__)
_TIMEOUT = 999999


def has_python_shebang(filepath, accepted_shebangs=None):
    """Checks if the filepath is a python script.

    The file is a python script if the first line starts with '#!' and
    contains of the accepted shebangs. For example, a file starting with
    '#!usr/bin/python3' would return True if the list of shebangs was
    ['python'].

    Args:
        filepath (str): The filepath of the file to check.
        accepted_shebangs (list(str) or None): The list of shebangs
            that constitute a python script. If None, the default list
            of ['python'] is used.

    Returns:
        bool: True if the filepath matches the accepted shebangs.
    """
    if accepted_shebangs is None:
        accepted_shebangs = ["python"]
    with open(filepath, "r") as script:
        try:
            first_line = script.readline().strip()
        except UnicodeDecodeError:
            return False
    if first_line.startswith("#!"):
        for script in accepted_shebangs:
            if script in first_line:
                return True
    return False


def find_python_files(path, file_ext=".py", accepted_shebangs=None):
    """Finds all python files within directory.

    Args:
        path (str): The directory path to search.
        file_ext (str): The file extension of files to find.
        accepted_shebangs (list(str) or None): The list of shebangs
            that constitute a python script.
    Returns:
        list(str): The list of python files found in the directory.
    """
    src_files = []
    for dirpath, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        files = [f for f in files if not f.startswith(".")]
        for filename in files:
            filepath = os.path.join(dirpath, filename)
            _, ext = os.path.splitext(filepath)
            if ext == file_ext:
                src_files.append(filepath)
            elif not ext and has_python_shebang(filepath, accepted_shebangs):
                src_files.append(filepath)
    return src_files


def convert_file(filepath, config, in_place):
    """Find all docstrings in file and convert them to output style.

    This function reads in a file, finds docstrings, converts them to
    the output style, and overwrites the file with the new content.

    Args:
        filepath (str): The python file to convert.
        config (DocconvertConfiguration): Configuration options
            for conversion.
        in_place (bool): Whether to write to the file in place (True)
            or output a diff to stdout (False).
    """
    with open(filepath, "r") as in_file:
        src_lines = in_file.readlines()
    module = parser.ModuleParser(src_lines)
    module.parse()
    new_lines = copy.copy(src_lines)
    # Replace docstrings in reverse module order, from the bottom up,
    # so that docstring line numbers are not changed
    docstrings = sorted(module.docstrings, key=lambda x: x.start, reverse=True)
    for raw_doc in docstrings:
        # set up parameters
        keywords = raw_doc.keywords + [raw_doc.kwarg]
        # parse docstring lines
        doc_parser = parser.get_parser(raw_doc.lines, config.input_style)
        doc_parser = doc_parser(raw_doc.lines, keywords=keywords)
        doc_parser.parse()
        # write new docstring lines
        doc_writer = writer.get_writer(config.output_style)
        doc_writer = doc_writer(
            doc_parser.doc,
            doc_parser.raw_indent,
            config,
            kwarg=raw_doc.kwarg,
            vararg=raw_doc.vararg,
        )
        new_doc = doc_writer.write()
        new_lines[raw_doc.start : raw_doc.end] = new_doc

    if in_place:
        with open(filepath, "w") as out_file:
            out_file.writelines(new_lines)
        return None
    else:
        src_prefix = "a"
        dest_prefix = "b"
        if not filepath.startswith(os.sep):
            src_prefix += os.sep
            dest_prefix += os.sep
        return list(
            difflib.unified_diff(
                src_lines,
                new_lines,
                fromfile=src_prefix + filepath,
                tofile=dest_prefix + filepath,
            )
        )


class _ConvertDocstring(object):
    """Object wrapping convert function for multiprocessing."""

    def __init__(self, config, in_place):
        self.config = config
        self.in_place = in_place

    def __call__(self, filename):
        try:
            return convert_file(filename, self.config, self.in_place)
        except Exception as exc:
            with multiprocessing.Lock():
                _LOGGER.error(
                    "Child process error, attempting to convert '%s'", filename
                )
                _LOGGER.error(exc, exc_info=True)


def convert(source, threads=0, config=None, in_place=False):
    """Main function, gets all files and converts docstrings.

    Note:
        This function uses multiprocessing to speed up the conversion
        of multiple files.

    Args:
        source (str): The source path to search in.
        threads (int): The amount of threads to use. If 0, will use the
            amount of threads returned by
            ``multiprocessing.cpu_count()``.
        config (DocconvertConfiguration or None): A docconvert config
            object with the settings to use for conversion. If None,
            the default configuration is used.
        in_place (bool): Whether to write to the input files in place (True)
            or output diffs to stdout (False).

    Returns:
        list(list(str)) or None: The diffs of converted files,
        or None if in place editing was enabled.

    Raises:
        ValueError: If source path does not exist.
    """
    if not os.path.exists(source):
        raise ValueError("Path does not exist: {0}".format(source))
    config = config or configuration.DocconvertConfiguration.from_default()
    threads = threads or multiprocessing.cpu_count()
    if os.path.isfile(source):
        src_files = [source]
    else:
        _LOGGER.info("Finding files within %s...", source)
        src_files = find_python_files(
            source, accepted_shebangs=config.accepted_shebangs
        )
    for filename in src_files:
        _LOGGER.info("  Found file: %s", filename)
    _LOGGER.info("Converting files...")

    pool = multiprocessing.Pool(initializer=_ignore_sigint, processes=threads)
    results = None
    try:
        converter = _ConvertDocstring(config, in_place)
        results = pool.map_async(converter, src_files).get(_TIMEOUT)
        pool.close()
        _LOGGER.info("Conversion complete")
    except KeyboardInterrupt:
        pool.terminate()
    finally:
        pool.join()

    return results


def _ignore_sigint():
    """Initializer function to ignore ctrl+c sigint in child process."""
    signal.signal(signal.SIGINT, signal.SIG_IGN)
