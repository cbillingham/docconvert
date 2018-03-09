# Docconvert

Update or convert docstrings in existing Python files, managing several styles.

This Python (2.7+/3+) module and script intends to help Python programmers to
enhance internal code documentation using docstrings.
It is useful to harmonize or change a project docstring style format.

It will parse one or several python scripts and retrieve existing docstrings.
Then, for all found modules/functions/methods/classes, it will convert docstrings
with parameters, returns, and other fields formatted in the newly specified style.
At the end, the python files are overwritten.

Currently, the managed styles in input/output are:

#### Input

- [epytext][1]
- [reST][2] (re-Structured Text, as used by Sphinx)

#### Output

- [google][3]


## Getting Started

### Installation

Docconvert can be installed through pip:

```bash
pip install docconvert
```

### Usage

```bash
usage: docconvert [-h] [-i {guess,rest,epytext}] [-o {google}] [--in-place]
                  [-c CONFIG] [-t THREADS] [-v]
                  source

positional arguments:
  source                The directory or file to convert.

optional arguments:
  -h, --help            show this help message and exit
  -i {epytext,guess,rest}, --input {epytext,guess,rest}
                        Input docstring style. (default: guess)
  -o {google}, --output {google}
                        Output docstring style to convert to. (default:
                        google)
  --in-place            Write the changes to the input file instead of
                        printing diffs.
  -c CONFIG, --config CONFIG
                        Location of configuration file to use.
  -t THREADS, --threads THREADS
                        Number of threads to use. (default: cpu count)
  -v, --verbose         Log more information.
```

Examples:

Convert files in `src/mypackage` from epytext to google using 4 threads.

    docconvert --input epytext --output google --threads 4 src/mypackage/

Convert file `src/mypackage/myfile.py` from rest to google.

    docconvert --input rest --output google src/mypackage/myfile.py

#### Custom Configuration

You can configure optional conversion arguments in a json config file. Just
specify a config filepath to the commandline tool.

    docconvert --config path/to/config.json src/mypackage/

Detailed description of all configuration options can be found in the
full user documentation.


## Contributing

### Running the Tests

Tests are executed through [tox][5].

```bash
tox
```

Tests are written with [pytest][6]. Please add unit tests under the
`tests/` directory to cover any new functionality you have added.

### Code Style

Code is formatted using [black][7].

You can check your formatting using black's check mode:

```bash
tox -e formatting
```

You can also get black to format your changes for you:

```bash
black --exclude tests/test_resources/fixtures/ src/ tests/
```

### Building Documentation

You can build the documentation through tox.

```bash
tox -e docs
```

The built documentation will be output to doc/build

### Releasing

Before releasing please remember to:

- Run the tests and check that they pass
- Update version in `doc/source/conf.py`, `src/docconvert/__init__.py`, `setup.py`
- Build the new documentation
- Add new release notes to `RELEASE_NOTES.rst`


## Versioning

We use [SemVer][4] for versioning.
For the versions available, see the tags on this repository.


## License

This project is licensed under the BSD-3-Clause License.
See the LICENSE.md file for details.


[1]: http://epydoc.sourceforge.net/manual-fields.html
[2]: http://www.sphinx-doc.org/en/stable/domains.html#info-field-lists
[3]: http://www.sphinx-doc.org/en/stable/ext/example_google.html
[4]: http://semver.org/
[5]: https://tox.readthedocs.io/en/latest/
[6]: https://docs.pytest.org/en/latest/
[7]: https://github.com/python/black
[8]: https://pre-commit.com/
