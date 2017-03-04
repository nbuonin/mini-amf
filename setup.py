#!/usr/bin/env python

# Copyright (c) The PyAMF Project.
# See LICENSE.txt for details.

# import ordering is important
import setupinfo
from setuptools import setup, find_packages

from pyamf._version import version

name = "Mini-PyAMF"
description = "AMF serialization and deserialization support for Python"
long_description = setupinfo.read('README.rst')
url = "https://github.com/zackw/minipyamf"
author = "Zack Weinberg, The PyAMF Project"
author_email = "zackw@panix.com"
license = "MIT License"

classifiers = """
Intended Audience :: Developers
Intended Audience :: Information Technology
License :: OSI Approved :: MIT License
Natural Language :: English
Operating System :: OS Independent
Programming Language :: C
Programming Language :: Python
Programming Language :: Cython
Programming Language :: Python :: 2.7
Topic :: Internet :: WWW/HTTP :: WSGI :: Application
Topic :: Software Development :: Libraries :: Python Modules
Development Status :: 5 - Production/Stable
"""

keywords = """
amf amf0 amf3 flex flash remoting rpc http flashplayer air bytearray
objectproxy arraycollection recordset actionscript decoder encoder gateway
remoteobject twisted pylons django sharedobject lso sol
"""


def setup_package():

    setup(
        name=name,
        version=str(version),
        description=description,
        long_description=long_description,
        url=url,
        author=author,
        author_email=author_email,
        keywords=keywords.strip(),
        license=license,
        packages=find_packages(),
        ext_modules=setupinfo.get_extensions(),
        install_requires=setupinfo.get_install_requirements(),
        test_suite="pyamf.tests.get_suite",
        zip_safe=False,
        extras_require=setupinfo.get_extras_require(),
        classifiers=[
            l for l in (ll.strip() for ll in classifiers.splitlines()) if l
        ],
        **setupinfo.extra_setup_args())


if __name__ == '__main__':
    setup_package()
