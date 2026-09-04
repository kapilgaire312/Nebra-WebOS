"""
Page table entry- how the page table is stored in the ram.

for 32 bit address registers:
20 bit-> virtual page number => converted to 20 bit physical page number
12 bit -> offset => added to above physical page to get final physical address.

PTE is the data structure which represents mapping from virtual page to physical page.
It has the mapping as wel as flags to enforce rules.

total bytes: 3 bytes -> 24 bits
20 bits -> physical page number.
1 bit -> Present flag: if the virtual page is mapped to a physical frame of RAM. 1 if loaded, 0 if not mapper.
1 bit -> Read/write flag : if the frame is read only => 0 , if read and write allowed => 1
1 bit -> user/ kernel flag : if accessible to user => 1 , only kernel => 0
1 bit -> executable flag: if it is executable->1, else 0


"""

from dataclasses import dataclass
from sys import executable


@dataclass()
class PTE:
    pte_data_block: int | None = None
    physical_frame_number: int | None = None
    present_flag: bool | None = None
    read_write_flag: bool | None = None
    user_kernel_flag: bool | None = None
    executable_flag: bool | None = None

    def _initialize_entries_from_block(self, pte_data_block):
        """
        protected method to initialize entries of block.
        """
        flag_bits = (
            pte_data_block & 0xF
        )  # masking with 1111, so only the last 4 bits are preserved

        self.pte_data_block = pte_data_block
        self.physical_frame_number = pte_data_block >> 4

        self.present_flag = bool(flag_bits >> 3)
        self.read_write_flag = bool((flag_bits >> 2) & 1)
        self.user_kernel_flag = bool((flag_bits >> 1) & 1)
        self.executable_flag = bool(flag_bits & 1)

    def construct_from_bytes(self, byte_1: int, byte_2: int, byte_3: int) -> None:
        pte_data_block = (
            (byte_1 << 16) | (byte_2 << 8) | byte_3
        )  # left shift and combine with bitwise OR

        self._initialize_entries_from_block(pte_data_block)

    def construct_from_pte_data_block(self, pte_data_block):
        self._initialize_entries_from_block(pte_data_block)

    def construct_from_data_entries(
        self,
        physical_frame_number: int,
        present_flag: bool,
        read_write_flag: bool,
        user_kernel_flag: bool,
        executable_flag:bool
    ):
        present_flag_bit: int = 1 if present_flag else 0

        read_write_flag_bit: int = 1 if read_write_flag else 0

        user_kernel_flag_bit: int = 1 if user_kernel_flag else 0

        executable_flag_bit :int = 1 if executable_flag else 0

        pte_data_block = physical_frame_number << 4
        pte_data_block |= present_flag_bit << 3
        pte_data_block |= read_write_flag_bit << 2
        pte_data_block |= user_kernel_flag_bit << 1
        pte_data_block |= executable_flag_bit

        self._initialize_entries_from_block(pte_data_block)

    def get_pte_bytes(self) -> list[int]:
        if self.pte_data_block:
            byte_1: int = (self.pte_data_block >> 16) & 0xFF
            byte_2: int = (self.pte_data_block >> 8) & 0xFF
            byte_3: int = self.pte_data_block & 0xFF

            return [byte_1, byte_2, byte_3]

        else:
            raise Exception("PTE block values are not initialized.")
