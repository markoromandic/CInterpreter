import random
from .number import Number
from ..syntax_analysis.tree import VarDecl, Var

import numbers

bytesMem = 1 * 1024

memoryLocation = 0

address = {}


def initializeAddress(numBytes=1024):
    for i in range(0, numBytes):
        address[i] = Value(chr(random.randint(32, 127)), False)


def readFromMemory(num_bit, location):
    global address
    rez = 0
    if num_bit == 1:
        rez = address[location].value
    else:
        for i in range(0, num_bit):
            rez |= address[location + i].value << ((num_bit - 1 - i) * 8)
    return rez

def findEmptyMemoryMalloc(num_byte):
    location = 0

    while True:
        find = 1
        location += 1

        for j in range(location, location + num_byte):
            if address[j].used is True:
                find = 0
        if find is 1:
            break

    for j in range(location, location + num_byte):
        address[j].used = True

    return location

def findEmptyMemoryCalloc(num_byte):
    location = 0

    while True:
        find = 1
        location += 1

        for j in range(location, location + num_byte):
            if address[j].used is True:
                find = 0
        if find is 1:
            break

    for j in range(location, location + num_byte):
        address[j].used = True
        address[j].value = 0

    return location


def findEmptyMemory(num_bit):
    location = 0

    while True:
        find = 1
        location += 1

        for j in range(location, location + num_bit):
            if address[j].used is True:
                find = 0
        if find is 1:
            return location

    return 0

def getByteType(type):

    if type == 'char':
        return 1
    elif type == 'short':
        return 2
    elif type == 'int':
        return 4
    elif type == 'long':
        return 8
    elif type == 'float':
        return 1
    elif type == 'double':
        return 1
    elif type == 'unsigned_char':
        return 1
    elif type == 'unsigned_short':
        return 2
    elif type == 'unsigned_int':
        return 4
    elif type == 'unsigned_long':
        return 8
    elif type == 'unsigned':
        return 4
    else:
        return -1

def writeToMemory(location, num_byte, value):
    global address
    if num_byte == 1:
        address[location] = Value(value=value, used=True)
    else:
        for i in range(0, num_byte):
            address[location + i] = Value(value=(value >> (8 * (num_byte - 1 - i))) & 0xFF, used=True)

class Value(object):
    def __init__(self, value, used=False):
        self.value = value
        self.used = used

    def __str__(self):
        return self.value

    def setValue(self, newValue):
        self.value = newValue


class Variable(object):

    def __init__(self, type, name, memoryLocation):
        self.type = type
        self.name = name
        self.memoryLocation = memoryLocation

    def __str__(self):
        return self.type

    def getName(self):
        return self.name


    def getLocation(self):
        return self.memoryLocation

class Scope(object):
    def __init__(self, scope_name, parent_scope=None):
        self.scope_name = scope_name
        self.parent_scope = parent_scope
        self._values = dict()

    def __setitem__(self, key, value):
        global address, memoryLocation

        if isinstance(key, Var):
            print('POINTERS ASSIGN', key.num_dereferences, key.value)
            key = key.value
        if isinstance(key, VarDecl):
            var_type = key.type_node.value
            var_pointer_num = key.var_node.num_dereferences
            print('POINTER DECLARATION:', var_pointer_num)
            var_name = key.var_node.value
            var_memoryLocation = findEmptyMemory(getByteType(var_type))

            newVar = Variable(type=var_type, name=var_name, memoryLocation=var_memoryLocation)

            self._values[var_name] = newVar

            return 0

        if isinstance(value, Number) and key in self._values.keys():
            # memoryLocation = findEmptyMemory(getByteType(value.type))
            newVar = self._values[key]
            number = Number(ttype=newVar.type, value=value.value)
            writeToMemory(location=newVar.memoryLocation, num_byte=getByteType(newVar.type), value=number.value)
            return
        elif isinstance(value, Number):
            memoryLocation = findEmptyMemory(getByteType(value.type))
            newVar = Variable(type=value.type, name=key, memoryLocation=memoryLocation)
            writeToMemory(location=memoryLocation, num_byte=getByteType(newVar.type), value=value.value)
            self._values[key] = newVar
            return
        elif isinstance(value, Value):
            memoryLocation = findEmptyMemory(1)
            if isinstance(value.value, numbers.Number):
                address[memoryLocation] = Value(value=value.value, used=True)
            else:
                address[memoryLocation] = Value(value=value, used=True)
        else:
            memoryLocation = findEmptyMemory(1)
            address[memoryLocation] = Value(value=value, used=True)

        if isinstance(value,Number):
            newVar = Variable(value.type, key, memoryLocation)
        elif isinstance(value, Value):
            if isinstance(value.value, numbers.Number):
                newVar = Variable('ASSIGN', key, memoryLocation)
            else:
                newVar = Variable(type(value).__name__, key, memoryLocation)
        else:
            newVar = Variable(type(value).__name__, key, memoryLocation)

        self._values[key] = newVar


    def readFromMemory(num_byte, location):
        global address
        rez = 0
        if num_bit == 1:
            rez = address[location].value
        else:
            for i in range(0, num_bit):
                rez |= address[location + i].value << ((num_bit - 1 - i) * 8)
        return rez


    def __getitem__(self, item):
        global address

        if isinstance(item, Var):
            print('POINTERS ASSIGN', item.num_dereferences, item.value)
            item = item.value

        varCur = self._values[item]
        addressLocation = varCur.getLocation()

        result = address[addressLocation]

        if varCur.type == 'short':
            rez = readFromMemory(2, addressLocation)
            result = Number(ttype=varCur.type, value=rez)
        elif varCur.type == 'int':
            rez = readFromMemory(4, addressLocation)
            result = Number(ttype=varCur.type, value=rez)
        elif varCur.type == 'long':
            rez = readFromMemory(8, addressLocation)
            result = Number(ttype=varCur.type, value=rez)
        elif varCur.type == 'float':
            rez = readFromMemory(1, addressLocation)
            result = Number(ttype=varCur.type, value=rez)
        elif varCur.type == 'unsigned_char':
            rez = readFromMemory(1, addressLocation)
            result = Number(ttype=varCur.type, value=rez)
        elif varCur.type == 'unsigned_short':
            rez = readFromMemory(2, addressLocation)
            result = Number(ttype=varCur.type, value=rez)
        elif varCur.type == 'unsigned_int':
            rez = readFromMemory(4, addressLocation)
            result = Number(ttype=varCur.type, value=rez)
        elif varCur.type == 'unsigned_long':
            rez = readFromMemory(8, addressLocation)
            result = Number(ttype=varCur.type, value=rez)
        elif varCur.type == 'unsigned':
            rez = readFromMemory(4, addressLocation)
            result = Number(ttype=varCur.type, value=rez)

        if varCur.type == 'ASSIGN':
            result = Number(ttype='int', value=result.value)

        if type(result).__name__ == 'Value':
            result = result.value

        return result

    def __contains__(self, key):
        if isinstance(key, Var):
            key = key.value
        return key in self._values

    def remove(self, key):
        global address

        varCur = self._values[key]
        addressLocation = varCur.memoryLocation

        result = readFromMemory(4, addressLocation)

        for i in range(0, getByteType(varCur.type)):
            address[addressLocation + i].used = False
        res = Number(ttype=varCur.type, value=result)
        return res

    def __repr__(self):
        lines = [
            '{}:{}'.format(key, val) for key, val in self._values.items()
        ]
        title = '{}\n'.format(self.scope_name)
        return title + '\n'.join(lines)

    def deleteScope(self):
        for v in self._values:
            addressLocation = self._values[v].memoryLocation
            for i in range(addressLocation, addressLocation + getByteType(v.type)):
                address[addressLocation + i].used = False

