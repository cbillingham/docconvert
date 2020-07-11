Release Notes
=============

Versions follow `Semantic Versioning <https://semver.org/>`_
(``<major>.<minor>.<patch>``).

v2.0.0 (2020-07-11)
-------------------

Breaking Changes
^^^^^^^^^^^^^^^^
* Remove google specific output from config and moved
  ``use_types`` and ``separate_keywords`` into global output config.

Features
^^^^^^^^
* Support numpy docstring output.
* Support reST docstring output.
* Support epytext docstring output.

v1.2.0 (2020-06-08)
-------------------

Features
^^^^^^^^
* `#1 <https://github.com/cbillingham/docconvert/issues/1>`_:
  Support converting docstrings nested inside functions.
* Add support for Python 3.8.

v1.1.0 (2018-06-17)
-------------------

Features
^^^^^^^^
* Output diffs by default, add in-place flag for overwriting files in place.
* Can convert attribute docstrings.

v1.0.0 (2018-03-12)
-------------------

* Initial release.
