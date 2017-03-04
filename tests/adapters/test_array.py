# Copyright (c) The PyAMF Project.
# See LICENSE.txt for details.

"""
Tests for the L{array} L{miniamf.adapters._array} module.

@since: 0.5
"""

import array
import unittest

import miniamf


class ArrayTestCase(unittest.TestCase):
    """
    """

    def setUp(self):
        self.orig = ['f', 'o', 'o']

        self.obj = array.array('c')

        self.obj.append('f')
        self.obj.append('o')
        self.obj.append('o')

    def encdec(self, encoding):
        return miniamf.decode(
            miniamf.encode(self.obj, encoding=encoding),
            encoding=encoding).next()

    def test_amf0(self):
        self.assertEqual(self.encdec(miniamf.AMF0), self.orig)

    def test_amf3(self):
        self.assertEqual(self.encdec(miniamf.AMF3), self.orig)
