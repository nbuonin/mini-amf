# -*- coding: utf-8 -*-
#
# Copyright (c) The PyAMF Project.
# See LICENSE.txt for details.

"""
Provides the pure Python versions of L{BufferedByteStream}.

Do not reference directly, use L{miniamf.util.BufferedByteStream} instead.

@since: 0.6
"""

from __future__ import absolute_import
import struct

from cStringIO import StringIO
import six


def _get_endian_system():
    encoded = struct.pack('@I', 0x01020304)
    if encoded == '\x01\x02\x03\x04':
        return ENDIAN_BIG
    elif encoded == '\x04\x03\x02\x01':
        return ENDIAN_LITTLE
    else:
        raise ValueError("unrecognized system endianness: %r" % (encoded,))


#: Network byte order
ENDIAN_NETWORK = "!"

#: Native byte order
ENDIAN_NATIVE = "@"

#: Little endian
ENDIAN_LITTLE = "<"

#: Big endian
ENDIAN_BIG = ">"

#: System endian (whichever of '<' or '>' corresponds to the behavior of '@').
ENDIAN_SYSTEM = _get_endian_system()

#: All valid endianness strings
VALID_ENDIANS = (ENDIAN_NETWORK, ENDIAN_NATIVE, ENDIAN_LITTLE, ENDIAN_BIG)


def _compile_packers(endian):
    """
    Compile struct packers for all of the formats used by BufferedByteStream.
    Called whenever a BufferedByteStream's endianness is changed.
    """
    return {
        'b': struct.Struct(endian + 'b'),
        'h': struct.Struct(endian + 'h'),
        'H': struct.Struct(endian + 'H'),
        'l': struct.Struct(endian + 'l'),
        'L': struct.Struct(endian + 'L'),
        'd': struct.Struct(endian + 'd'),
        'f': struct.Struct(endian + 'f')
    }


