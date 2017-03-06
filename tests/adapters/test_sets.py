# Copyright (c) The PyAMF Project.
# See LICENSE.txt for details.

"""
Tests for the C{sets} module integration.
"""

from __future__ import absolute_import

import unittest

import miniamf
from ..util import check_buffer

# All set types are mapped to simple tuples.
class BaseTestCase(unittest.TestCase):
    def amf0_encode_test(self, ty):
        x = ty(['1', '2', '3'])

        self.assertTrue(check_buffer(
            miniamf.encode(x, encoding=miniamf.AMF0).getvalue(), (
                b'\n\x00\x00\x00\x03', (
                    b'\x02\x00\x011',
                    b'\x02\x00\x013',
                    b'\x02\x00\x012'
                )
            )
        ))

    def amf3_encode_test(self, ty):
        x = ty(['1', '2', '3'])

        self.assertTrue(check_buffer(
            miniamf.encode(x, encoding=miniamf.AMF3).getvalue(), (
                b'\t\x07\x01', (
                    b'\x06\x031',
                    b'\x06\x033',
                    b'\x06\x032'
                )
            )
        ))


class BuiltinSetTypesTestCase(BaseTestCase):
    def test_amf0_set(self):
        self.amf0_encode_test(set)

    def test_amf3_set(self):
        self.amf3_encode_test(set)

    def test_amf0_frozenset(self):
        self.amf0_encode_test(frozenset)

    def test_amf3_frozenset(self):
        self.amf3_encode_test(frozenset)


# The sets module was removed in Python 3.
try:
    ModuleNotFoundError
except NameError:
    ModuleNotFoundError = ImportError

try:
    import sets

    class LibrarySetTypesTestCase(BaseTestCase):
        def test_amf0_Set(self):
            self.amf0_encode_test(sets.Set)

        def test_amf3_Set(self):
            self.amf3_encode_test(sets.Set)

        def test_amf0_ImmutableSet(self):
            self.amf0_encode_test(sets.ImmutableSet)

        def test_amf3_ImmutableSet(self):
            self.amf3_encode_test(sets.ImmutableSet)

except ModuleNotFoundError:
    pass
