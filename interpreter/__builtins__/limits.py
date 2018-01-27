"""
This module file supports basic functions from limits.h library
"""
from ..utils.utils import definition

@definition(return_type='int')
def INT_MAX():
    return 2147483647

@definition(return_type='int')
def INT_MIN():
    return -2147483648

@definition(return_type='short')
def SHORT_MAX():
    return 32767

@definition(return_type='short')
def SHORT_MIN():
    return -32768

@definition(return_type='int')
def LONG_MAX():
    return 9223372036854775807

@definition(return_type='int')
def LONG_MIN():
    return -9223372036854775808

@definition(return_type='int')
def CHAR_MAX():
    return 127

@definition(return_type='int')
def CHAR_MIN():
    return -128

@definition(return_type='int')
def SCHAR_MAX():
    return 127

@definition(return_type='int')
def SCHAR_MIN():
    return -128

@definition(return_type='int')
def CHAR_BIT():
    return 8