"""
This module file supports basic functions from stdlib.h library
"""

from ..utils.utils import definition
from ..interpreter.memory import findEmptyMemoryMalloc
from ..interpreter.memory import findEmptyMemoryCalloc

@definition(return_type='int', arg_types=['int'])
def malloc(n):
    return findEmptyMemoryMalloc(n.value)


@definition(return_type='int', arg_types=['int', 'int'])
def calloc(n, m):
    return findEmptyMemoryCalloc(n.value * m.value)
