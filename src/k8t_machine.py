"""K8T M1 executable machine model."""

RAM_SIZE = 1 << 20
IO_BASE = 0xE000
IO_END = 0xEFFF
ROM_BASE = 0xF000

BANK_REG_LO = 0xE000
BANK_REG_HI = 0xE001
IRQ_PENDING = 0xE010
IRQ_MASK = 0xE011
TIMER_LO = 0xE020
TIMER_HI = 0xE021
UART_BASE = 0xE100
UART_STRIDE = 0x10
UART_COUNT = 4

class K8TMachine:
    def __init__(self):
        self.ram = bytearray(RAM_SIZE)
        self.rom = bytearray(0x1000)
        self.bank = 0
        self.irq_pending = 0
        self.irq_mask = 0
        self.timer_reload = 0
        self.uart = [bytearray(UART_STRIDE) for _ in range(UART_COUNT)]
        self.reset()

    def reset(self):
        self.a = self.x = self.y = 0
        self.sp = 0xDFFF
        self.pc = 0xF000
        self.flags = 0
        self.supervisor = True

    def _physical_ram(self, addr):
        if 0x8000 <= addr <= 0xBFFF:
            return ((self.bank * 0x4000) + (addr - 0x8000)) % RAM_SIZE
        return addr

    def read8(self, addr):
        addr &= 0xFFFF
        if IO_BASE <= addr <= IO_END:
            return self._io_read(addr)
        if addr >= ROM_BASE:
            return self.rom[addr - ROM_BASE]
        return self.ram[self._physical_ram(addr)]

    def write8(self, addr, value):
        addr &= 0xFFFF
        value &= 0xFF
        if IO_BASE <= addr <= IO_END:
            self._io_write(addr, value)
        elif addr < ROM_BASE:
            self.ram[self._physical_ram(addr)] = value

    def _io_read(self, addr):
        if addr == BANK_REG_LO: return self.bank & 0xFF
        if addr == BANK_REG_HI: return (self.bank >> 8) & 0xFF
        if addr == IRQ_PENDING: return self.irq_pending
        if addr == IRQ_MASK: return self.irq_mask
        if addr == TIMER_LO: return self.timer_reload & 0xFF
        if addr == TIMER_HI: return (self.timer_reload >> 8) & 0xFF
        if UART_BASE <= addr < UART_BASE + UART_COUNT * UART_STRIDE:
            n=(addr-UART_BASE)//UART_STRIDE
            off=(addr-UART_BASE)%UART_STRIDE
            return self.uart[n][off]
        return 0xFF

    def _io_write(self, addr, value):
        if addr == BANK_REG_LO:
            self.bank=(self.bank & 0xFF00)|value
        elif addr == BANK_REG_HI:
            self.bank=((value << 8)|(self.bank & 0xFF)) & 0x3F
        elif addr == IRQ_PENDING:
            self.irq_pending &= ~value
        elif addr == IRQ_MASK:
            self.irq_mask=value
        elif addr == TIMER_LO:
            self.timer_reload=(self.timer_reload & 0xFF00)|value
        elif addr == TIMER_HI:
            self.timer_reload=(value << 8)|(self.timer_reload & 0xFF)
        elif UART_BASE <= addr < UART_BASE + UART_COUNT * UART_STRIDE:
            n=(addr-UART_BASE)//UART_STRIDE
            off=(addr-UART_BASE)%UART_STRIDE
            self.uart[n][off]=value
