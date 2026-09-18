"""K8T M2.0 platform model for the W65C265S baseline.

This is a platform/address-space oracle, not a CPU emulator.  Instruction
semantics belong to the documented W65C816-compatible processor.
"""

ADDRESS_MASK = 0xFFFFFF
ADDRESS_SPACE = 1 << 24
CPU_HZ = 8_000_000

BANK0_END = 0x00FFFF
RAM_BASE = 0x010000
RAM_END = 0x7FFFFF
EXPANSION_BASE = 0x800000
EXPANSION_END = 0xDFFFFF
PLATFORM_IO_BASE = 0xE00000
PLATFORM_IO_END = 0xEFFFFF
ROM_BASE = 0xF00000
ROM_END = 0xFFFFFF
UART_COUNT = 4

class K8TMachine:
    """Minimal M2 platform state; not a W65C816 instruction emulator."""

    def __init__(self, ram_size=1 << 20, rom_size=1 << 20):
        if ram_size < 0 or ram_size > (RAM_END - RAM_BASE + 1):
            raise ValueError("RAM size outside M2 primary RAM window")
        if rom_size < 0 or rom_size > (ROM_END - ROM_BASE + 1):
            raise ValueError("ROM size outside M2 ROM window")
        self.bank0 = bytearray(1 << 16)
        self.ram = bytearray(ram_size)
        self.rom = bytearray(rom_size)
        self.platform_io = {}
        self.uart = [bytearray() for _ in range(UART_COUNT)]
        self.reset()

    def reset(self):
        # Architectural reset starts in W65C816 emulation mode.
        self.emulation = True
        self.native_mode = False

    @staticmethod
    def normalize_address(addr):
        return addr & ADDRESS_MASK

    def region(self, addr):
        addr = self.normalize_address(addr)
        if addr <= BANK0_END: return "bank0"
        if RAM_BASE <= addr <= RAM_END: return "ram"
        if EXPANSION_BASE <= addr <= EXPANSION_END: return "expansion"
        if PLATFORM_IO_BASE <= addr <= PLATFORM_IO_END: return "io"
        return "rom"

    def enter_native_mode(self):
        self.emulation = False
        self.native_mode = True

    def read8(self, addr):
        addr = self.normalize_address(addr)
        region = self.region(addr)
        if region == "bank0":
            return self.bank0[addr]
        if region == "ram":
            off = addr - RAM_BASE
            return self.ram[off] if off < len(self.ram) else 0xFF
        if region == "io":
            return self.platform_io.get(addr, 0xFF)
        if region == "rom":
            off = addr - ROM_BASE
            return self.rom[off] if off < len(self.rom) else 0xFF
        return 0xFF

    def write8(self, addr, value):
        addr = self.normalize_address(addr)
        value &= 0xFF
        region = self.region(addr)
        if region == "bank0":
            self.bank0[addr] = value
        elif region == "ram":
            off = addr - RAM_BASE
            if off < len(self.ram):
                self.ram[off] = value
        elif region == "io":
            self.platform_io[addr] = value
        # expansion is device-owned and ROM is read-only in this oracle.
