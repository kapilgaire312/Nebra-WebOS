from cpu_architecture.isa import Opcode

from os_engine.process import ProcessState
from os_engine.utils import reg_index


def handle_add(cpu, process, operands: list):
    r0, r1, r2 = operands

    result = cpu.registers[reg_index(r1)] + cpu.registers[reg_index(r2)]
    cpu.registers[reg_index(r0)] = result

    # update the flags
    if result == 0:
        cpu.flags.zero = True

    else:
        cpu.flags.zero = False

    cpu.program_counter += 1


def handle_subtract(cpu, process, operands: list):
    r0, r1, r2 = operands

    result = cpu.registers[reg_index(r1)] - cpu.registers[reg_index(r2)]
    cpu.registers[reg_index(r0)] = result

    # update the flags
    if result == 0:
        cpu.flags.zero = True

    else:
        cpu.flags.zero = False

    cpu.program_counter += 1


def handle_halt(cpu, process, operands: list):
    # syscall to kernel, which reclaims its resources. implement later.
    process.transition_to(ProcessState.TERMINATED)


def handle_jmp(cpu, process, operands: list):
    jump_label = operands.pop()
    cpu.program_counter = jump_label


def handle_jz(
    cpu, process, operands
):  # jumps if the result of previous operation was zero.
    if cpu.flags.zero:
        jump_label = operands.pop()
        cpu.program_counter = jump_label

    else:
        cpu.program_counter += 1


OPCODE_HANDLERS = {
    Opcode.ADD: handle_add,
    Opcode.HALT: handle_halt,
    Opcode.SUBTRACT: handle_subtract,
    Opcode.JMP: handle_jmp,
    Opcode.JZ: handle_jz,
}
