from dataclasses import dataclass, field
from enum import Enum, auto

from os_engine.cpu_architecture.opcode_handlers import OPCODE_HANDLERS

from os_engine.process.model import Process
from os_engine.cpu_architecture.isa import Instruction

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
    registers: list[int] = field(
        default_factory=lambda: [0]*32
    )  # using field instead of = [0,0,0,0,...] will avoid all objects pointing to same list.

    flags: Flags = field(default_factory=lambda: Flags())

    mode: CPUMode = CPUMode.USER

    def fetch_one_instruction(self, ram):
        from os_engine.memory.memory_request import MemoryRequest

        return MemoryRequest.read_instruction(
            virtual_address=self.program_counter, cpu=self, ram=ram
        )

    def decode_one_instruction(self, instruction: int):
        # decode the instruction into opcode and operands
        instruction_obj = Instruction(instruction) 
        
        return instruction_obj


    def execute_one_instruction(self, instruction_obj: Instruction):

        handler = OPCODE_HANDLERS[instruction_obj.opcode]

        handler(self, instruction_obj.operands)

    def increment_one_tick(self):
        pass
