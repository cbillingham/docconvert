# Docconvert

[![Build Status](https://github.com/cbillingham/docconvert/actions/workflows/test.yaml/badge.svg?branch=main)](https://github.com/cbillingham/docconvert/actions/workflows/test.yaml)
[![Documentation](https://readthedocs.org/projects/docconvert/badge/?version=latest)](https://docconvert.readthedocs.io)
[![PyPI Version](https://img.shields.io/pypi/v/docconvert.svg)](https://pypi.org/project/docconvert/)
[![Supported Python Versions](https://img.shields.io/pypi/pyversions/docconvert.svg)](https://pypi.org/project/docconvert/)
[![Formatted with Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)

Update or convert docstrings in existing Python files.

This Python (3.9+) module and script intends to help Python programmers to
enhance internal code documentation using docstrings.
It is useful to harmonize or change a project docstring style format.

It will parse one or several python scripts and retrieve existing docstrings.
Then, for all found modules/functions/methods/classes, it will convert docstrings
with parameters, returns, and other fields formatted in the newly specified style.

Currently, the managed styles in input/output are:

#### Input

- [epytext][1]
- [reST][2] (re-Structured Text, as used by Sphinx)

#### Output

- [google][3]
- [numpy][7]
- [epytext][1]
- [reST][2] (re-Structured Text, as used by Sphinx)


## Getting Started

### Installation

Docconvert can be installed through pip:

```bash
pip install docconvert
```

### Usage

```bash
usage: docconvert [-h] [-i {guess,rest,epytext}] [-o {google,numpy,rest,epytext}]
                  [--in-place] [-c CONFIG] [-t THREADS] [-v]
                  source

positional arguments:
  source                The directory or file to convert.

optional arguments:
  -h, --help            show this help message and exit
  -i {guess,rest,epytext}, --input {guess,rest,epytext}
                        Input docstring style. (default: guess)
  -o {google,numpy,rest,epytext}, --output {google,numpy,rest,epytext}
                        Output docstring style to convert to. (default: google)
  --in-place            Write the changes to the input file instead of printing diffs.
  -c CONFIG, --config CONFIG
                        Location of configuration file to use.
  -t THREADS, --threads THREADS
                        Number of threads to use. (default: cpu count)
  -v, --verbose         Log more information.
```

Examples:

Convert files in `src/mypackage` to google using 4 threads.

```bash
docconvert --output google --threads 4 src/mypackage/
```

Convert file `src/mypackage/myfile.py` from rest to google.

```bash
docconvert --input rest --output google src/mypackage/myfile.py
```

#### Custom Configuration

You can configure optional conversion arguments in a json config file. Just
specify a config filepath to the commandline tool.

```bash
docconvert --config path/to/config.json src/mypackage/
```

Detailed description of all configuration options can be found in the
[documentation][5].


## Contributing

If you would like to contribute, please take a look at the
[contributor documentation][6].


## Versioning

We use [SemVer][4] for versioning.
For the versions available, see the tags on the repository.

### Python 2.7

We tried really hard to have this package support both Python 2 and 3 for a
long time. We've dropped Python 2 support officially. Its just become
cumbersome to automate tests for. However, the code will probably still
work in Python 2.7+ *I think*. Good luck!

## License

This project is licensed under the BSD-3-Clause License.
See the LICENSE.md file for details.


[1]: http://epydoc.sourceforge.net/manual-fields.html
[2]: https://www.sphinx-doc.org/en/master/usage/restructuredtext/domains.html#info-field-lists
[3]: https://www.sphinx-doc.org/en/master/usage/extensions/example_google.html#example-google
[4]: http://semver.org/
[5]: https://docconvert.readthedocs.io/
[6]: https://docconvert.readthedocs.io/en/latest/contributing.html
[7]: https://www.sphinx-doc.org/en/master/usage/extensions/example_numpy.html#example-numpy
