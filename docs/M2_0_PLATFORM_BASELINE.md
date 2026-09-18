# M2.0 — W65C265S platform baseline

Status: **IMPLEMENTED**

M2 no longer designs a custom K8T CPU. The platform is built around the commercially available WDC W65C265S.

## CPU contract

- W65C816-compatible 8/16-bit CPU core
- 8-bit external data bus
- 24-bit address space (16 MiB)
- 8 MHz baseline clock
- native-mode operation is the normal K8T-OS target
- emulation mode is retained for boot, diagnostics and compatibility where useful
- K8 and K8T have no ISA/binary-compatibility requirement

K8T software uses the documented W65C816 ISA. There is no K8T-specific instruction set.

## Memory direction

The old M1 64 KiB bank-window model is retired as the M2 architecture. It remains useful only as historical executable-model evidence.

The W65C265S 24-bit address space is the native memory model. M2 reserves broad regions rather than prematurely freezing every decoder bit:

| 24-bit range | Purpose |
|---|---|
| 00:0000–00:FFFF | boot/compatibility bank, vectors and low-memory OS structures |
| 01:0000–7F:FFFF | primary RAM / expansion RAM |
| 80:0000–DF:FFFF | memory-mapped expansion and accelerator windows |
| E0:0000–EF:FFFF | K8T platform I/O and expansion I/O |
| F0:0000–FF:FFFF | ROM/flash, diagnostics and platform-reserved space |

Exact W65C265S internal-register addresses remain those defined by the silicon and are not remapped by this document.

The map is intentionally sparse. Cheap address decoding and future expansion are more valuable than filling every address.

## Hardware philosophy

Minimise programmable logic.

The W65C265S already supplies the CPU, four UARTs, interrupt facilities, timers and watchdog. K8T should not recreate these in an FPGA.

Preferred implementation order:

1. W65C265S native peripherals
2. dedicated commodity controller IC
3. ordinary 74xx/HC/HCT/LVC glue logic
4. small CPLD when it materially reduces BOM/board complexity
5. FPGA only for a subsystem that genuinely benefits from it

An FPGA must never become a hidden replacement CPU.

## OS implications

K8T-OS targets W65C816 native mode. The OS may use 16-bit accumulator/index operation where it improves scheduler, filesystem, TCP/IP and buffer performance. Device payloads remain naturally byte-oriented.

There is no hardware MMU or protected supervisor mode in the W65C816 architecture. M1's provisional `supervisor=True` field is therefore retired. K8T-OS isolation is cooperative/structural, with defensive APIs and memory ownership conventions rather than fictional hardware privilege.

Preemption uses timer interrupts and normal W65C816 interrupt/context-save mechanisms. M2.1 will define the exact task context and scheduler ABI.

## Serial architecture

The four integrated UARTs are the baseline serial channels. External RS-232 transceivers provide physical voltage levels and modem-control interfacing as required.

The software architecture must use ring buffers and hardware flow control. The feasibility model must not be interpreted as permission for expensive per-byte application processing in interrupt context.

## Expansion

Ethernet, storage and video remain external subsystems. They should expose simple memory-mapped or bus interfaces and buffer work so the 8 MHz CPU handles useful blocks/packets rather than bit-level signalling.

## M2.0 acceptance

- commercial CPU replaces custom CPU design: PASS
- native 24-bit memory architecture adopted: PASS
- fictional M1 supervisor/privilege assumption retired: PASS
- four integrated UARTs are platform baseline: PASS
- FPGA is optional rather than foundational: PASS
- M2.1 scheduler/context ABI identified as next step: PASS
