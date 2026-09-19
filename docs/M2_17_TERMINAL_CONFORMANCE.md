# M2.17 — Terminal conformance corpus

Status: **IMPLEMENTED / HOST-QUALIFIED**

M2.17 turns the terminal compatibility requirements into deterministic, platform-neutral golden vectors. The corpus tests semantic screen state rather than pixels, so the same vectors can qualify K8T and later Amiga/Atari ST frontends.

## Corpus contract

Each vector defines a terminal profile, geometry, input chunks, expected cursor position and expected semantic cells. Escape sequences may be split at arbitrary chunk boundaries. A frontend passes only when its core produces the same semantic result.

Initial corpus v1 covers:

- printable ANSI text and CR/LF;
- CUP/HVP and relative cursor movement;
- split CSI sequences across input chunks;
- erase-display baseline;
- SGR reset, bold, reverse and ANSI foreground/background colors;
- CP437 byte-to-glyph reference decoding for BBS box drawing;
- PETSCII clear/home/cursor/reverse controls and printable characters.

Unsupported or malformed sequences must fail safely without corrupting parser state.

## Qualification boundary

This milestone qualifies the implemented corpus and reference semantics. It does **not** claim complete ECMA-48, VT220 or PETSCII compliance. Additional behavior is added only with a golden vector and implementation test.

Pixel rendering remains platform-specific. ANSI art correctness is defined at the cell/attribute level, which lets SysOp-owned ANSI screens use the same corpus on every frontend.

## Acceptance

- corpus is deterministic and versioned as `terminal-corpus-v1`;
- vectors are independent of K8T MMIO/video hardware;
- chunked parsing is tested;
- cell attributes are part of snapshots;
- CP437 and PETSCII have explicit reference cases;
- CI runs the corpus.
