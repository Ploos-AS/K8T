import unittest
from src.m2_11_files import *
class M211Tests(unittest.TestCase):
 def test_large_ids_and_paging(self):
  a=FileArea(70000,"Files")
  for i in range(1,130): a.publish(FileRecord(100000+i,70000,str(i),i,"x",1))
  self.assertEqual(len(a.page()),PAGE_SIZE); self.assertGreater(a.page(64)[0].fid,65535)
 def test_transfer_completion(self):
  j=TransferJob(1,9,"download","zmodem",100); j.start(); j.advance(40); j.advance(60)
  self.assertEqual(j.state,TransferState.COMPLETE)
 def test_disconnect_is_session_local(self):
  q=TransferQueue(); a=TransferJob(1,1,"download","zmodem",10); b=TransferJob(2,2,"download","xmodem",10)
  a.start(); b.start(); q.add(a); q.add(b); q.disconnect(1)
  self.assertEqual(a.state,TransferState.CANCELLED); self.assertEqual(b.state,TransferState.ACTIVE)
 def test_upload_not_visible_before_validation(self):
  u=UploadStage()
  with self.assertRaises(RuntimeError): u.publish()
  u.validate(True); u.publish(); self.assertTrue(u.published)
 def test_bad_upload_policy(self):
  u=UploadStage()
  with self.assertRaises(ValueError): u.validate(False)
if __name__=="__main__": unittest.main()
