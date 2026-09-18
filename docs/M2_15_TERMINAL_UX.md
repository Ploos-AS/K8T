# M2.15 — Terminal UX and connection manager

Status: **IMPLEMENTED / HOST-QUALIFIED**

M2.15 turns the portable engine into a complete daily-use communications terminal.

## Connection profiles and phonebook

A profile stores a stable ID/name, transport, endpoint, terminal profile, geometry, serial/modem parameters, transfer preferences, reconnect policy and optional login macro reference. Secrets are referenced through protected credential storage rather than embedded in exported phonebook entries.

Transports include serial/direct, modem dial-up, Telnet and SSH. The connection manager owns state transitions and keeps terminal emulation independent of transport lifecycle.

## Connection lifecycle

DISCONNECTED -> CONNECTING/DIALING -> CONNECTED -> RECONNECT_WAIT -> CONNECTING, with explicit FAILED/CANCELLED outcomes. Reconnect uses bounded configurable attempts/backoff and is never an uncontrolled tight loop.

## Hayes modem profiles

Modem profiles support init strings, dial prefix, hangup behavior, auto-answer where appropriate, DCD/DTR semantics, result-code handling and per-device overrides. Raw modem command mode remains accessible.

## Scrollback and search

Scrollback is a bounded ring/page store independent of the visible screen. Capacity is configurable and may spill/page to storage on K8T. Search is incremental and must not block receive processing.

Selection/copy/paste works through the screen/scrollback model. Mouse support is a frontend capability; keyboard-only operation remains complete.

## Macros and keys

Profiles can bind function keys/key chords to text, encoded key sequences or bounded macro actions. Macros may include delays/waits and connection-safe actions, but cannot bypass credential or filesystem policy.

## Capture

Session capture can record received/sent text/bytes with timestamps and connection metadata. Capture is explicit/configurable, bounded by storage policy and clearly separated from terminal scrollback.

## Transfer integration

X/Y/ZMODEM and Kermit are launchable from the terminal UX. ZMODEM detection may offer/auto-start according to profile policy. Transfer mode suspends normal display interpretation of binary payload while preserving connection/session state.

## M2.15 acceptance

- phonebook/profile model: PASS
- serial/modem/Telnet/SSH profile support: PASS
- bounded reconnect state: PASS
- Hayes modem profile contract: PASS
- bounded scrollback/search model: PASS
- macros/key binding contract: PASS
- capture contract: PASS
- transfer UX integration: PASS
