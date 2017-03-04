============
  Features
============

Here's a brief description of the features in PyAMF. The
:doc:`CHANGES <../changelog>` document contains a more detailed
summary of all new features.

- :mod:`AMF0 <pyamf.amf0>` encoder/decoder for legacy Adobe Flash Players (version 6-8)
- :mod:`AMF3 <pyamf.amf3>` encoder/decoder for the new AMF format in Adobe Flash Player 9
  and newer
- Optional C-extension for maximum performance, created using `Cython`_
- Remoting gateway for any compatible WSGI_ framework
- :doc:`Adapter framework <../architecture/adapters>`
- :doc:`Authentication <../tutorials/general/authentication/index>`/``setCredentials`` support
- Python AMF :doc:`client <../tutorials/general/client>` with HTTP(S)
  and authentication support
- Service Browser requests supported
- :doc:`Local Shared Object <../tutorials/general/sharedobject>`
  support

Also see the plans for :doc:`future development <future>`.

.. _WSGI: https://wsgi.readthedocs.io/
.. _Cython: http://cython.org
