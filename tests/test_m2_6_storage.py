import unittest
from src.m2_6_storage import *

class M26Tests(unittest.TestCase):
    def test_block_size_and_rounding(self):
        self.assertEqual(BLOCK_SIZE,512)
        self.assertEqual(blocks_for(513),2)

    def test_committed_data_survives_recovery(self):
        s=PersistenceStore(); s.commit("users/1",b"sysop")
        s.data.clear(); s.recover()
        self.assertEqual(s.data["users/1"],b"sysop")

    def test_incomplete_transaction_is_discarded(self):
        s=PersistenceStore(); s.commit("messages/1",b"hello")
        s.inject_incomplete("messages/2",b"partial")
        s.recover()
        self.assertIn("messages/1",s.data)
        self.assertNotIn("messages/2",s.data)

    def test_full_storage_rejects_without_corrupting_committed_data(self):
        s=PersistenceStore(capacity_records=3); s.commit("a",b"ok")
        with self.assertRaises(OSError): s.commit("b",b"no")
        s.recover(); self.assertEqual(s.data,{"a":b"ok"})

    def test_snapshot_generation_is_consistent(self):
        s=PersistenceStore(); s.commit("users/1",b"a")
        snap=s.snapshot_manifest()
        s.commit("messages/1",b"b")
        self.assertEqual(snap["generation"],1)
        self.assertEqual(snap["keys"],("users/1",))

if __name__=="__main__": unittest.main()
