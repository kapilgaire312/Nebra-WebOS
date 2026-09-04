"""
Abstraction layer used to simulate hardware combinations which CPU uses to
read/write from/to the memory.
After the request is made, the MMU hardware translates the virtual addrtess to physical,
then memory controller feteches the data and puts it in data bus.
which is then retrieved by CPU and loaded into regiser.

Here, however we are not yet implementing data or addrtess bus. so we need to call methods directly and return data.
"""

from os_engine.cpu_architecture.cpu import CPU
from os_engine.memory.mmu import MMU
from os_engine.memory.ram import RAM


class MemoryRequest:
    @staticmethod
    def read(virtual_address: int, cpu: CPU, ram: RAM):
        # first get the physical memory address from the virtual_address

        physical_address = MMU.translate(
            virtual_address=virtual_address, cpu=cpu, ram=ram, write_access=False
        )

        # fetch the byte from the RAM contained in that physical address.
        byte_read = ram.read(physical_address)

        return byte_read

    @staticmethod
    def write(
        virtual_address: int,
        cpu: CPU,
        ram: RAM,
        byte_to_write: int,
    ):
        # get the physical memory address from the virtual_address

        physical_address = MMU.translate(
            virtual_address=virtual_address, cpu=cpu, ram=ram, write_access=True
        )

        # store the byte to the ram physical address
        ram.write(address=physical_address, byte=byte_to_write)
