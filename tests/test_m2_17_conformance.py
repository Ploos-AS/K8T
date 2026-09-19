import unittest
from src.m2_13_terminal import Screen, ANSI, PETSCII
from src.m2_17_conformance import CORPUS_VERSION, GoldenCell, cp437_decode, snapshot

class M217(unittest.TestCase):
 def test_version(self): self.assertEqual(CORPUS_VERSION,"terminal-corpus-v1")
 def test_text_crlf(self):
  s=Screen(8,3); a=ANSI(s); a.feed("AB\\r\\nC")
  self.assertEqual(snapshot(s),(GoldenCell(0,0,"A"),GoldenCell(1,0,"B"),GoldenCell(0,1,"C")))
 def test_split_csi_and_cursor(self):
  s=Screen(8,3); a=ANSI(s)
  for chunk in ("\\x1b","[2;","3H","X"): a.feed(chunk)
  self.assertEqual(snapshot(s),(GoldenCell(2,1,"X"),))
 def test_relative_cursor(self):
  s=Screen(8,3); a=ANSI(s); a.feed("A\\x1b[2CB")
  self.assertEqual(snapshot(s),(GoldenCell(0,0,"A"),GoldenCell(3,0,"B")))
 def test_erase_display(self):
  s=Screen(8,3); a=ANSI(s); a.feed("ABC\\x1b[2J")
  self.assertEqual(snapshot(s),()); self.assertEqual((s.x,s.y),(0,0))
 def test_sgr_attributes(self):
  s=Screen(8,3); a=ANSI(s); a.feed("\\x1b[1;31;44mX\\x1b[7mY\\x1b[0mZ")
  self.assertEqual(snapshot(s),(GoldenCell(0,0,"X",1,4,True,False),GoldenCell(1,0,"Y",1,4,True,True),GoldenCell(2,0,"Z")))
 def test_cp437_box(self):
  self.assertEqual("".join(cp437_decode(x) for x in (0xDA,0xC4,0xBF)),"┌─┐")
 def test_petscii_baseline(self):
  self.assertEqual(PETSCII.decode(0x93),("clear",None))
  self.assertEqual(PETSCII.decode(0x41),("char","A"))
if __name__=="__main__": unittest.main()
