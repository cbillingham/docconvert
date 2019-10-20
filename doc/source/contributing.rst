.. _contributing:

Contributing
============

Running the Tests
-----------------

Tests are executed through tox_.

.. code-block:: bash

    tox


Tests are written with pytest_. Please add unit tests under the
`tests/` directory to cover any new functionality you have added.

Code Style
----------

Code is formatted using black_.

You can check your formatting using black's check mode:

.. code-block:: bash

    tox -e formatting


You can also use pre-commit_ to format every commit with black:

.. code-block:: bash

    pip install pre-commit
    pre-commit install


Building Documentation
----------------------

You can build the documentation through tox.

.. code-block:: bash

    tox -e docs


The built documentation will be output to doc/build

Releasing
---------

Before releasing please remember to:

1. Run the tests and check that they pass
2. Build the new documentation and check it
3. Update version in ``doc/source/conf.py``,
   ``src/docconvert/__init__.py``, and ``setup.cfg``
4. Add new release notes to ``RELEASE_NOTES.rst``
5. Commit, tag the version number, and push the changes

To release

.. code-block:: bash

    git clean -idx
    python setup.py sdist bdist_wheel
    twine upload dist/*


.. _tox: https://tox.readthedocs.io/en/latest/
.. _pytest: https://docs.pytest.org/en/latest/
.. _black: https://github.com/python/black
.. _pre-commit: https://pre-commit.com/
