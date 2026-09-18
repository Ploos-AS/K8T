# Terminal subsystem — beyond first-class requirement

The terminal side of K8T is a product pillar equal to the BBS. It must be an exceptional standalone communications terminal even when the local BBS is unused.

## Architecture
Terminal emulation is split into reusable components: byte/character decoder, terminal state machine, screen/cell model, keyboard/input encoder, transport adapter and renderer. K8T-specific hardware access lives outside the emulation core.

This separation is intentional so the portable core can later be reused for native terminal applications on other retro systems, initially **Amiga** and **Atari ST**, and potentially C64/128 and others where a suitable frontend/backend subset fits.

## Emulation roadmap
Required/target profiles include:
- ANSI/ECMA-48 core and BBS ANSI;
- VT100, with VT220-compatible functionality expanded through qualification;
- PETSCII/Commodore terminal mode;
- plain ASCII/dumb terminal;
- UTF-8 capable network profile with graceful legacy fallback;
- configurable 40/80+ columns and screen geometry where hardware permits;
- CP437-style BBS glyph handling;
- terminal capability/profile detection and user overrides.

Additional historically useful terminal families should be surveyed before terminal compatibility is frozen.

## Terminal features
- high quality scrollback/search;
- selection/copy/paste using keyboard and mouse where available;
- configurable keymaps/macros/function keys;
- capture/log session;
- send text/file;
- X/Y/ZMODEM;
- serial, Telnet and SSH transports;
- phonebook/address book and connection profiles;
- modem dialing/Hayes profiles;
- reconnect;
- local echo/line ending/flow-control settings;
- ANSI/PETSCII art correctness tests;
- scriptable terminal events through a restricted KScript-facing API where appropriate.

## Portable terminal core
The reusable core must avoid assumptions about W65C265S, K8T memory-mapped I/O or K8T video hardware. Platform frontends provide allocation policy, rendering, clock/input and transport bindings.

A future extraction/companion library may produce AmigaOS and Atari ST terminal programs from the same protocol/state-machine test corpus. Platform-specific UIs remain native to each machine rather than forcing the K8T UI onto them.
