Release Notes
=============

Versions follow `Semantic Versioning <https://semver.org/>`_
(``<major>.<minor>.<patch>``).

v2.2.0 (2024-10-20)
-------------------
Features
^^^^^^^^
* Add new config option to convert epytext markup to reST equivalents. (#7)
* Support not writing return types for google and reST when use_types is off. (#4)

Bugfixes
^^^^^^^^
* Fix as parsing error when using ellipsis in nested scopes. (#11)
* Fix issue where docstring after variable assignment were getting skipped by module parser.

Misc
^^^^
* Drop official support for python2.7. We will no longer run tests
  against python2.7 when making changes.

v2.1.0 (2023-01-30)
-------------------
Features
^^^^^^^^
* Support async function definitions in docstring parsing. (#8)

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
* Support converting docstrings nested inside functions. (#1)
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
