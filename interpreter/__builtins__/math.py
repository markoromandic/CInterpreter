"""
This module file supports basic functions from math.h library
"""

from ..utils.utils import definition
import math

@definition(return_type='double', arg_types=['double'])
def sqrt(a):
    return math.sqrt(a.value)

@definition(return_type='double', arg_types=['double'])
def ceil(a):
    return math.ceil(a.value)

@definition(return_type='double', arg_types=['double'])
def acos(a):
    return math.acos(a.value)

@definition(return_type='double', arg_types=['double'])
def asin(a):
    return math.asin(a.value)

@definition(return_type='double', arg_types=['double'])
def atan(a):
    return math.atan(a.value)

@definition(return_type='double', arg_types=['double'])
def cos(a):
    return math.cos(a.value)

@definition(return_type='double', arg_types=['double'])
def cosh(a):
    return math.cosh(a.value)

@definition(return_type='double', arg_types=['double'])
def sin(a):
    return math.sin(a.value)

@definition(return_type='double', arg_types=['double'])
def sinh(a):
    return math.sinh(a.value)

@definition(return_type='double', arg_types=['double'])
def tan(a):
    return math.tan(a.value)

@definition(return_type='double', arg_types=['double'])
def tanh(a):
    return math.tanh(a.value)

@definition(return_type='double', arg_types=['double'])
def exp(a):
    return math.exp(a.value)

@definition(return_type='double', arg_types=['double'])
def log(a):
    return math.log1p(a.value)

@definition(return_type='double', arg_types=['double'])
def log10(a):
    return math.log10(a.value)

@definition(return_type='double', arg_types=['double'])
def fabs(a):
    return math.fabs(a.value)
