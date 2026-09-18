# K8T Architecture — M0

## Identity and principles

K8T is a genuine 8-bit communications workstation for terminal use, BBS hosting and classic/modern networking. It boots into the K8T environment; terminal and BBS are first-class applications.

Core services run on K8T-OS, not on a hidden Linux/ARM computer. Hardware helpers may offload repetitive I/O but expose documented interfaces.

## CPU and memory

### K8T CPU identity

K8T has its own CPU and ISA. It is explicitly independent of the K8 computer's CPU/ISA; K8 is not to be redesigned for K8T compatibility and binary compatibility between the machines is not a goal.

The K8T CPU must balance two first-class requirements: it must be powerful enough for the communications workload, and it must remain educational and maker-friendly. The architecture should be explainable from registers, buses, ALU and control sequencing rather than depending on opaque modern CPU features.

FPGA is the reference implementation path for development and the performance-oriented K8T machine, but FPGA is not part of the ISA contract. The ISA and microarchitecture must deliberately remain practical to implement with CPLDs and, as an educational implementation, TTL/74xx-class logic. Avoid features whose only justification is an FPGA shortcut and which make a discrete implementation unreasonable.

The K8T communications workload is the performance acceptance driver: four simultaneous RS-232 channels plus Ethernet, storage, local terminal activity and multitasking must be supportable without sacrificing the understandable 8-bit architecture.

M0 requires an 8-bit data path, 16-bit logical addressing, 16-bit stack pointer, interrupts, reset/NMI path, software traps/system calls and efficient context switching. Initial target is approximately 12–16 MHz.

Standard RAM target is 1 MiB, with at least 4 MiB physical addressing capability through explicit banking.

Provisional logical map:

| Range | Purpose |
|---|---|
| 0000–7FFF | process/local RAM |
| 8000–BFFF | banked RAM window |
| C000–DFFF | shared/kernel RAM |
| E000–EFFF | memory-mapped I/O |
| F000–FFFF | ROM/kernel vectors |

M1 freezes the exact map.

## Communications hardware

K8T has four physical RS-232 ports. Each supports RX/TX, RTS/CTS, DTR/DSR, DCD, RI, independent baud generation, interrupts and hardware FIFO, including classic rates through at least 115200 baud.

Ethernet is mandatory; initial target is 100BASE-TX/RJ45. K8T-OS initially targets ARP, IPv4, ICMP, UDP, TCP and DNS. IPv6 is deferred rather than prohibited.

## Storage

Internal SSD is the primary persistent store for users, messages, files, logs, captures and queues. Its K8T-facing block interface uses 64-bit LBA and must not impose legacy 2/4 GiB limits. The architectural target is at least 1 TB.

SD is removable boot/recovery/import/export media rather than the preferred write-heavy BBS store.

The provisional native filesystem, K8TFS, must support crash-tolerant metadata, checksums for critical metadata, flush semantics, large files, safe concurrency and snapshot/backup primitives.

## Console

K8T is text-first: 80-column modes including 80x25, 80x30 and 80x50, programmable fonts, ANSI/BBS attributes, fast scrolling and virtual consoles.

Keyboard and mouse are standard. Mouse use focuses on selection, copy/paste, scrollback and lightweight navigation.

## Interrupts and reliability

A prioritised interrupt controller covers timer, UART1–4, Ethernet, storage, video, keyboard, mouse, RTC and DMA. A hardware watchdog is required for unattended operation.

## K8T-OS

K8T-OS uses preemptive multitasking. Terminal, BBS, serial nodes, Telnet, Gopher, HTTP, FidoNet/BinkP, IRC, RSS/Atom, networking and storage may execute concurrently. Event-driven service designs are preferred where appropriate.

## BBS data and policy

Users, groups/security levels, messages, message areas, files, file areas, sessions and network metadata form one canonical BBS data model.

Every message/file area has a central policy controlling visibility, read/write, upload/download, authentication, security level and network import/export independently for local/serial BBS, Telnet, FidoNet, Gopher, HTTP, RSS, Atom and IRC gateway.

Protocol servers may not bypass this policy to expose private data.

## FidoNet and Internet services

FidoNet is first-class: addresses, netmail, echomail, packet/bundle handling, nodelists, TIC/file echoes, BinkP over Ethernet and dial-up over RS-232. K8T should operate as a self-contained FidoNet node.

Gopher and lightweight HTTP expose selected BBS content. RSS and Atom publish selected updates. K8T includes an IRC client and may bridge configured BBS areas to IRC.

## Qualification target

A future qualification must demonstrate four active RS-232 connections, several TCP sessions, BBS message/file activity, Gopher/HTTP requests, FidoNet/BinkP processing, local terminal/IRC use and SSD activity simultaneously, with no lost serial bytes.

## Deferred to M1+

Exact K8T ISA details, register addresses beyond the M1 contract, banking refinement, device implementations, physical video/input connectors, scheduler quantum and K8TFS on-disk format remain intentionally open. M2 will freeze the K8T CPU/ISA baseline; it will not alter the K8 CPU.
