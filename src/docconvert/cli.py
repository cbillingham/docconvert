"""Commandline script for docconvert."""

import argparse
import logging
import os
import subprocess
import sys

from six.moves import input

from . import configuration
from . import core
from . import parser
from . import writer


_LOGGER = logging.getLogger(__name__)


def setup_logger(verbose=False):
    """Setup basic logging handler for console feedback.

    Args:
        verbose (bool): If true, sets level of logger to logging.INFO,
            else leaves handler at default of logging.WARNING.
    """
    level = logging.INFO if verbose else logging.WARNING
    log_format = "%(name)s:%(levelname)s: %(message)s"
    logging.basicConfig(format=log_format, level=level)


def is_git_repository(path):
    """Checks if path is in a git repository.

    Args:
        path (str): The path to check.

    Returns:
        bool: Whether the path is a git repository.
    """
    if os.path.isfile(path):
        path = os.path.dirname(path)
    with open(os.devnull, "wb") as devnull:
        proc = subprocess.Popen(
            ["git", "rev-parse", "--is-inside-work-tree"],
            cwd=path,
            stdout=devnull,
            stderr=devnull,
        )
        proc.wait()
    return proc.returncode == 0


def run():
    """Parses arguments and calls core convert function."""
    arg_parser = argparse.ArgumentParser(prog="docconvert")
    arg_parser.add_argument("source", help="The directory or file to convert.")
    arg_parser.add_argument(
        "-i",
        "--input",
        help="Input docstring style. (default: guess)",
        type=parser.InputStyle,
        choices=list(parser.InputStyle),
    )
    arg_parser.add_argument(
        "-o",
        "--output",
        help="Output docstring style to convert to. (default: google)",
        type=writer.OutputStyle,
        choices=list(writer.OutputStyle),
    )
    arg_parser.add_argument(
        "--in-place",
        help="Write the changes to the input file instead of printing diffs.",
        action="store_true",
    )
    arg_parser.add_argument(
        "-c", "--config", help="Location of configuration file to use."
    )
    arg_parser.add_argument(
        "-t",
        "--threads",
        type=int,
        default=0,
        help="Number of threads to use. (default: cpu count)",
    )
    arg_parser.add_argument(
        "-v", "--verbose", action="store_true", help="Log more information."
    )
    args = arg_parser.parse_args()
    setup_logger(verbose=args.verbose)
    source = os.path.abspath(os.path.expanduser(args.source))
    if not os.path.exists(source):
        _LOGGER.error("Path does not exist: %s", source)
        return
    if not is_git_repository(source):
        _LOGGER.warning(
            "This directory is not under git control. "
            "Continuing will overwrite files."
        )
        answer = input("Are you sure you would like to proceed? [y/n] ")
        if answer.lower() not in ("y", "yes"):
            _LOGGER.warning("Exiting without converting.")
            return
    config = configuration.DocconvertConfiguration.create_default()
    if args.config:
        config_path = os.path.abspath(os.path.expanduser(args.config))
        if not os.path.exists(config_path):
            _LOGGER.error("Config path does not exist: %s", config_path)
            return
        config.update_from_json(config_path)
    # Override config values if specified directly with flags
    if args.input:
        config.input_style = args.input
    if args.output:
        config.output_style = args.output
    diffs = core.convert(source, args.threads, config, args.in_place)
    if diffs and not args.in_place:
        for diff in diffs:
            for line in diff:
                sys.stdout.write(line)


if __name__ == "__main__":
    sys.exit(run())
