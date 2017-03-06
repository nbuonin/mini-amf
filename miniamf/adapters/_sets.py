# Copyright (c) The PyAMF Project.
# See LICENSE.txt for details.

"""
Adapter for the stdlib C{sets} module.

@since: 0.4
"""

from __future__ import absolute_import

import miniamf
from miniamf.adapters import util


miniamf.add_type(frozenset, util.to_tuple)
miniamf.add_type(set, util.to_tuple)


# The sets module was removed in Python 3.
try:
    ModuleNotFoundError
except NameError:
    ModuleNotFoundError = ImportError

try:
    import sets
    miniamf.add_type(sets.ImmutableSet, util.to_tuple)
    miniamf.add_type(sets.Set, util.to_tuple)
except ModuleNotFoundError:
    pass
