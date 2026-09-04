from cpu_architecture.isa import Opcode

from os_engine.cpu_architecture.utils.set_cpu_flags import set_cpu_arithmetic_flags
from os_engine.process import ProcessState

MASK = 0xFFFFFFFF  # any value written to register needs to be maske to ensure it is 32 bit value.


def handle_add(cpu, process, operands: list[int]):
    # r1 = r2 +r3

    r1, r2, remaining_16_bits = operands
    r3 = (remaining_16_bits >> 11) & 0x1F

    result = cpu.registers[(r2)] + cpu.registers[(r3)]
    result = result & MASK  # to only keep 32 bit value in case overflow occurs
    cpu.registers[r1] = result

    # update the flags
    set_cpu_arithmetic_flags(cpu=cpu, opcode=Opcode.ADD, result=result, op1=r2, op2=r3)

    cpu.program_counter += 1


def handle_subtract(cpu, process, operands: list[int]):
    # r1 = r2 - r3
    r1, r2, remaining_16_bits = operands
    r3: int = (remaining_16_bits >> 11) & 0x1F

    result = cpu.registers[r1] - cpu.registers[r2]
    result = result & MASK

    cpu.registers[r3] = result

    # update the flags
    set_cpu_arithmetic_flags(
        cpu=cpu, opcode=Opcode.SUBTRACT, result=result, op1=r2, op2=r3
    )
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
