=====================
 Installation Guide
=====================

.. contents::

Mini-PyAMF requires Python_ 2.7 or 3.4+, and DefusedXML_.


Easy Installation
=================

The easiest way to install Mini-PyAMF is with ``pip``::

    pip install mini-pyamf


Manual Installation
===================

First install DefusedXML_.  If you wish to build the C accelerator
module, you will also need a C compiler and the libraries for
compiling Python extensions.

:doc:`community/download` and unpack the PyAMF archive of your choice::

    tar zxfv Mini-PyAMF-<version>.tar.gz
    cd Mini-PyAMF-<version>

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
- a :doc:`copy <community/download>` of the PyAMF source distribution

Then, from the ``doc`` subdirectory of the source distribution, run
this command::

    sphinx-build -b html . build

This will generate HTML documentation in the ``doc/build/html``
folder. This documentation is identical to the content on the main PyAMF
website_.

.. _Python: 			http://www.python.org
.. _DefusedXML:                 https://pypi.python.org/pypi/defusedxml
.. _Sphinx:     		http://sphinx.pocoo.org
.. _Epydoc:			http://epydoc.sourceforge.net
.. _sphinxcontrib.epydoc:       http://packages.python.org/sphinxcontrib-epydoc
.. _ElementTree:		http://effbot.org/zone/element-index.htm
.. _website:    		https://github.com/hydralabs/pyamf

.. _lxml:			http://lxml.de
.. _uuid:			http://pypi.python.org/pypi/uuid
.. _wsgiref:			http://pypi.python.org/pypi/wsgiref
.. _cElementTree: 		http://effbot.org/zone/celementtree.htm
.. _SQLAlchemy:			http://www.sqlalchemy.org
.. _Twisted:			http://twistedmatrix.com
.. _Django:			http://www.djangoproject.com
.. _Google App Engine: 		http://code.google.com/appengine
.. _`python-pyamf`: http://packages.debian.org/python-pyamf
.. _Elixir:			http://elixir.ematia.de
.. _unittest2:			http://pypi.python.org/pypi/unittest2
.. _nose:			http://somethingaboutorange.com/mrl/projects/nose
.. _Trial:			http://twistedmatrix.com/trac/wiki/TwistedTrial
.. _Cython:			http://cython.org
.. _Installing Python Modules: 	http://docs.python.org/install/index.html
