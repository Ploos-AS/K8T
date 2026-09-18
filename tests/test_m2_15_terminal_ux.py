import unittest
from src.m2_15_terminal_ux import *
class M215(unittest.TestCase):
 def test_transports(self):
  for t in ("serial","modem","telnet","ssh"): self.assertEqual(Profile(1,t,t,"x").transport,t)
 def test_modem_dials(self):
  c=Connection(Profile(1,"bbs","modem","555",reconnect=1)); c.start(); self.assertEqual(c.state,State.DIALING)
 def test_bounded_reconnect(self):
  c=Connection(Profile(1,"bbs","telnet","x",reconnect=2)); c.start(); c.connected(); c.lost(); self.assertEqual(c.state,State.RECONNECT_WAIT)
  c.retry(); c.lost(); self.assertEqual(c.state,State.RECONNECT_WAIT)
  c.retry(); c.lost(); self.assertEqual(c.state,State.FAILED)
 def test_scrollback_ring_and_search(self):
  s=Scrollback(2); s.add("one"); s.add("BBS hello"); s.add("three")
  self.assertEqual(list(s.lines),["BBS hello","three"]); self.assertEqual(s.search("bbs"),["BBS hello"])
 def test_keymap(self):
  k=KeyMap(); k.bind("F1","ATDT555"); self.assertEqual(k.get("F1"),"ATDT555")
if __name__=="__main__":unittest.main()
