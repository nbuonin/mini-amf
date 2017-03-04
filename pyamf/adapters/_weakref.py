# Copyright (c) The PyAMF Project.
# See LICENSE.txt for details.

"""
C{weakref} support.

@since: 0.6.2
"""

import weakref

import pyamf
from pyamf.adapters import util


def get_referent(reference, **kwargs):
    return reference()


pyamf.add_type(weakref.ref, get_referent)
pyamf.add_type(weakref.WeakValueDictionary, util.to_dict)
pyamf.add_type(weakref.WeakSet, util.to_list)
