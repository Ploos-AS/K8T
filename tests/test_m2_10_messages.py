import unittest
from src.m2_10_messages import *

class M210Tests(unittest.TestCase):
    def test_32bit_ids_beyond_16bit(self):
        a=MessageArea(70000,"Big")
        m=Message(100000,70000,1,"Hi","Body",1); a.add(m)
        self.assertEqual(a.page()[0].mid,100000)

    def test_paging(self):
        a=MessageArea(1,"General")
        for i in range(1,150): a.add(Message(i,1,1,str(i),"x",i))
        self.assertEqual(len(a.page(0)),PAGE_SIZE)
        self.assertEqual(a.page(PAGE_SIZE)[0].mid,PAGE_SIZE+1)

    def test_thread_root(self):
        a=MessageArea(1,"General"); a.add(Message(1,1,1,"Topic","x",1))
        r=a.reply(1,2,2,"reply",2); rr=a.reply(2,3,3,"reply2",3)
        self.assertEqual(r.thread_root,1); self.assertEqual(rr.thread_root,1)

    def test_last_read_per_user_area(self):
        l=LastRead(); l.set(7,99,123456)
        self.assertEqual(l.get(7,99),123456); self.assertEqual(l.get(8,99),0)

    def test_bounded_editor_lines_and_quote(self):
        d=Draft(max_line=20); d.quote("hello\nworld")
        self.assertEqual(d.body(),"> hello\n> world")
        with self.assertRaises(ValueError): d.append("x"*21)

if __name__=="__main__": unittest.main()
