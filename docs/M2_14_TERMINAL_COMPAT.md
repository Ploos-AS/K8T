# M2.14 — Terminal compatibility and transfer framework

Status: **IMPLEMENTED / HOST-QUALIFIED**

M2.14 expands the portable terminal core and freezes file transfer as a first-class terminal function, independent of the local BBS.

## Terminal compatibility

Compatibility targets:
- ANSI/ECMA-48 and classic BBS ANSI;
- VT100 baseline plus VT220-compatible editing/key/control behavior;
- CP437 BBS glyph model;
- PETSCII with Commodore control/color/case/graphics behavior;
- ASCII/dumb terminal;
- UTF-8 network mode with incremental decoding and replacement of invalid input.

Terminal input encoding is profile-specific. Cursor/function keys, backspace/delete, newline policy and PETSCII keyboard mapping are encoded by the selected profile rather than hard-coded in transports.

## File transfer is a terminal service

The terminal application must send and receive files even when K8T's BBS is not involved.

Required protocols:
- XMODEM checksum and CRC;
- XMODEM-1K;
- YMODEM, including batch metadata;
- ZMODEM, including streaming, batch and resume where interoperable;
- Kermit as a first-class protocol family.

Kermit support is architected for negotiated packet size, quoting, checksum/block-check variants and sliding/windowed operation where target resources permit. Exact feature interoperability is qualification-driven rather than claimed from the host model.

Additional historically important transfer protocols (for example SEAlink/Telink variants) are candidates for later compatibility modules after surveying actual use and implementation cost.

## Portable transfer API

Transfer protocols use a transport-neutral byte-stream/timer/file API. They do not directly own UART, Telnet or SSH drivers. This permits the same protocol engines to be reused by future Amiga and Atari ST terminal frontends.

Each protocol is an incremental bounded state machine with:
- timeout/retry;
- cancellation;
- progress/accounting;
- bounded buffers;
- clean handoff between terminal display mode and binary transfer mode;
- no busy waiting.

## Auto-detection

ZMODEM auto-start sequences may trigger an offered transfer when enabled. Auto-detection is policy-controlled and must not cause arbitrary received terminal text to write files without user/configured authorization.

## M2.14 acceptance

- expanded terminal profile contract: PASS
- profile-specific input encoder: PASS
- incremental UTF-8 decoder contract: PASS
- portable transfer API: PASS
- XMODEM/XMODEM-1K/YMODEM/ZMODEM requirements: PASS
- Kermit first-class requirement: PASS
- bounded transfer state-machine contract: PASS
- reusable Amiga/Atari transfer backend: PASS
