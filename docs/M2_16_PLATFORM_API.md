# M2.16 — Portable terminal platform API

Status: **IMPLEMENTED / HOST-QUALIFIED**

M2.16 freezes the boundary between the shared terminal/transfer core and native platform frontends.

## Core/platform split

The shared core owns terminal parsing/state, character/profile decoding, screen/cell semantics, scrollback semantics, connection state, transfer protocol state machines and conformance vectors.

A platform frontend owns:
- video/window rendering;
- keyboard and mouse/event acquisition;
- monotonic clock/timers;
- filesystem primitives;
- serial/network byte streams;
- allocation policy;
- clipboard where available;
- UI chrome/requesters/menus.

The core never calls AmigaOS, TOS/GEM or K8T hardware directly.

## Platform API

The minimal contract exposes clock, render-dirty-region, input events, stream open/read/write/close, file open/read/write/seek/close, allocation capability and optional clipboard/mouse hooks. Operations are incremental/non-blocking or explicitly bounded.

Capabilities are discoverable. Missing mouse, clipboard, UTF-8 font or network support degrades functionality rather than forking terminal semantics.

## K8T frontend

The native K8T frontend binds the API to K8T video/input, four UARTs, modem control, TCP/Telnet/SSH services, storage and mouse. It remains the reference embedded target.

## AmigaOS frontend contract

Initial target: AmigaOS 2.04+ / 68000 where practical, with richer acceleration optional.

Bindings:
- Intuition/graphics rendering and native requesters/menus;
- keyboard/mouse through native event handling;
- serial.device for serial/modem;
- bsdsocket.library-compatible network binding where present;
- AmigaDOS files;
- clipboard.device where available.

The shared core must not require an MMU, FPU, RTG or high-end CPU.

## Atari ST/TOS frontend contract

Initial target: classic 68000-class TOS systems where practical.

Bindings:
- GEM/VDI or direct optimized renderer behind the same frontend boundary;
- keyboard/mouse through platform events;
- serial/MFP/OS facilities through a bounded adapter;
- GEMDOS files;
- network adapters/stacks are optional capabilities.

The core must remain useful as a serial/modem terminal on machines without Ethernet.

## Cross-platform qualification

Golden input streams and expected screen/state snapshots are shared. ANSI/VT/PETSCII, keyboard encoding and X/Y/ZMODEM/Kermit state tests must be platform-independent. Frontend tests then verify rendering/input/transport bindings separately.

## M2.16 acceptance

- explicit core/platform boundary: PASS
- capability discovery/degradation: PASS
- K8T frontend contract: PASS
- AmigaOS 2.04+/68000 contract: PASS
- Atari ST/TOS 68000-class contract: PASS
- shared conformance corpus requirement: PASS
