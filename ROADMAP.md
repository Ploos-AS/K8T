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
Status: **DONE — selection pending feasibility test**

- prefer a currently produced physical CPU over a custom FPGA CPU
- minimize FPGA use
- preserve educational and maker-friendly architecture
- W65C02S is the leading strict-8-bit candidate
- W65C265S is a strong alternative only if an 8/16-bit core is acceptable
- next gate: W65C02S workload/throughput feasibility model

See [docs/M1_5_CPU_SURVEY.md](docs/M1_5_CPU_SURVEY.md).

## M1.6 — W65C02S feasibility
Model/benchmark four 115200-bit/s UART streams, interrupt/preemption load, Ethernet, storage, ANSI rendering and BBS activity. Require practical headroom before CPU selection is frozen.

## M2 — K8T CPU and memory subsystem
Design and freeze the independent K8T CPU/ISA baseline. K8 compatibility is explicitly not a goal and K8 is not changed.

- educational and maker-friendly CPU architecture
- genuine 8-bit data path and 16-bit logical addressing
- instruction-set baseline and readable assembler syntax
- FPGA reference implementation without making FPGA an ISA requirement
- CPLD and TTL/74xx feasibility as explicit design constraints
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
