#!/usr/bin/env python

# Copyright (c) The PyAMF Project.
# See LICENSE.txt for details.

name = "Mini-AMF"
description = "AMF serialization and deserialization support for Python"
url = "https://github.com/zackw/mini-amf"
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
amf amf0 amf3 actionscript air flash flashplayer bytearray recordset
decoder encoder sharedobject lso sol
"""

import sys
import os.path
import fnmatch

try:
    from Cython.Distutils import build_ext

    have_cython = True
except ImportError:
    from setuptools.command.build_ext import build_ext

    have_cython = False

from setuptools.command import sdist
from setuptools import Extension, setup
from distutils.core import Distribution


jython = sys.platform.startswith("java")
can_compile_extensions = not jython


class MyDistribution(Distribution):
    """
    This seems to be is the only obvious way to add a global option to
    distutils.

    Provide the ability to disable building the extensions for any called
    command.
    """

    global_options = Distribution.global_options + [
        ("disable-ext", None, "Disable building extensions.")
    ]

    def finalize_options(self):
        Distribution.finalize_options(self)

        try:
            i = self.script_args.index("--disable-ext")
        except ValueError:
            self.disable_ext = False
        else:
            self.disable_ext = True
            self.script_args.pop(i)


class MyBuildExt(build_ext):
    """
    The companion to L{MyDistribution} that checks to see if building the
    extensions are disabled.
    """

    def run(self, *args, **kwargs):
        if self.distribution.disable_ext:
            return

        build_ext.run(self, *args, **kwargs)


class MySDist(sdist.sdist):
    """
    We generate the Cython code for a source distribution
    """

    def cythonise(self):
        ext = MyBuildExt(self.distribution)
        ext.initialize_options()
        ext.finalize_options()

        ext.check_extensions_list(ext.extensions)

        for e in ext.extensions:
            e.sources = ext.cython_sources(e.sources, e)

    def run(self):
        if not have_cython:
            print("ERROR - Cython is required to build source distributions")

            raise SystemExit(1)

        self.cythonise()

        return sdist.sdist.run(self)


def make_extension(mod_name, **extra_options):
    """
    Tries is best to return an Extension instance based on the mod_name
    """
    base_name = os.path.join(mod_name.replace(".", os.path.sep))

    if have_cython:
        for ext in [".pyx", ".py"]:
            source = base_name + ext

            if os.path.exists(source):
                return Extension(mod_name, [source], **extra_options)

        print("WARNING: Could not find Cython source for %r" % (mod_name,))
    else:
        source = base_name + ".c"

        if os.path.exists(source):
            return Extension(mod_name, [source], **extra_options)

        print("WARNING: Could not build extension for %r, no source found" % (
            mod_name,))

def get_extensions():
    """
    Return a list of Extension instances that can be compiled.
    """
    if not can_compile_extensions:
        print(80 * "*")
        print("WARNING:")
        print(
            "\tAn optional code optimization (C extension) could not be "
            "compiled.\n\n"
        )
        print("\tOptimizations for this package will not be available!\n\n")
        print("Compiling extensions is not supported on %r" % (sys.platform,))
        print(80 * "*")

        return []

    extensions = []

    for p in recursive_glob(".", "*.pyx"):
        mod_name = os.path.splitext(p)[0].replace(os.path.sep, ".")

        e = make_extension(mod_name)

        if e:
            extensions.append(e)

    return extensions


def recursive_glob(path, pattern):
    matches = []

    for root, dirnames, filenames in os.walk(path):
        for filename in fnmatch.filter(filenames, pattern):
            matches.append(os.path.normpath(os.path.join(root, filename)))

    return matches



def setup_package():

    with open(os.path.join(os.path.dirname(__file__), "README.rst"), "rt") as f:
        long_description=f.read()

    from miniamf._version import version

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
        packages=["miniamf"],
        ext_modules=get_extensions(),
        install_requires=["defusedxml"],
        test_suite="tests",
        zip_safe=False,
        extras_require={},
        classifiers=[
            l for l in (ll.strip() for ll in classifiers.splitlines()) if l
        ],
        distclass=MyDistribution,
        cmdclass={
            "build_ext": MyBuildExt,
            "sdist": MySDist
        },
        package_data={
            "miniamf._accel": ["*.pxd"]
        }
    )

if __name__ == "__main__":
    setup_package()
