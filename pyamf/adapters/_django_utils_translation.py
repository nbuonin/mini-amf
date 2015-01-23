# Copyright (c) The PyAMF Project.
# See LICENSE.txt for details.

"""
C{django.utils.translation} adapter module.

@see: U{Django Project<http://www.djangoproject.com>}
@since: 0.4.2
"""

from django.utils.translation import ugettext_lazy
from six import text_type
import pyamf


def convert_lazy(l, encoder=None):
    try:
        return text_type(l)
    except Exception as e:
        raise ValueError(
            'Don\'t know how to convert lazy value ' +repr(l)) from e

pyamf.add_type(type(ugettext_lazy('foo')), convert_lazy)
