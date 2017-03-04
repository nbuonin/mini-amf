=====================
 Installation Guide
=====================

.. contents::

Mini-AMF requires Python_ 2.7 or 3.4+, and DefusedXML_.


Easy Installation
=================

The easiest way to install Mini-AMF is with ``pip``::

    pip install mini-amf


Manual Installation
===================

First install DefusedXML_.  If you wish to build the C accelerator
module, you will also need a C compiler and the libraries for
compiling Python extensions.

:doc:`community/download` and unpack the Mini-AMF archive of your choice::

    tar zxfv Mini-AMF-<version>.tar.gz
    cd Mini-AMF-<version>

Then install using the ``setup.py`` script::

    python setup.py install

This will byte-compile the Python source code and install it in the
``site-packages`` directory of your Python installation.

To disable the installation of the C accelerator module, supply the
``--disable-ext`` option::

    python setup.py install --disable-ext


Unit Tests
==========

Unit tests can also be run via ``setup.py``.  No additional modules
are required::

    python setup.py test


C Accelerator Module
====================

To modify the C accelerator module, you will need Cython_.  If it is
installed, the C source code will automatically be regenerated from
the ``.pyx`` files during the build.

Documentation
=============

To build the main documentation you need:

- Sphinx_ 1.0 or newer
- Epydoc_ 3.0 or newer
- `sphinxcontrib.epydoc`_ 0.4 or newer
- a :doc:`copy <community/download>` of the Mini-AMF source distribution

Then, from the ``doc`` subdirectory of the source distribution, run
this command::

    sphinx-build -b html . build

This will generate HTML documentation in the ``doc/build/html``
folder. This documentation is identical to the content on the main Mini-AMF
website_.

.. _Python: 			https://www.python.org/
.. _DefusedXML:                 https://pypi.python.org/pypi/defusedxml
.. _Cython:			http://cython.org
.. _Sphinx:     		http://www.sphinx-doc.org/
.. _Epydoc:			http://epydoc.sourceforge.net/
.. _sphinxcontrib.epydoc:       http://packages.python.org/sphinxcontrib-epydoc
.. _website:    		https://github.com/hydralabs/miniamf

