import unittest
from src.m2_4_serial import *

class M24Tests(unittest.TestCase):
    def test_four_independent_ports(self):
        s=SerialSubsystem(); self.assertEqual(len(s.ports),4)
        s.ports[0].receive(b"A")
        self.assertEqual(s.ports[0].read(1),b"A")
        self.assertEqual(len(s.ports[1].rx),0)

    def test_rts_watermarks(self):
        p=SerialPort(1)
        p.receive(bytes([1])*HIGH_WATER)
        self.assertFalse(p.signals.rts)
        p.read(HIGH_WATER-LOW_WATER)
        self.assertTrue(p.signals.rts)

    def test_cts_stops_transmit_queue(self):
        p=SerialPort(1); p.signals.cts=False
        self.assertEqual(p.queue_tx(b"BBS"),0)
        self.assertEqual(len(p.tx),0)

    def test_modem_dcd_drop_is_hangup(self):
        p=SerialPort(1); p.configure("modem",57600)
        p.set_dcd(True); p.set_dcd(False)
        self.assertTrue(p.hangup_pending)

    def test_terminal_dcd_drop_is_not_modem_hangup(self):
        p=SerialPort(1); p.configure("terminal",9600)
        p.set_dcd(True); p.set_dcd(False)
        self.assertFalse(p.hangup_pending)

    def test_overrun_is_local_counter(self):
        p=SerialPort(1)
        self.assertEqual(p.receive(bytes(RING_SIZE+1)),RING_SIZE)
        self.assertEqual(p.overruns,1)

if __name__=="__main__": unittest.main()
