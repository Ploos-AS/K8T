# K8T

K8T is a retro 8/16-bit communications terminal and BBS computer.

Its purpose is to combine a first-class local terminal, a multitasking BBS, classic serial communications and modern Ethernet services in one understandable machine architecture.

## M0 goals

M0 defines the machine and software contracts before implementation begins.

K8T is specified around:

- a WDC W65C265S 8/16-bit processor, independent of the K8 computer
- an educational and maker-friendly external bus architecture
- an 8-bit external data bus and native 24-bit address space
- minimal FPGA use; dedicated ICs, ordinary logic or small CPLDs are preferred where practical
- four first-class RS-232 ports
- 100BASE-TX Ethernet
- internal SSD storage plus removable SD
- text-first video with strong ANSI support
- keyboard and mouse, including terminal copy/paste
- preemptive multitasking in K8T-OS
- a shared BBS core for users, messages and files
- per-area publication and access-control policy
- FidoNet/BinkP, Telnet, Gopher, HTTP, IRC, RSS and Atom

The design rule is simple: K8T may use modern components where useful, but it must remain a real, understandable retro computer built around the W65C265S. No hidden Linux/ARM system is allowed to implement the machine's core services.

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) and [ROADMAP.md](ROADMAP.md).

## Status

**M2 — W65C265S CPU and memory subsystem: in progress (M2.0 complete)**

W65C265S is the selected baseline CPU. M2.1 defines the scheduler/context ABI.

## License

MIT
