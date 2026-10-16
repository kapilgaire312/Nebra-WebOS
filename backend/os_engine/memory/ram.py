from dataclasses import dataclass, field


@dataclass()
class RAM:
    ram_size: int = 1024 * 1024  # 1 MB ram
    ram_bytearray: bytearray = field(init=False)

    # allocate the bytearray after initialization to create bytearray using the ram_size
    def __post_init__(self):
        self.ram_bytearray = bytearray(self.ram_size)

    def read(self, address):
        # check if address is out of range.
        self._check_address_valid(address)

        return self.ram_bytearray[address]

    def read_instruction(self, address):
        instruction = 0
        for byte_offset in range(4):
            instruction = (instruction << 8) | self.read(address + byte_offset)
        return instruction

    def write(self, address, byte):
        self._check_address_valid(address)

        # check if the value is a valid byte
        self._check_byte_valid(byte)

        self.ram_bytearray[address] = byte

    def _check_address_valid(self, address):
        if address < 0 or address > self.ram_size - 1:
            # raise custom exception later
            raise Exception("Address out of range.")

    def _check_byte_valid(self, byte):
        if byte < 0 or byte > 255:
            # raise custom exception later
            raise Exception("Byte is not valid.")
