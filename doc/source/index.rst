==========
Docconvert
==========

**docconvert** will parse one or several python files and retrieve existing
docstrings. Then, for all found modules/functions/methods/classes, it will
convert docstring formatting (including parameters, returns, and other
fields) to the newly specified style.

Currently, the managed styles in input/output are:

**Input**

-  epytext_
-  reST_ (re-Structured Text, as used by Sphinx)

**Output**

-  google_
-  numpy_
-  epytext_
-  reST_ (re-Structured Text, as used by Sphinx)


Contents
========
.. toctree::
    :maxdepth: 2

    intro
    contributing

Release Notes
=============
.. toctree::
    :maxdepth: 2

    release_notes


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. _epytext: http://epydoc.sourceforge.net/manual-fields.html
.. _reST: http://www.sphinx-doc.org/en/master/usage/restructuredtext/domains.html#info-field-lists
.. _google: https://www.sphinx-doc.org/en/master/usage/extensions/example_google.html#example-google
.. _numpy: https://www.sphinx-doc.org/en/master/usage/extensions/example_numpy.html#example-numpy
