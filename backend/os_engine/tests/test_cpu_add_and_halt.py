from os_engine.cpu_architecture.cpu import CPU
from os_engine.cpu_architecture.isa import Instruction, Opcode
from os_engine.process.model import Process, ProcessState
from os_engine.process.memory_descriptor import MemoryDescriptor, MemoryRegion, RegionPermission, RegionType
from os_engine.memory.pte import PTE
from os_engine.memory.ram import RAM


def test_cpu_add_and_halt():
    mm = MemoryDescriptor(
        page_table_pointer=0x1000,
        regions=[
            MemoryRegion(start=0x0000, end=0x0FFF, permissions=RegionPermission.RX, type=RegionType.CODE),
            MemoryRegion(start=0x1000, end=0x1FFF, permissions=RegionPermission.RW, type=RegionType.DATA),
        ]
    )
    proc = Process(
        process_id=1,
        process_state=ProcessState.RUNNING,
        saved_program_counter_value=0x0000,
        saved_register_values=[0, 5, 3, 0],
        memory_descriptor=mm
    )

    ram = RAM()
    code_page = PTE()
    code_page.construct_from_data_entries(
        physical_frame_number=0,
        present_flag=True,
        read_write_flag=False,
        user_kernel_flag=True,
        executable_flag=True,
    )
    for offset, byte in enumerate(code_page.get_pte_bytes()):
        ram.write(mm.page_table_pointer + offset, byte)

    instructions = [
        Instruction(0),
        Instruction(0),
    ]
    instructions[0].construct_instruction(Opcode.ADD, 0, 1, 2 << 11)
    instructions[1].construct_instruction(Opcode.HALT, 0, 0, 0)
    for instruction_address, instruction in zip((0x0000, 0x0004), instructions):
        for offset, byte in enumerate(instruction.get_bytes()):
            ram.write(instruction_address + offset, byte)

    cpu = CPU(0)
    # restore process values, done in kernel mode
    cpu.program_counter = proc.saved_program_counter_value
    cpu.registers = proc.saved_register_values.copy()

    cpu.page_table_pointer = proc.memory_descriptor.page_table_pointer

    instruction = cpu.fetch_one_instruction(ram)
    cpu.execute_one_instruction(
        instruction_obj=cpu.decode_one_instruction(instruction)
    )

    assert cpu.registers[0] == 8
    assert cpu.program_counter == 4

    instruction = cpu.fetch_one_instruction(ram)
    cpu.execute_one_instruction(
        instruction_obj=cpu.decode_one_instruction(instruction)
    )
    assert cpu.program_counter == 4
