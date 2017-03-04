# Copyright (c) The PyAMF Project.
# See LICENSE.txt for details.

"""
Adapter for the stdlib C{sets} module.

@since: 0.4
"""

import sets

import pyamf
from pyamf.adapters import util

pyamf.add_type(frozenset, util.to_tuple)
pyamf.add_type(set, util.to_tuple)

pyamf.add_type(sets.ImmutableSet, util.to_tuple)
pyamf.add_type(sets.Set, util.to_tuple)
