import unittest
from src.m2_1_scheduler import *

class M21Tests(unittest.TestCase):
    def test_context_round_trip_normalization(self):
        c=TaskContext(a=0x12345,x=2,y=3,s=0x4567,d=0x89ab,pc=0xcdef,dbr=0x123,pbr=0x45,p=0x1ff)
        n=c.normalized()
        self.assertEqual(n.a,0x2345)
        self.assertEqual(n.s,0x4567)
        self.assertEqual(n.dbr,0x23)
        self.assertEqual(n.p,0xff)

    def test_stack_overlap_rejected(self):
        s=Scheduler()
        s.add(Task(1,1,0x2000,TaskContext()))
        with self.assertRaises(ValueError):
            s.add(Task(2,1,0x2100,TaskContext()))

    def test_equal_priority_round_robin(self):
        s=Scheduler()
        a=Task(1,1,0x2000,TaskContext(),ticks_left=0)
        b=Task(2,1,0x2400,TaskContext())
        s.add(a); s.add(b); s.current=a
        self.assertIs(s.tick(),b)

    def test_higher_priority_wakeup_preempts(self):
        s=Scheduler()
        low=Task(1,5,0x2000,TaskContext())
        high=Task(2,1,0x2400,TaskContext(),ready=False)
        s.add(low); s.add(high); s.current=low
        self.assertTrue(s.wake(2))
        self.assertIs(s.current,high)

    def test_scheduler_constants(self):
        self.assertEqual(TICK_HZ,1000)
        self.assertEqual(DEFAULT_QUANTUM_TICKS,10)

if __name__=="__main__":
    unittest.main()
