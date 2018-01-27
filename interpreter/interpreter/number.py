import math

MAX_SHORT = 32767
MIN_SHORT = -32768

MAX_INT = 2147483647
MIN_INT = -2147483648

MAX_LONG = 9223372036854775807
MIN_LONG = -9223372036854775808

MIN_CHAR = -128
MAX_CHAR = 127

MAX_UNSIGNED_SHORT = 65535
MAX_UNSIGNED_INT = 4294967295
MAX_UNSGINED_LONG = 18446744073709551615
MAX_UNSGINED = MAX_UNSIGNED_INT
MAX_UNSIGNED_CHAR = 255

class Number(object):
    types = dict(char=int, short=int, int=int, long=int, unsigned_short=int, unsigned_int=int, unsigned_long=int,
                 unsigned=int, unsigned_char=int, float=float, double=float)
    order = ('char', 'short', 'int', 'long', 'unsigned_short', 'unsigned_int', 'unsigned_long', 'unsigned',
             'unsigned_char', 'float', 'double')

    def __init__(self, ttype, value):
        self.type = ttype
        if ttype == 'short':
            if Number.types[ttype](value) < MIN_SHORT:
                self.value = MAX_SHORT - (Number.types[ttype](value) % (MIN_SHORT - 1))
            elif Number.types[ttype](value) > MAX_SHORT:
                self.value = MIN_SHORT + (Number.types[ttype](value) % (MAX_SHORT + 1))
            else:
                self.value = Number.types[ttype](value)
        elif ttype == 'int':
            if Number.types[ttype](value) < MIN_INT:
                self.value = MAX_INT - (Number.types[ttype](value) % (MIN_INT - 1))
            elif Number.types[ttype](value) > MAX_INT:
                self.value = MIN_INT + (Number.types[ttype](value) % (MAX_INT + 1))
            else:
                self.value = Number.types[ttype](value)
        elif ttype == 'long':
            if Number.types[ttype](value) < MIN_LONG:
                self.value = MAX_LONG - (Number.types[ttype](value) % (MIN_LONG - 1))
            elif Number.types[ttype](value) > MAX_LONG:
                self.value = MIN_LONG + (Number.types[ttype](value) % (MAX_LONG + 1))
            else:
                self.value = value
        elif ttype == 'char':
            if Number.types[ttype](value) < MIN_CHAR:
                self.value = MAX_CHAR - (Number.types[ttype](value) % (MIN_CHAR - 1))
            elif Number.types[ttype](value) > MAX_CHAR:
                self.value = MIN_CHAR + (Number.types[ttype](value) % (MAX_CHAR + 1))
            else:
                self.value = value
        elif ttype == 'unsigned_short':
            if Number.types[ttype](value) < 0:
                self.value = MAX_UNSIGNED_SHORT - (Number.types[ttype](value) % (0 - 1))
            self.value = value
        elif ttype == 'unsigned_int':
            if Number.types[ttype](value) < 0:
                self.value = MAX_UNSIGNED_INT - (Number.types[ttype](value) % (0 - 1))
            self.value = value
        elif ttype == 'unsigned_long':
            if Number.types[ttype](value) < 0:
                self.value = MAX_UNSGINED_LONG - (Number.types[ttype](value) % (0 - 1))
            self.value = value
        elif ttype == 'unsigned':
            if Number.types[ttype](value) < 0:
                self.value = MAX_UNSGINED - (Number.types[ttype](value) % (0 - 1))
            self.value = value
        elif ttype == 'unsigned_char':
            if Number.types[ttype](value) < 0:
                self.value = MAX_UNSIGNED_CHAR - (Number.types[ttype](value) % (0 - 1))
            self.value = value

    def _get_res_type(self, other):
        left_order = Number.order.index(self.type)
        right_order = Number.order.index(other.type)
        ttype = Number.order[max(left_order, right_order)]
        return ttype, Number.types[ttype]

    def __add__(self, other):
        """ self + other """
        ttype, ctype = self._get_res_type(other)

        return Number(ttype, ctype(self.value) + ctype(other.value))

    def __sub__(self, other):
        """ self - other """
        ttype, ctype = self._get_res_type(other)
        return Number(ttype, ctype(self.value) - ctype(other.value))

    def __mul__(self, other):
        """ self * other """
        ttype, ctype = self._get_res_type(other)
        return Number(ttype, ctype(self.value) * ctype(other.value))

    def __truediv__(self, other):
        """ self / other """
        ttype, ctype = self._get_res_type(other)
        if ctype == int:
            return Number(ttype, ctype(self.value) // ctype(other.value))
        return Number(ttype, ctype(self.value) / ctype(other.value))

    def __mod__(self, other):
        """ self % other """
        ttype, ctype = self._get_res_type(other)

        if ctype != int:
            raise TypeError("invalid operands of types '{}' and '{}' to binary ‘operator %’".format(
                self.type,
                other.type
            ))
        return Number(ttype, ctype(self.value) % ctype(other.value))

    def __gt__(self, other):
        """ self > other """
        ttype, ctype = self._get_res_type(other)
        return Number('int', int(ctype(self.value) > ctype(other.value)))

    def __ge__(self, other):
        """ self >= other """
        ttype, ctype = self._get_res_type(other)
        return Number('int', int(ctype(self.value) >= ctype(other.value)))

    def __lt__(self, other):
        """ self < other """
        ttype, ctype = self._get_res_type(other)
        return Number('int', int(ctype(self.value) < ctype(other.value)))

    def __le__(self, other):
        """ self <= other """
        ttype, ctype = self._get_res_type(other)
        return Number('int', int(ctype(self.value) <= ctype(other.value)))

    def __eq__(self, other):
        """ self == other """
        ttype, ctype = self._get_res_type(other)
        return Number('int', int(ctype(self.value) == ctype(other.value)))

    def __ne__(self, other):
        """ self != other """
        ttype, ctype = self._get_res_type(other)
        return Number('int', int(ctype(self.value) != ctype(other.value)))

    def __iadd__(self, other):
        """ self += other """
        ctype = Number.types[self.type]
        result = self + other
        return Number(self.type, ctype(result.value))

    def __isub__(self, other):
        """ self -= other """
        ctype = Number.types[self.type]
        result = self - other
        return Number(self.type, ctype(result.value))

    def __imul__(self, other):
        """ self *= other """
        ctype = Number.types[self.type]
        result = self * other
        return Number(self.type, ctype(result.value))

    def __itruediv__(self, other):
        """ self /= other """
        ctype = Number.types[self.type]
        result = self / other
        return Number(self.type, ctype(result.value))

    def __and__(self, other):
        """ self & other """
        ttype, ctype = self._get_res_type(other)
        return Number(ttype, int(ctype(self.value) & ctype(other.value)))

    def __or__(self, other):
        """ self | other """
        ttype, ctype = self._get_res_type(other)
        return Number(ttype, int(ctype(self.value) | ctype(other.value)))

    def __xor__(self, other):
        """ self ^ other """
        ttype, ctype = self._get_res_type(other)
        return Number(ttype, int(ctype(self.value) ^ ctype(other.value)))

    def __bool__(self):
        return bool(self.value)

    def _not(self):
        return Number('int', 0) if self.value else Number('int', 1)

    def __repr__(self):
        return '{} ({})'.format(
            self.type,
            self.value
        )

    def __str__(self):
        return self.__repr__()
