import unittest
from src.m2_3_bus import *

class M23Tests(unittest.TestCase):
    def test_map_has_no_overlaps(self): self.assertTrue(validate_map())
    def test_standard_memory_sizes(self):
        self.assertEqual(STANDARD_SRAM_BYTES,2*1024*1024)
        self.assertEqual(MAX_ONBOARD_SRAM_BYTES,4*1024*1024)
        self.assertEqual(FLASH_BYTES,512*1024)
    def test_bbs_controller_apertures(self):
        self.assertEqual(decode(0x800000),"video")
        self.assertEqual(decode(0x900000),"ethernet")
        self.assertEqual(decode(0xA00000),"storage")
    def test_flash_at_top_of_address_space(self):
        self.assertEqual(decode(0xFFFFFF),"flash")
        self.assertEqual(FLASH_END-FLASH_BASE+1,FLASH_BYTES)
    def test_unassigned_space_is_open_bus(self):
        self.assertEqual(decode(0x500000),"open_bus")
    def test_24bit_wrap(self):
        self.assertEqual(decode(0x1900000),"ethernet")

if __name__=="__main__": unittest.main()
