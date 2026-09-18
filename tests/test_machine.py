import unittest
from src.k8t_machine import *

class M1Tests(unittest.TestCase):
    def test_reset_state(self):
        m=K8TMachine()
        self.assertEqual(m.pc,0xF000)
        self.assertEqual(m.sp,0xDFFF)
        self.assertTrue(m.supervisor)

    def test_rom_is_read_only(self):
        m=K8TMachine(); m.rom[0]=0x42
        m.write8(0xF000,0x99)
        self.assertEqual(m.read8(0xF000),0x42)

    def test_banked_window(self):
        m=K8TMachine()
        m.write8(BANK_REG_LO,1); m.write8(0x8000,0x11)
        m.write8(BANK_REG_LO,2); m.write8(0x8000,0x22)
        m.write8(BANK_REG_LO,1); self.assertEqual(m.read8(0x8000),0x11)
        m.write8(BANK_REG_LO,2); self.assertEqual(m.read8(0x8000),0x22)

    def test_irq_write_one_to_clear(self):
        m=K8TMachine(); m.irq_pending=0b1111
        m.write8(IRQ_PENDING,0b0101)
        self.assertEqual(m.irq_pending,0b1010)

    def test_four_uart_windows(self):
        m=K8TMachine()
        for n in range(4):
            a=UART_BASE+n*UART_STRIDE
            m.write8(a,n+1)
            self.assertEqual(m.read8(a),n+1)

if __name__=="__main__":
    unittest.main()
