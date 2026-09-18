# M1.6 — W65C265S feasibility qualification

Status: **ANALYTICAL PASS; HARDWARE QUALIFICATION REQUIRED BEFORE RELEASE**

## Question

Can an 8 MHz W65C265S plausibly run the communications/BBS machine without making an FPGA the real computer?

WDC specifies the W65C265S as a fully-static W65C816-compatible 8/16-bit MCU with an 8-bit external data bus, 24-bit address bus / 16 MiB address space, four UARTs, 29 priority-encoded interrupts, eight 16-bit timers/counters and watchdog. Those integrated peripherals are the key reason the 8 MHz clock is more viable than it first appears.

## Method

M1.6 adds `src/m1_6_w65c265s_feasibility.py`. It is deliberately an analytical cycle-budget model rather than pretending to be a cycle-accurate benchmark before hardware exists.

Reference stress case:

- 4 UARTs simultaneously receiving 115200 baud, 8N1
- UART service in 16-byte bursts
- 1 kHz scheduler tick
- 1000 Ethernet packet-service events/s
- 250 storage completion events/s
- 500 ANSI/text-render batches/s
- 1000 BBS/protocol work units/s

The cycle cost assigned to every event is explicit in the source and can later be replaced by measured assembly routines.

## Result

At 8 MHz the reference model consumes:

- UART service: 748,800 cycles/s
- scheduler: 220,000 cycles/s
- Ethernet: 650,000 cycles/s
- storage: 125,000 cycles/s
- ANSI/text: 275,000 cycles/s
- BBS/protocol work: 900,000 cycles/s
- total: **2,918,800 cycles/s**
- utilization: **36.5%**
- unallocated headroom: **63.5%**

The CI gate requires at least 25% analytical headroom.

## Interpretation

**PASS for architecture selection.**

This does not prove that final K8T software will consume exactly these cycle counts. It proves that the W65C265S is not obviously underpowered under a conservative, FIFO/buffer-oriented architecture: the model can more than double its assumed aggregate CPU work before reaching saturation.

The design must therefore avoid per-byte interrupt handling. UARTs are serviced in bursts/ring buffers; Ethernet and storage must be buffered and should interrupt on useful units of work rather than byte-level activity.

No FPGA is required for CPU, UARTs, interrupt controller, timers or watchdog. Small programmable logic remains optional for address/glue logic or later acceleration, not as a hidden replacement CPU.

## Remaining risks

- The integrated W65C265S UARTs do not magically provide deep modern FIFOs; the final serial buffering/handshake design must be verified from the device behavior and on hardware.
- Ethernet controller choice can radically change CPU load.
- TCP/IP and filesystem implementation costs are not cycle-accurately represented yet.
- Real compiler-generated code may be materially slower than tuned 65C816 assembly for hot paths.
- Full-duplex TX adds work, although transmit can be queue/buffer driven.
- Hardware qualification at the selected clock is mandatory.

## Decision

W65C265S becomes the **baseline CPU for M2** subject to later physical qualification.

M2 should use the native 24-bit address space instead of preserving the provisional M1 64 KiB banking model merely for historical reasons. The M1 executable model is an architecture prototype and should now be revised around the selected processor rather than treated as silicon truth.

A development board such as W65C265SXB can be used for early software/runtime measurements before the custom motherboard is manufactured.
