import unittest
from src.k8t_machine import *

class M2PlatformTests(unittest.TestCase):
    def test_24_bit_address_wrap(self):
        m=K8TMachine()
        self.assertEqual(m.normalize_address(0x1234567),0x234567)

    def test_native_memory_regions(self):
        m=K8TMachine()
        self.assertEqual(m.region(0x000100),"bank0")
        self.assertEqual(m.region(0x010000),"ram")
        self.assertEqual(m.region(0x800000),"expansion")
        self.assertEqual(m.region(0xE00000),"io")
        self.assertEqual(m.region(0xF00000),"rom")

    def test_reset_then_native_mode(self):
        m=K8TMachine()
        self.assertTrue(m.emulation)
        self.assertFalse(m.native_mode)
        m.enter_native_mode()
        self.assertTrue(m.native_mode)
        self.assertFalse(m.emulation)

    def test_primary_ram_is_directly_addressed(self):
        m=K8TMachine()
        m.write8(0x010000,0x11)
        m.write8(0x020000,0x22)
        self.assertEqual(m.read8(0x010000),0x11)
        self.assertEqual(m.read8(0x020000),0x22)

    def test_rom_is_read_only(self):
        m=K8TMachine()
        m.rom[0]=0x42
        m.write8(ROM_BASE,0x99)
        self.assertEqual(m.read8(ROM_BASE),0x42)

    def test_four_integrated_uart_channels_are_baseline(self):
        m=K8TMachine()
        self.assertEqual(len(m.uart),4)

if __name__=="__main__":
    unittest.main()
