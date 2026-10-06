"""
The MemoryDiscriptor defines the address space of a process.
"""

from dataclasses import dataclass
from enum import Enum, IntEnum, auto


class RegionType(Enum):
    """
    Type of the memory region in the address space.
    """

    CODE = auto()
    STACK = auto()
    HEAP = auto()
    DATA = auto()


class RegionPermission(IntEnum):
    # read, write, execute permissions
    R = 100
    RW = 110
    RX = 101


@dataclass()
class MemoryRegion:
    start: int
    end: int
    permissions: RegionPermission
    type: RegionType


class MemoryDescriptor:
    page_table_pointer: int
    regions: list[MemoryRegion]
