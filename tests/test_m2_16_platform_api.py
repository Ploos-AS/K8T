import unittest
from src.m2_16_platform_api import *
class M216(unittest.TestCase):
 def test_k8t_network(self):
  p=Platform("k8t",frontend_contract("k8t")); self.assertEqual(p.open_stream("ssh"),"ssh")
 def test_atari_serial_without_network(self):
  p=Platform("st",frontend_contract("atari-st")); self.assertEqual(p.open_stream("serial"),"serial")
  with self.assertRaises(ValueError): p.open_stream("telnet")
 def test_amiga_capabilities(self):
  c=frontend_contract("amiga"); self.assertTrue(c.mouse); self.assertTrue(c.network)
 def test_degrade_optional(self):
  p=Platform("minimal"); self.assertFalse(p.supports("clipboard")); self.assertEqual(p.open_stream("modem"),"modem")
if __name__=="__main__":unittest.main()
