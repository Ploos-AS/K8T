import unittest
from src.m2_12_fidonet import *
class M212(unittest.TestCase):
 def test_address(self): self.assertEqual(str(FidoAddress(2,5020,1200,1)),"2:5020/1200.1")
 def test_dupe(self):
  d=DupeIndex(); self.assertTrue(d.accept("x")); self.assertFalse(d.accept("x"))
 def test_link_area_acl(self):
  l=Link(FidoAddress(2,1,1),{"K8T.TEST"}); self.assertTrue(l.permits("K8T.TEST")); self.assertFalse(l.permits("SECRET"))
 def test_routing(self):
  a=FidoAddress(2,5020,1); r=Router({(2,5020):"hub",(2,None):"zone"})
  self.assertEqual(r.next_hop(a),"hub"); self.assertEqual(r.next_hop(FidoAddress(2,999,1)),"zone")
if __name__=="__main__":unittest.main()
