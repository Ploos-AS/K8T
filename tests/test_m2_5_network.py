import unittest
from src.m2_5_network import *

class M25Tests(unittest.TestCase):
    def test_more_than_eight_tcp_connections(self):
        n=NetworkIngress()
        cs=[n.accept(23) for _ in range(9)]
        self.assertTrue(all(cs)); self.assertEqual(len(n.connections),9)

    def test_design_floor_is_32(self):
        n=NetworkIngress()
        self.assertEqual(MAX_CONNECTIONS,32)
        self.assertTrue(all(n.accept(23) for _ in range(32)))
        self.assertIsNone(n.accept(23))

    def test_telnet_becomes_bbs_node(self):
        n=NetworkIngress(); c=n.accept(23)
        self.assertTrue(n.bbs_node(c))

    def test_services_route_independently(self):
        n=NetworkIngress()
        self.assertEqual(n.accept(24554).service,"binkp")
        self.assertEqual(n.accept(70).service,"gopher")
        self.assertEqual(n.accept(80).service,"http")

    def test_queues_are_bounded(self):
        n=NetworkIngress(); c=n.accept(23)
        self.assertEqual(c.queue_rx(bytes(QUEUE_BYTES+10)),QUEUE_BYTES)
        self.assertEqual(len(c.rx),QUEUE_BYTES)

    def test_closing_network_session_is_local(self):
        n=NetworkIngress(); a=n.accept(23); b=n.accept(23)
        n.close(a.cid)
        self.assertIn(b.cid,n.connections)

if __name__=="__main__": unittest.main()
