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

## M2 — CPU and memory subsystem
Instruction-set baseline, assembler syntax, banking, privilege/traps, context switching and timer-driven preemption.

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
