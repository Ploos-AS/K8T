import unittest
from src.m2_7_bbs import *

class M27Tests(unittest.TestCase):
    def test_four_serial_nodes_reserved(self):
        b=BBSCore()
        self.assertEqual([b.nodes[i].transport for i in range(1,5)],["serial"]*4)

    def test_network_nodes_are_dynamic(self):
        b=BBSCore(); a=b.new_network_node(); c=b.new_network_node()
        self.assertNotEqual(a.nid,c.nid); self.assertEqual(a.transport,"telnet")

    def test_default_deny(self):
        self.assertFalse(allowed(User(1,"pgo"),Area(1,"General"),"read"))

    def test_group_allow(self):
        a=Area(1,"General",[ACLRule("User","read",True)])
        self.assertTrue(allowed(User(1,"pgo"),a,"read"))

    def test_explicit_deny_wins(self):
        a=Area(1,"Private",[ACLRule("User","read",True),ACLRule("user:7","read",False)])
        self.assertFalse(allowed(User(7,"x"),a,"read"))

    def test_disconnect_is_session_local(self):
        b=BBSCore(); n1=b.new_network_node(); n2=b.new_network_node()
        b.connect(n1.nid); s2=b.connect(n2.nid)
        b.disconnect(n1.nid)
        self.assertIn(s2.sid,b.sessions); self.assertEqual(n2.state,"connected")

    def test_area_publication_surfaces(self):
        a=Area(1,"Public",surfaces={"bbs","gopher","rss"})
        self.assertIn("gopher",a.surfaces); self.assertNotIn("fidonet",a.surfaces)

if __name__=="__main__": unittest.main()
