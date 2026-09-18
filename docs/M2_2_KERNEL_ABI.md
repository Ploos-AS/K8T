# M2.2 — Kernel trap, syscall and interrupt-service ABI

Status: **IMPLEMENTED / HOST-QUALIFIED**

## Goals

M2.2 freezes the first stable application-to-kernel calling convention and the driver interrupt-service contract. It uses real W65C816 mechanisms rather than inventing privilege hardware that the W65C265S does not have.

## Kernel entry

- **COP** is the normal K8T-OS system-call instruction.
- **BRK** is reserved for debugger/breakpoint and fatal diagnostic use.
- hardware IRQ/NMI paths remain device/reliability entry paths and are not application syscalls.
- syscall callers must be in native mode with 16-bit A/X/Y ABI width on entry.

COP's signature byte is the syscall number. This gives a compact, readable call site and leaves BRK available for development/debugging.

## Register ABI

On syscall entry:

| Register | Meaning |
|---|---|
| A | primary scalar argument / result |
| X | secondary scalar argument |
| Y | tertiary scalar argument |
| DBR | data bank for caller buffers unless an explicit 24-bit pointer structure is used |
| P | status; carry reports success/failure on return |

Return convention:

- Carry clear: success; A contains result/value where applicable.
- Carry set: failure; A contains a stable K8T errno value.
- X/Y are preserved unless the syscall documentation explicitly declares output values.
- D, S, DBR and PBR are preserved by the kernel boundary.

## Initial syscall namespace

The namespace is deliberately small and capability-oriented:

- 0x00 K_SYS_INFO
- 0x01 K_YIELD
- 0x02 K_SLEEP
- 0x10 K_OPEN
- 0x11 K_CLOSE
- 0x12 K_READ
- 0x13 K_WRITE
- 0x20 K_EVENT_WAIT
- 0x21 K_EVENT_SIGNAL
- 0x30 K_TASK_SPAWN
- 0x31 K_TASK_EXIT
- 0x40 K_CLOCK_GET
- 0x50 K_IOCTL

Unassigned values return ENOSYS. Network, terminal, serial and filesystem APIs should primarily compose these generic handle/read/write/event/ioctl primitives instead of consuming hundreds of CPU trap numbers.

## Errors

Initial stable errno values:

- 0 OK
- 1 EPERM
- 2 ENOENT
- 5 EIO
- 9 EBADF
- 11 EAGAIN
- 12 ENOMEM
- 16 EBUSY
- 22 EINVAL
- 38 ENOSYS
- 110 ETIMEDOUT

## Interrupt-service ABI

An ISR must:

1. identify/acknowledge the source;
2. perform only bounded device work;
3. transfer data/status to a ring, packet, block or event structure;
4. wake an appropriate service task if necessary;
5. request reschedule when a higher-priority task became ready;
6. return through the common context epilogue.

An ISR must not parse BBS messages, run TCP protocol state for arbitrary duration, modify filesystem structures beyond bounded queue completion, allocate unbounded memory or busy-wait on a device.

## Driver contract

Drivers expose handles/events to normal tasks. The kernel owns interrupt registration and validates one handler per source. Handlers return a small result containing acknowledged/work/wake/reschedule state; they do not directly switch stacks.

## M2.2 acceptance

- COP syscall namespace defined: PASS
- BRK retained for debugger/diagnostics: PASS
- register/error ABI defined: PASS
- generic handle I/O primitives defined: PASS
- bounded ISR rules defined: PASS
- interrupt wakeup/reschedule handoff defined: PASS
- host model/tests cover dispatch, ENOSYS, errors and ISR bounds: PASS

Instruction-level COP/IRQ frame verification on a W65C265S runtime remains a later hardware/runtime qualification.
