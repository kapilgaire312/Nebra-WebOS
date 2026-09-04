import pytest

from os_engine.cpu_architecture.cpu import CPU
from os_engine.memory.memory_request import MemoryRequest
from os_engine.memory.pte import PTE
from os_engine.memory.ram import RAM


def test_memory_request():
    # initialize cpu and ram
    cpu = CPU(10)
    ram = RAM()

    # save the pte at the address in ram
    # create 3 entries
    pte1 = PTE()
    pte2 = PTE()
    pte3 = PTE()

    # initialize the entries values
    pte1.construct_from_bytes(
        byte_1=0x00, byte_2=0x06, byte_3=0x4A
    )  # frame number= 100, flags= 1010-> present,read only, user access

    (
        pte2.construct_from_data_entries(
            physical_frame_number=0x00065,
            present_flag=True,
            read_write_flag=True,
            user_kernel_flag=False,
        ),
    )  # frame number = 101, flags 1100 ->present, read/write, kernel only

    pte3.construct_from_pte_data_block(
        pte_data_block=0x00066E
    )  # fram number = 102, flags= 1110 -> present, read/write, user access

    # put these pte in ram

    pt_pointer = cpu.page_table_pointer

    # for pte1
    bytes_pte1 = pte1.get_pte_bytes()
    print(bytes_pte1)
    print(pte1.pte_data_block)
    for byte in bytes_pte1:
        ram.write(pt_pointer, byte)
        pt_pointer += 1

    # for pte2
    bytes_pte2 = pte2.get_pte_bytes()
    for byte in bytes_pte2:
        ram.write(pt_pointer, byte)
        pt_pointer += 1

    # for pte3
    bytes_pte3 = pte3.get_pte_bytes()
    for byte in bytes_pte3:
        ram.write(pt_pointer, byte)
        pt_pointer += 1

    print(list(ram.ram_bytearray[:20]))
    # test the memory request
    with pytest.raises(Exception, match="Page fault: Only read allowed."):
        # only read allowed
        MemoryRequest.write(
            virtual_address=0x00000002, cpu=cpu, ram=ram, byte_to_write=33
        )  # vitrual page number 0, and offset of 2. pte_1. present,read,user

    # the byte array initializes valuess to 0 when creating RAM
    assert 0 == (MemoryRequest.read(virtual_address=0x00000002, cpu=cpu, ram=ram))

    with pytest.raises(Exception, match="Page fault : Kernel level access required."):
        MemoryRequest.read(
            virtual_address=0x00001002, cpu=cpu, ram=ram
        )  # virtual page no 1 and offset 2. present,write, kernel

    MemoryRequest.write(
        virtual_address=0x00002002, cpu=cpu, ram=ram, byte_to_write=33
    )  # virtaul page no 2, offset 2. present, write, user
    assert MemoryRequest.read(virtual_address=0x00002002, cpu=cpu, ram=ram) == 33
