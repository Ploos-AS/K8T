"""K8T M2.2 syscall and interrupt-service ABI host model."""

from dataclasses import dataclass

K_SYS_INFO=0x00
K_YIELD=0x01
K_SLEEP=0x02
K_OPEN=0x10
K_CLOSE=0x11
K_READ=0x12
K_WRITE=0x13
K_EVENT_WAIT=0x20
K_EVENT_SIGNAL=0x21
K_TASK_SPAWN=0x30
K_TASK_EXIT=0x31
K_CLOCK_GET=0x40
K_IOCTL=0x50

OK=0
EPERM=1
ENOENT=2
EIO=5
EBADF=9
EAGAIN=11
ENOMEM=12
EBUSY=16
EINVAL=22
ENOSYS=38
ETIMEDOUT=110

SYSCALLS={
 K_SYS_INFO:"sys_info", K_YIELD:"yield", K_SLEEP:"sleep",
 K_OPEN:"open", K_CLOSE:"close", K_READ:"read", K_WRITE:"write",
 K_EVENT_WAIT:"event_wait", K_EVENT_SIGNAL:"event_signal",
 K_TASK_SPAWN:"task_spawn", K_TASK_EXIT:"task_exit",
 K_CLOCK_GET:"clock_get", K_IOCTL:"ioctl",
}

@dataclass(frozen=True)
class SysResult:
    carry: bool
    a: int

    @classmethod
    def ok(cls,value=0): return cls(False,value & 0xffff)
    @classmethod
    def error(cls,errno): return cls(True,errno & 0xffff)

class SyscallDispatcher:
    def __init__(self):
        self.handlers={}

    def register(self,number,handler):
        if number not in SYSCALLS:
            raise ValueError("not a defined K8T syscall")
        self.handlers[number]=handler

    def dispatch(self,number,a=0,x=0,y=0):
        if number not in SYSCALLS:
            return SysResult.error(ENOSYS)
        handler=self.handlers.get(number)
        if handler is None:
            return SysResult.error(ENOSYS)
        result=handler(a & 0xffff,x & 0xffff,y & 0xffff)
        if not isinstance(result,SysResult):
            raise TypeError("syscall handler must return SysResult")
        return result

@dataclass(frozen=True)
class ISRResult:
    acknowledged: bool
    work_units: int=0
    wake_tid: int|None=None
    reschedule: bool=False

    def validate(self,max_work_units=64):
        if not self.acknowledged:
            raise ValueError("ISR must acknowledge its source")
        if self.work_units < 0 or self.work_units > max_work_units:
            raise ValueError("ISR work must be bounded")
        if self.reschedule and self.wake_tid is None:
            raise ValueError("reschedule requires a wake target")
        return self

class InterruptRegistry:
    def __init__(self):
        self.handlers={}

    def register(self,source,handler):
        if source in self.handlers:
            raise ValueError("interrupt source already registered")
        self.handlers[source]=handler

    def service(self,source):
        handler=self.handlers.get(source)
        if handler is None:
            raise KeyError(source)
        result=handler()
        if not isinstance(result,ISRResult):
            raise TypeError("ISR must return ISRResult")
        return result.validate()
