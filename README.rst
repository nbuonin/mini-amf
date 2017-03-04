==========
Mini-PyAMF
==========

Mini-PyAMF provides Action Message Format (AMF_) serialization and
deserialization support for Python_, compatible with the `Adobe Flash
Player`_.  It supports Python 2.7 and 3.4+.

.. image:: https://travis-ci.org/hydralabs/pyamf.svg?branch=master
    :target: https://travis-ci.org/hydralabs/pyamf
.. image:: https://coveralls.io/repos/hydralabs/pyamf/badge.svg
   :target: https://coveralls.io/r/hydralabs/pyamf

Mini-PyAMF is a trimmed-down version of the `original PyAMF`_, which
(as far as I can tell) is no longer being maintained.  It retains the
same API, but provides only the core serialization and deserialization
logic.  All of the integration with various server-side web
frameworks, ORMs, alternative XML parsers, etc. has been scrapped, as
has support for `Adobe Flex`_.
(You can still define your own framework-integration "adapter"
classes, and you can still hook in your own XML parser.)

Mini-PyAMF is lightly maintained by `Zack Weinberg`_.  All bug reports
and pull requests will be heard and responded to, but I have no plans
to develop the software any further myself.  (In particular, I would
happily take patches that built this back up into a complete
replacement for PyAMF, but don't be waiting for me to do it.)
(Also, please note that patches to restore support for old versions of
Python 2 will *not* be accepted, as this interferes with support for
Python 3.)

What's AMF?
-----------

The `Adobe Integrated Runtime`_ and `Adobe Flash Player`_ use AMF to
communicate between an application and a remote server. AMF encodes
remote procedure calls (RPC) into a compact binary representation that
can be transferred over HTTP/HTTPS or the `RTMP/RTMPS`_ protocol.
Objects and data values are serialized into this binary format, which
increases performance, allowing applications to load data up to 10 times
faster than with text-based formats such as XML or SOAP.

AMF3, the default serialization for ActionScript_ 3.0, provides various
advantages over AMF0, which is used for ActionScript 1.0 and 2.0. AMF3
sends data over the network more efficiently than AMF0. AMF3 supports
sending ``int`` and ``uint`` objects as integers and supports data types
that are available only in ActionScript 3.0, such as ByteArray.

.. _AMF: https://en.wikipedia.org/wiki/Action_Message_Format
.. _Python: https://www.python.org
.. _Adobe Flash Player: https://en.wikipedia.org/wiki/Flash_Player
.. _original PyAMF: https://github.com/hydralabs/pyamf
.. _Zack Weinberg: https://www.owlfolio.org/

.. _Adobe Integrated Runtime: https://en.wikipedia.org/wiki/Adobe_AIR
.. _RTMP/RTMPS:	https://en.wikipedia.org/wiki/Real_Time_Messaging_Protocol
.. _ActionScript: https://en.wikipedia.org/wiki/ActionScript
