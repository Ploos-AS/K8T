import unittest
from src.m2_2_kernel_abi import *

class M22Tests(unittest.TestCase):
    def test_unknown_syscall_is_enosys(self):
        r=SyscallDispatcher().dispatch(0xff)
        self.assertTrue(r.carry); self.assertEqual(r.a,ENOSYS)

    def test_syscall_success_and_16bit_arguments(self):
        d=SyscallDispatcher()
        d.register(K_WRITE,lambda a,x,y: SysResult.ok(a+x+y))
        r=d.dispatch(K_WRITE,0x10001,2,3)
        self.assertFalse(r.carry); self.assertEqual(r.a,6)

    def test_error_uses_carry_and_errno(self):
        d=SyscallDispatcher()
        d.register(K_OPEN,lambda a,x,y: SysResult.error(ENOENT))
        r=d.dispatch(K_OPEN)
        self.assertTrue(r.carry); self.assertEqual(r.a,ENOENT)

    def test_duplicate_interrupt_registration_rejected(self):
        ir=InterruptRegistry(); ir.register("uart1_rx",lambda:ISRResult(True))
        with self.assertRaises(ValueError):
            ir.register("uart1_rx",lambda:ISRResult(True))

    def test_bounded_isr_can_request_preemption(self):
        ir=InterruptRegistry()
        ir.register("uart1_rx",lambda:ISRResult(True,16,7,True))
        r=ir.service("uart1_rx")
        self.assertEqual(r.wake_tid,7); self.assertTrue(r.reschedule)

    def test_unbounded_isr_rejected(self):
        ir=InterruptRegistry()
        ir.register("bad",lambda:ISRResult(True,1000))
        with self.assertRaises(ValueError):
            ir.service("bad")

if __name__=="__main__":
    unittest.main()
