# M2.13 — Portable terminal engine

Status: **IMPLEMENTED / HOST-QUALIFIED**

The terminal is a product pillar equal to the BBS. M2.13 freezes the portable engine boundary and an executable compatibility model.

## Pipeline

Transport bytes -> decoder/profile -> terminal parser/state machine -> screen/cell model -> renderer.

Keyboard/mouse -> platform input frontend -> terminal encoder/profile -> transport.

The engine has no W65C265S register, K8T video, Amiga or Atari dependency. Platforms provide allocation, rendering, input, clock and transport adapters.

## Profiles

Initial executable profiles:
- ASCII/dumb;
- ANSI/BBS ANSI core;
- VT100 baseline;
- PETSCII baseline.

Planned qualification expands VT220, CP437/BBS art, UTF-8 network mode and additional historically useful profiles.

## Screen model

A cell stores a character/glyph plus attributes. Cursor position, saved cursor, colors, bold/reverse and clear/erase operations live in terminal state rather than renderer state. Geometry is configurable and not hard-wired to 80x25.

## ANSI/VT parser

The parser is incremental across arbitrary transport chunk boundaries. Baseline CSI support includes cursor movement/positioning, erase display/line and SGR attributes/colors. Unknown/unsupported sequences fail safely and do not corrupt parser state.

## PETSCII

PETSCII is a distinct terminal profile, not treated as ANSI with a font swap. Character mapping, case/graphics modes, control codes, colors, cursor behavior and keyboard encoding belong to the profile. Exact Commodore compatibility will be expanded against test vectors/reference machines.

## Portability

The same parser/state/screen conformance corpus is intended to be compiled/reimplemented against:
- K8T native frontend;
- AmigaOS terminal frontend;
- Atari ST/TOS terminal frontend;
- later constrained Commodore frontend where feasible.

No platform frontend may fork terminal semantics casually; differences are explicit profile/platform capability rules.

## Beyond-first-class UX requirements

Scrollback/search, selection/copy/paste, keymaps/macros, session capture, phonebook, modem profiles, reconnect, X/Y/ZMODEM and serial/Telnet/SSH remain required higher-level terminal services.

## M2.13 acceptance

- hardware-independent terminal core boundary: PASS
- configurable screen geometry: PASS
- incremental ANSI parser: PASS
- cursor/erase/SGR executable model: PASS
- PETSCII distinct profile: PASS
- safe unsupported-sequence behavior: PASS
- shared cross-platform conformance strategy: PASS