# Note: cStringIO.StringIO is not a type and cannot be subclassed.
class BufferedByteStream(object):
    """
    I am a C{StringIO} type object containing byte data from the AMF stream.

    Features:
     - Always read-write.
     - Raises L{IOError} if reading past end.
     - Allows you to C{peek()} into the stream.
     - Knows its length.

    @see: U{ByteArray on OSFlash
        <http://osflash.org/documentation/amf3#x0c_-_bytearray>}
    @see: U{Parsing ByteArrays on OSFlash
        <http://osflash.org/documentation/amf3/parsing_byte_arrays>}

    @ivar endian: Byte ordering used to represent the data. Default byte order
        is L{ENDIAN_NETWORK}.
    @type endian: ENDIAN_* code
    """

    def __init__(self, buf=None, endian=ENDIAN_NETWORK):
        """
        @raise TypeError: Unable to coerce C{buf} to C{StringIO}.
        """

        self.endian = endian
        self._buf = StringIO()
        self._len = 0

        if buf is not None:
            if not isinstance(buf, (six.binary_type, buffer)):
                if hasattr(buf, 'getvalue'):
                    buf = buf.getvalue()
                elif (hasattr(buf, 'read') and
                      hasattr(buf, 'seek') and
                      hasattr(buf, 'tell')):
                    old_pos = buf.tell()
                    buf.seek(0)
                    s = buf.read()
                    buf.seek(old_pos, 0)
                    buf = s
                else:
                    raise TypeError("Unable to coerce %r to a byte buffer"
                                    % (buf,))

            self._buf.write(buf)
            self._buf.seek(0, 0)
            self._len = len(buf)

    def __len__(self):
        if self._len is None:
            old_pos = self._buf.tell()
            self._buf.seek(0, 2)

            self._len = self._buf.tell()
            self._buf.seek(old_pos)
        return self._len

    def seek(self, offset, whence=0):
        return self._buf.seek(offset, whence)

    def tell(self):
        return self._buf.tell()

    def truncate(self, size=0):
        self._buf.truncate(size)
        self._len = None

    def getvalue(self):
        return self._buf.getvalue()

    def write(self, s):
        """
        Writes the content of the specified C{s} into this buffer.

        @param s: Raw bytes
        """
        self._buf.write(s)
        self._len = None

    def consume(self):
        """
        Discard all of the data already read (from byte 0 up to C{tell()})
        and reset the read position to the new beginning of the stream.

        @since: 0.4
        """
        bytes = self._buf.read()
        self._buf.truncate(0)

        if len(bytes) > 0:
            self._buf.write(bytes)
            self._buf.seek(0)

        self._len = None

    def read(self, length=-1):
        """
        If C{length} is -1 or unspecified, reads the rest of the buffer.
        Otherwise, reads exactly the specified number of bytes from the
        buffer.

        @raise IOError: Attempted to read past the end of the buffer.
        """
        if length == 0:
            return ''
        if length < -1:
            raise IOError("invalid read length: %r" % length)
        if self.at_eof():
            raise IOError(
                'Attempted to read from the buffer but already at the end')

        if length == -1:
            return self._buf.read()
        else:
            if self._buf.tell() + length > len(self):
                raise IOError(
                    'Attempted to read %d bytes from the buffer but only %d '
                    'remain' % (length, len(self) - self.tell())
                )
            return self._buf.read(length)

    def peek(self, size=1):
        """
        Looks C{size} bytes ahead in the stream, returning what it finds,
        returning the stream pointer to its initial position.

        @param size: Default is 1.
        @type size: C{int}
        @raise ValueError: Trying to peek backwards.

        @return: Bytes.
        """
        if size == -1:
            return self.peek(len(self) - self.tell())

        if size < -1:
            raise ValueError("Cannot peek backwards")

        bytes = ''
        pos = self.tell()

        while not self.at_eof() and len(bytes) != size:
            bytes += self.read(1)

        self.seek(pos)

        return bytes

    def remaining(self):
        """
        Returns number of remaining bytes.

        @rtype: C{number}
        @return: Number of remaining bytes.
        """
        return len(self) - self.tell()

    def at_eof(self):
        """
        Returns C{True} if the internal pointer is at the end of the stream.

        @rtype: C{bool}
        """
        return self.tell() == len(self)

    def append(self, data):
        """
        Append data to the end of the stream. The pointer will not move if
        this operation is successful.

        @param data: The data to append to the stream.
        @type data: string
        @raise TypeError: data is not a string
        """
        t = self.tell()

        # seek to the end of the stream
        self.seek(0, 2)

        if hasattr(data, 'getvalue'):
            self.write_utf8_string(data.getvalue())
        else:
            self.write_utf8_string(data)

        self.seek(t)

    def __add__(self, other):
        old_pos = self.tell()
        old_other_pos = other.tell()

        new = BufferedByteStream(self)

        other.seek(0)
        new.seek(0, 2)
        new.write(other.read())

        self.seek(old_pos)
        other.seek(old_other_pos)
        new.seek(0)

        return new

    # Methods for reading and writing typed data.
    @property
    def endian(self):
        """The endianness of this stream."""
        return self._endian

    @endian.setter
    def endian(self, val):
        if val not in VALID_ENDIANS:
            raise ValueError("invalid endianness code %r" % (val,))
        self._endian = val
        self._packers = _compile_packers(val)

    def _is_little_endian(self):
        if self._endian == ENDIAN_NATIVE:
            return ENDIAN_SYSTEM == ENDIAN_LITTLE
        else:
            return self._endian == ENDIAN_LITTLE

    def read_uchar(self):
        """
        Reads an C{unsigned char} from the stream.
        """
        return ord(self.read(1))

    def write_uchar(self, c):
        """
        Writes an C{unsigned char} to the stream.

        @param c: Unsigned char
        @type c: C{int}
        @raise TypeError: Unexpected type for int C{c}.
        @raise OverflowError: Not in range.
        """
        if not isinstance(c, six.integer_types):
            raise TypeError('expected an int (got:%r)' % type(c))

        if not 0 <= c <= 255:
            raise OverflowError("Not in range, %d" % c)

        self.write(chr(c))

    def read_char(self):
        """
        Reads a C{char} from the stream.
        """
        return self._packers["b"].unpack(self.read(1))[0]

    def write_char(self, c):
        """
        Write a C{char} to the stream.

        @param c: char
        @type c: C{int}
        @raise TypeError: Unexpected type for int C{c}.
        @raise OverflowError: Not in range.
        """
        if not isinstance(c, six.integer_types):
            raise TypeError('expected an int (got:%r)' % type(c))

        if not -128 <= c <= 127:
            raise OverflowError("Not in range, %d" % c)

        self.write(self._packers["b"].pack(c))

    def read_ushort(self):
        """
        Reads a 2 byte unsigned integer from the stream.
        """
        return self._packers["H"].unpack(self.read(2))[0]

    def write_ushort(self, s):
        """
        Writes a 2 byte unsigned integer to the stream.

        @param s: 2 byte unsigned integer
        @type s: C{int}
        @raise TypeError: Unexpected type for int C{s}.
        @raise OverflowError: Not in range.
        """
        if not isinstance(s, six.integer_types):
            raise TypeError('expected an int (got:%r)' % (type(s),))

        if not 0 <= s <= 65535:
            raise OverflowError("Not in range, %d" % s)

        self.write(self._packers["H"].pack(s))

    def read_short(self):
        """
        Reads a 2 byte integer from the stream.
        """
        return self._packers["h"].unpack(self.read(2))[0]

    def write_short(self, s):
        """
        Writes a 2 byte integer to the stream.

        @param s: 2 byte integer
        @type s: C{int}
        @raise TypeError: Unexpected type for int C{s}.
        @raise OverflowError: Not in range.
        """
        if not isinstance(s, six.integer_types):
            raise TypeError('expected an int (got:%r)' % (type(s),))

        if not -32768 <= s <= 32767:
            raise OverflowError("Not in range, %d" % s)

        self.write(self._packers["h"].pack(s))

    def read_ulong(self):
        """
        Reads a 4 byte unsigned integer from the stream.
        """
        return self._packers["L"].unpack(self.read(4))[0]

    def write_ulong(self, l):
        """
        Writes a 4 byte unsigned integer to the stream.

        @param l: 4 byte unsigned integer
        @type l: C{int}
        @raise TypeError: Unexpected type for int C{l}.
        @raise OverflowError: Not in range.
        """
        if not isinstance(l, six.integer_types):
            raise TypeError('expected an int (got:%r)' % (type(l),))

        if not 0 <= l <= 4294967295:
            raise OverflowError("Not in range, %d" % l)

        self.write(self._packers["L"].pack(l))

    def read_long(self):
        """
        Reads a 4 byte integer from the stream.
        """
        return self._packers["l"].unpack(self.read(4))[0]

    def write_long(self, l):
        """
        Writes a 4 byte integer to the stream.

        @param l: 4 byte integer
        @type l: C{int}
        @raise TypeError: Unexpected type for int C{l}.
        @raise OverflowError: Not in range.
        """
        if not isinstance(l, six.integer_types):
            raise TypeError('expected an int (got:%r)' % (type(l),))

        if not -2147483648 <= l <= 2147483647:
            raise OverflowError("Not in range, %d" % l)

        self.write(self._packers["l"].pack(l))

    def read_24bit_uint(self):
        """
        Reads a 24 bit unsigned integer from the stream.

        @since: 0.4
        """
        if self._is_little_endian():
            order = [0, 8, 16]
        else:
            order = [16, 8, 0]

        n = 0
        for x in order:
            n += (self.read_uchar() << x)

        return n

    def write_24bit_uint(self, n):
        """
        Writes a 24 bit unsigned integer to the stream.

        @since: 0.4
        @param n: 24 bit unsigned integer
        @type n: C{int}
        @raise TypeError: Unexpected type for int C{n}.
        @raise OverflowError: Not in range.
        """
        if not isinstance(n, six.integer_types):
            raise TypeError('expected an int (got:%r)' % (type(n),))

        if not 0 <= n <= 0xffffff:
            raise OverflowError("n is out of range")

        if self._is_little_endian():
            order = [0, 8, 16]
        else:
            order = [16, 8, 0]

        for x in order:
            self.write_uchar((n >> x) & 0xff)

    def read_24bit_int(self):
        """
        Reads a 24 bit integer from the stream.

        @since: 0.4
        """
        n = self.read_24bit_uint()

        if n & 0x800000 != 0:
            # the int is signed
            n -= 0x1000000

        return n

    def write_24bit_int(self, n):
        """
        Writes a 24 bit integer to the stream.

        @since: 0.4
        @param n: 24 bit integer
        @type n: C{int}
        @raise TypeError: Unexpected type for int C{n}.
        @raise OverflowError: Not in range.
        """
        if not isinstance(n, six.integer_types):
            raise TypeError('expected an int (got:%r)' % (type(n),))

        if not -8388608 <= n <= 8388607:
            raise OverflowError("n is out of range")

        if n < 0:
            n += 0x1000000

        if self._is_little_endian():
            order = [0, 8, 16]
        else:
            order = [16, 8, 0]

        for x in order:
            self.write_uchar((n >> x) & 0xff)

    def read_double(self):
        """
        Reads an 8 byte float from the stream.
        """
        return self._packers["d"].unpack(self.read(8))[0]

    def write_double(self, d):
        """
        Writes an 8 byte float to the stream.

        @param d: 8 byte float
        @type d: C{float}
        @raise TypeError: Unexpected type for float C{d}.
        """
        if not isinstance(d, float):
            raise TypeError('expected a float (got:%r)' % (type(d),))

        self.write(self._packers["d"].pack(d))

    def read_float(self):
        """
        Reads a 4 byte float from the stream.
        """
        return self._packers["f"].unpack(self.read(4))[0]

    def write_float(self, f):
        """
        Writes a 4 byte float to the stream.

        @param f: 4 byte float
        @type f: C{float}
        @raise TypeError: Unexpected type for float C{f}.
        """
        if not isinstance(f, float):
            raise TypeError('expected a float (got:%r)' % (type(f),))

        self.write(self._packers["f"].pack(f))

    def read_utf8_string(self, length):
        """
        Reads a UTF-8 string from the stream.

        @rtype: Unicode string
        """
        return self.read(length).decode('utf-8')

    def write_utf8_string(self, u):
        """
        Writes a string to the stream.  If it is a Unicode object,
        it will be encoded in UTF-8; if it is a byte string, it will
        be written out as-is.

        @param u: string
        @raise TypeError: Unexpected type for C{u}
        """
        if isinstance(u, six.text_type):
            u = u.encode('utf-8')
        if not isinstance(u, six.binary_type):
            raise TypeError('Expected a string, not %r' % (u,))
        self.write(u)
