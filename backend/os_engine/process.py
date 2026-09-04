from dataclasses import dataclass
from enum import Enum, auto

from os_engine.cpu_architecture.isa import Instruction


class ProcessState(Enum):
    NEW = auto()
    READY = auto()
    RUNNING = auto()
    WAITING = auto()
    TERMINATED = auto()


@dataclass()
class Process:
    process_id: int
    instructions: list[Instruction]
    process_state: ProcessState
    saved_register_values: list
    saved_program_counter_value: int = 0

    def transition_to(self, state: ProcessState):
        # check the validity of transition
        self.process_state = state
