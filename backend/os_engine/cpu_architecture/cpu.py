from dataclasses import dataclass, field
from enum import Enum, auto

from cpu_architecture.opcode_handlers import OPCODE_HANDLERS

from os_engine.process import Process


@dataclass()
class Flags:
    zero = False  # the result was 0
    negative: bool = False  # result was negative
    carry: bool = False  # add/sub was done with a carry/borrow
    overflow: bool = False  # signed arithmetic overflowed


class CPUMode(Enum):
    USER = auto()
    KERNEL = auto()


@dataclass()
class CPU:
    page_table_pointer: int
    program_counter: int = 0
    registers: list = field(
        default_factory=lambda: [0, 0, 0, 0]
    )  # using field instead of = [0,0,0,0] will avoid all objects pointing to same list.

    flags: Flags = field(default_factory=lambda: Flags())

    mode: CPUMode = CPUMode.USER

    def fetch_one_instruction(self, process):
        # for now fetch and decode are in the execute until a proper memory mangaement unit is implemented.
        pass

    def decode_one_instruction(self):
        pass

    def execute_one_instruction(self, process: Process):
        instruction = process.instructions[self.program_counter]
        handler = OPCODE_HANDLERS[instruction.opcode]
        handler(self, process, instruction.operands)

    def increment_one_tick(self):
        pass
