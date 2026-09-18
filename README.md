# K8T

K8T is an 8-bit communications terminal and BBS computer.

Its purpose is to combine a first-class local terminal, a multitasking BBS, classic serial communications and modern Ethernet services in one understandable machine architecture.

## M0 goals

M0 defines the machine and software contracts before implementation begins.

K8T is specified around:

- its own K8T CPU and ISA, independent of the K8 computer
- an educational and maker-friendly CPU architecture with FPGA as the reference implementation and realistic CPLD/TTL implementations kept as design constraints

- a genuine 8-bit CPU/data path with a 16-bit logical address space
- banked RAM for practical multitasking and caching
- four first-class RS-232 ports
- 100BASE-TX Ethernet
- internal SSD storage plus removable SD
- text-first video with strong ANSI support
- keyboard and mouse, including terminal copy/paste
- preemptive multitasking in K8T-OS
- a shared BBS core for users, messages and files
- per-area publication and access-control policy
- FidoNet/BinkP, Telnet, Gopher, HTTP, IRC, RSS and Atom

The design rule is simple: K8T may use modern components where useful, but it must remain a real, understandable 8-bit computer. No hidden Linux/ARM system is allowed to implement the machine's core services.

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) and [ROADMAP.md](ROADMAP.md).

## Status

**M0 — Architecture foundation: implemented**

The next milestone is M1: executable machine model and register-level device contracts.

## License

MIT
