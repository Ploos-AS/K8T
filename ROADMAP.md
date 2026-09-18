# K8T Roadmap

## M0 — Architecture foundation
Status: **DONE**

- product identity and design principles
- 8-bit CPU, 64 KiB logical address space and banked RAM
- four-port RS-232 subsystem
- Ethernet, SSD/SD, video, keyboard and mouse
- interrupts, DMA and watchdog direction
- preemptive K8T-OS
- shared BBS users/messages/files
- central ACL/publication policy
- Telnet, Gopher, HTTP, IRC, RSS, Atom and FidoNet/BinkP
- concurrency acceptance target

## M1 — Executable machine model
Status: **DONE**

- freeze M1 register map
- CPU programmer-visible state and reset/vector behaviour
- bank and interrupt controller registers
- UART and timer/RTC contracts
- host-side executable machine skeleton
- deterministic register/memory-map tests
- CI checks

## M1.5 — CPU market survey
Status: **DONE — W65C265S selected after M1.6 analytical qualification**

- prefer a currently produced physical CPU over a custom FPGA CPU
- minimize FPGA use
- preserve educational and maker-friendly architecture
- pure 8-bit operation is not a requirement; total system cost matters
- W65C265S selected as baseline: 8/16-bit core, 24-bit external addressing, four UARTs, timers, interrupts and watchdog integrated
- W65C02S retained as survey reference, not baseline

See [docs/M1_5_CPU_SURVEY.md](docs/M1_5_CPU_SURVEY.md).

## M1.6 — W65C265S feasibility
Status: **ANALYTICAL PASS**

Cycle-budget qualification covers four 115200-bit/s UART streams, interrupt/preemption load, Ethernet, storage, ANSI rendering and BBS activity. Reference model uses 36.5% of an 8 MHz CPU budget, leaving 63.5% analytical headroom. Physical hardware qualification remains mandatory.

See [docs/M1_6_W65C265S_FEASIBILITY.md](docs/M1_6_W65C265S_FEASIBILITY.md).

## M2 — K8T CPU and memory subsystem
Status: **IN PROGRESS — M2.0–M2.7 DONE**

M2.0 freezes the W65C265S platform baseline, native 24-bit memory direction, real privilege model and minimum-FPGA hardware policy. M2.1 freezes the native-mode task context, private stacks, 1 kHz tick, 10 ms default quantum and priority/round-robin scheduler ABI. M2.2 freezes COP-based syscalls, error/register conventions and the bounded interrupt-service ABI. M2.3 freezes the BBS-first external bus direction: 2 MiB standard SRAM, 4 MiB onboard path, 512 KiB recovery flash, buffered controller apertures and cost/reliability-driven decode logic. M2.4 freezes four physical DTE DE-9 BBS/modem ports, one per integrated UART, with RTS/CTS, modem-control semantics and 1 KiB RX/TX rings. M2.5 freezes packet-level 10/100 Ethernet, an OS-owned TCP/IP stack and a 32-connection design floor so BBS networking is not constrained by hardware socket count. M2.6 freezes SSD/SD/flash roles, asynchronous block I/O, BBS durability classes, atomic intent/data/commit persistence and online snapshot semantics. M2.7 freezes one canonical BBS core across serial/Telnet, dynamic sessions, built-in groups, default-deny ACLs and canonical message/file objects with per-area publication surfaces. Next: M2.8 authentication, login flow and sysop/user management.

Integrate and freeze the W65C265S-based CPU/memory architecture. K8 compatibility is explicitly not a goal and K8 is not changed.

- educational and maker-friendly W65C265S architecture
- 8/16-bit W65C816-compatible CPU with 8-bit external data bus and 24-bit addressing
- readable 65C816 assembler/toolchain documentation
- minimize FPGA; use ordinary logic or small CPLD only where justified
- expose the external bus and memory/peripheral architecture clearly
- banking, privilege/traps and efficient context switching
- vectored/prioritised interrupt support suitable for four UARTs plus Ethernet/storage
- timer-driven preemption
- architecture documentation sufficient to explain and eventually build the CPU

## M3 — Console and ANSI terminal
Text video, keyboard/mouse, virtual consoles, ANSI renderer, scrollback/copy-paste and serial terminal sessions.

## M4 — Storage
Block protocol, SD, SSD, 64-bit LBA, K8TFS prototype, recovery and snapshots.

## M5 — Networking
Ethernet, ARP/IPv4/ICMP, UDP/TCP/DNS, sockets, Telnet and stress tests.

## M6 — BBS core
Users/authentication, security groups, message/file areas, ACL/publication policy, multi-node sessions and sysop console.

## M7 — Internet/classic services
Gopher, HTTP, RSS, Atom, IRC client/gateway and configurable per-service exposure.

## M8 — FidoNet
Addresses, netmail, echomail, packets/bundles, TIC/file echoes, nodelists, BinkP and dial-up RS-232 transport.

## M9 — Hardware prototype
Physical RS-232 x4, Ethernet, SSD/SD, video, keyboard/mouse, watchdog/RTC and concurrency qualification.

## M10 — Release qualification
Four active serial links plus multiple TCP sessions, BBS, Gopher/HTTP, FidoNet/BinkP, local terminal/IRC and storage activity without lost serial data.
