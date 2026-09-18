"""K8T M2.1 scheduler/context ABI model."""

from dataclasses import dataclass

TICK_HZ = 1000
DEFAULT_QUANTUM_TICKS = 10
STACK_BYTES = 512

@dataclass(eq=True)
class TaskContext:
    a: int = 0
    x: int = 0
    y: int = 0
    s: int = 0
    d: int = 0
    pc: int = 0
    dbr: int = 0
    pbr: int = 0
    p: int = 0

    def normalized(self):
        return TaskContext(
            self.a & 0xFFFF, self.x & 0xFFFF, self.y & 0xFFFF,
            self.s & 0xFFFF, self.d & 0xFFFF, self.pc & 0xFFFF,
            self.dbr & 0xFF, self.pbr & 0xFF, self.p & 0xFF,
        )

@dataclass
class Task:
    tid: int
    priority: int
    stack_base: int
    context: TaskContext
    ready: bool = True
    ticks_left: int = DEFAULT_QUANTUM_TICKS

    @property
    def stack_end(self):
        return self.stack_base + STACK_BYTES - 1

class Scheduler:
    def __init__(self):
        self.tasks = []
        self.current = None

    def add(self, task):
        for other in self.tasks:
            if not (task.stack_end < other.stack_base or task.stack_base > other.stack_end):
                raise ValueError("task stacks overlap")
        self.tasks.append(task)

    def choose(self):
        ready = [t for t in self.tasks if t.ready]
        if not ready:
            return None
        best_priority = min(t.priority for t in ready)
        peers = [t for t in ready if t.priority == best_priority]
        if self.current in peers and self.current.ticks_left > 0:
            return self.current
        if self.current in peers:
            i = peers.index(self.current)
            return peers[(i + 1) % len(peers)]
        return peers[0]

    def tick(self):
        if self.current:
            self.current.ticks_left -= 1
        nxt = self.choose()
        if nxt is not self.current:
            if nxt:
                nxt.ticks_left = DEFAULT_QUANTUM_TICKS
            self.current = nxt
        elif self.current and self.current.ticks_left <= 0:
            self.current.ticks_left = DEFAULT_QUANTUM_TICKS
        return self.current

    def wake(self, tid):
        task = next(t for t in self.tasks if t.tid == tid)
        task.ready = True
        if self.current is None or task.priority < self.current.priority:
            self.current = task
            task.ticks_left = DEFAULT_QUANTUM_TICKS
            return True
        return False
