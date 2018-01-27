CInterpreter
=============
CInterpreter is a very small C interpreter written in Python from scratch. Project was written as a part of course
Compiler Construction at [The Faculty Of Computer Science](https://raf.edu.rs/).

Interpreter was designed and written by [Slađan Kantar](https://github.com/SKantar), without using additional libraries. You can easily rewrite this to any other language. 

My team upgraded the interpreter to:
* Simulate memory addresses
* Simulate pointers
* Dynamic allocation of the memory
* Simulate n-dimensional arrays
* Break
* Continue
* Switch-case
* Data types (short, int, long, float, double, unsigned, etc.)
* Adding restrictions to data types
* Added more libraries (math.h, stdlib.h, limits.h)

With this interpreter you can execute codes like following:

* [example1](example1.c)
* [example2](example2.c)
* [example3](example3.c)
* [example4](example4.c)

## Setup
**Prerequsite**:<br/>
    - Install [python3.5](https://www.python.org) or later, preferably use a virtualenv.<br/>

### Running interpreter
To execute c program, run `python3 __main__.py -f <file>`.

For example, to run the [example1](example1.c):
```bash
cd CInterpreter
python3 __main__.py -f example1.c
```
