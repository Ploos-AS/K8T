import unittest
from src.m2_14_terminal_compat import *
class M214(unittest.TestCase):
 def test_all_required_transfers(self):
  r=TransferRegistry()
  for p in ("xmodem","xmodem-crc","xmodem-1k","ymodem","zmodem","kermit"): self.assertTrue(r.supports(p))
 def test_profile_input(self):
  self.assertEqual(InputEncoder("ansi").key("UP"),b"\x1b[A")
  self.assertEqual(InputEncoder("petscii").key("UP"),bytes([0x91]))
 def test_incremental_utf8(self):
  d=UTF8Decoder(); euro="€".encode()
  self.assertEqual(d.feed(euro[:2]),""); self.assertEqual(d.feed(euro[2:]),"€")
 def test_transfer_bounded_state(self):
  t=Transfer("kermit",100); t.progress(20); t.retry(); self.assertEqual((t.done,t.retries),(20,1)); t.cancel(); self.assertTrue(t.cancelled)
 def test_unknown_protocol(self):
  with self.assertRaises(ValueError): Transfer("nope")
if __name__=="__main__":unittest.main()
