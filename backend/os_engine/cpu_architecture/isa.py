"""Instruction set architecture:
- commands that CPU understands.
"""

from dataclasses import dataclass
from enum import IntEnum


class Opcode(IntEnum):
    # 6 bit opcode will be used. so 64 posisble opcodes (0x00 to 0x3F)
    ADD = 0x00
    HALT = 0x01
    SUBTRACT = 0x02
    JMP = 0x03  # unconditional jump
    JZ = 0x04  # jump on zero


@dataclass()
class Instruction:
    opcode: Opcode
    operands: list
