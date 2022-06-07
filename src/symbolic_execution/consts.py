from collections import namedtuple

BITS_IN_BYTE = 8
SymbolicExecutionProperties = namedtuple('SymbolicExecutionProperties', ['load_dynamic_libaries', 'len_symbolic_bits'])