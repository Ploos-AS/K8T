import unittest
from src.m2_13_terminal import *
class M213(unittest.TestCase):
 def test_geometry(self): self.assertEqual((Screen(40,25).w,Screen(40,25).h),(40,25))
 def test_incremental_escape(self):
  s=Screen(); p=ANSI(s); p.feed("Hi\x1b["); p.feed("2;5H"); p.feed("X")
  self.assertEqual(s.cells[1][4].ch,"X")
 def test_cursor(self):
  s=Screen(); p=ANSI(s); p.feed("\x1b[10;20H"); self.assertEqual((s.x,s.y),(19,9))
 def test_clear(self):
  s=Screen(); p=ANSI(s); p.feed("x\x1b[2J"); self.assertEqual(s.cells[0][0].ch," ")
 def test_unknown_sequence_recovers(self):
  s=Screen(); p=ANSI(s); p.feed("\x1b[999zOK"); self.assertEqual(s.cells[0][0].ch,"O")
 def test_petscii_is_profile(self):
  self.assertEqual(PETSCII.decode(0x93)[0],"clear"); self.assertEqual(PETSCII.decode(0x41),("char","A"))
if __name__=="__main__":unittest.main()