class Frame(object):
    def __init__(self, frame_name, global_scope):
        self.frame_name = frame_name
        self.current_scope = Scope(
            '{}.scope_00'.format(frame_name),
            global_scope
        )
        self.scopes = [self.current_scope]

    def new_scope(self):
        self.current_scope = Scope(
            '{}{:02d}'.format(
                self.current_scope.scope_name[:-2],
                int(self.current_scope.scope_name[-2:]) + 1
            ),
            self.current_scope
        )
        self.scopes.append(self.current_scope)

    def del_scope(self):
        current_scope = self.current_scope

        self.current_scope = current_scope.parent_scope
        self.scopes.pop(-1)
        current_scope.deleteScope()
        del current_scope

    def __contains__(self, key):
        return key in self.current_scope

    def __repr__(self):
        lines = [
            '{}\n{}'.format(
                scope,
                '-' * 40
            ) for scope in self.scopes
        ]

        title = 'Frame: {}\n{}\n'.format(
            self.frame_name,
            '*' * 40
        )

        return title + '\n'.join(lines)


class Stack(object):
    def __init__(self):
        self.frames = list()
        self.current_frame = None

    def __bool__(self):
        return bool(self.frames)

    def new_frame(self, frame_name, global_scope=None):
        frame = Frame(frame_name, global_scope=global_scope)
        self.frames.append(frame)
        self.current_frame = frame

    def del_frame(self):
        self.frames.pop(-1)
        self.current_frame = len(self.frames) and self.frames[-1] or None

    def __repr__(self):
        lines = [
            '{}'.format(frame) for frame in self.frames
        ]
        return '\n'.join(lines)


class Memory(object):
    def __init__(self):
        initializeAddress(bytesMem)
        self.global_frame = Frame('GLOBAL_MEMORY', None)
        self.stack = Stack()

    def declare(self, key, value=random.randint(0, 2 ** 32)):
        ins_scope = self.stack.current_frame.current_scope if self.stack.current_frame else self.global_frame.current_scope
        ins_scope[key] = value

    def __setitem__(self, key, value):
        ins_scope = self.stack.current_frame.current_scope if self.stack.current_frame else self.global_frame.current_scope
        curr_scope = ins_scope
        while curr_scope and key not in curr_scope:
            curr_scope = curr_scope.parent_scope
        ins_scope = curr_scope if curr_scope else ins_scope
        ins_scope[key] = value

    def __getitem__(self, item):
        curr_scope = self.stack.current_frame.current_scope if self.stack.current_frame else self.global_frame.current_scope
        while curr_scope and item not in curr_scope:
            curr_scope = curr_scope.parent_scope
        return curr_scope[item]

    def new_frame(self, frame_name):
        self.stack.new_frame(frame_name, self.global_frame.current_scope)

    def del_frame(self):
        self.stack.del_frame()

    def new_scope(self):
        self.stack.current_frame.new_scope()

    def del_scope(self):
        self.stack.current_frame.del_scope()

    def __repr__(self):
        return "{}\nStack\n{}\n{}".format(
            self.global_frame,
            '=' * 40,
            self.stack
        )

    def __str__(self):
        return self.__repr__()
