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


class Instruction:
    """
    The instruction is 32 bit fixed length instruction.
    format:
    opcode |  reg_1 | reg_2 | reg_3/immediate/offset/unused

    opcode - 6 bits
    reg_1-> 5 bits (32bit register) = destination (depends on opcode hanlders implementaion)
    reg_2-> 5 bits (32bit register) = source
    reg_3/immediate/offset/unused -> 16 bits = load immediate values, offset for things like arrays or empty.


    instead of having multiple formats like real system.
    in this architecture, the opcode handler will decide if the last 16 bits is a register, immediate value or offset.
    This lets us have 3 register system instead of 2 which makes the compilation easier.

    """

    # opcode: Opcode | None = None
    # operands: list[int] | None =None  # list of [reg_1(5 bits), reg_2(5 bits)-, remaining_16_bits]

    def __init__(self, instruction_bits: int):
        opcode: int = (instruction_bits >> 26) & 0x3F
        r1: int = (instruction_bits >> 21) & 0x1F  # maksing with 00000011111
        r2: int = (instruction_bits >> 16) & 0x1F
        remaining_16_bits: int = instruction_bits & 0xFFFF

        self.opcode = Opcode(opcode)
        self.operands = [r1, r2, remaining_16_bits]

    # create instructions for testing.
    def construct_instruction(
        self, opcode: Opcode, r1: int, r2: int, remaining_16_bits: int
    ):
        self.opcode = opcode
        self.operands = [r1, r2, remaining_16_bits]
