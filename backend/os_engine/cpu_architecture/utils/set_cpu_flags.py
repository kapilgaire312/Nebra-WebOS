"""
set the values of zero, negative, carry and overflow cpu flags.
"""

from os_engine.cpu_architecture.cpu import CPU
from os_engine.cpu_architecture.isa import Opcode

WORD_BITS = 32
MASK = 0xFFFFFFFF
SIGN_BIT = 0x80000000  # check the MSB. if it is 1 in a signed bit then it is negative.


def set_cpu_arithmetic_flags(
    cpu: CPU, opcode: Opcode, result: int, op1: int = 0, op2: int = 0
):
    flags = cpu.flags
    match opcode:
        case Opcode.ADD:
            value = op1 + op2

            flags.zero = result == 0
            flags.negative = bool(result & SIGN_BIT)
            flags.carry = value > MASK
            flags.overflow = (~(op1 ^ op2) & (op1 ^ result) & SIGN_BIT) != 0

        case Opcode.SUBTRACT:
            value = op1 - op2

            flags.zero = result == 0
            flags.negative = bool(result & SIGN_BIT)
            flags.carry = op1 < op2  # borrow
            flags.overflow = ((op1 ^ op2) & (op1 ^ result) & SIGN_BIT) != 0
