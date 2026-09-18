# M2.9 — Menu/bulletin engine and KScript VM/API

Status: **IMPLEMENTED / HOST-QUALIFIED**

M2.9 defines the customization layer that makes a K8T BBS a sysop's own system without recompiling the BBS.

## Menu engine

Menus are data, not hard-coded control flow. A menu has a stable ID, title, optional ANSI/plain presentation asset and ordered commands. Commands can open another menu, enter message/file areas, show bulletins, start doors/KScript, invoke chat or execute an authorized BBS action.

Every command has an ACL predicate. Hidden commands are not merely omitted visually: invoking them directly still goes through authorization.

Menus can select presentation by terminal capability and fall back to plain text.

## Bulletins

Bulletins are first-class objects with stable 32-bit IDs and:
- ANSI asset plus plain-text fallback;
- title;
- ACL;
- optional valid-from/valid-until;
- login/logout/menu/manual presentation roles;
- optional per-user seen state;
- priority/order.

Bulletin count is disk-backed and not constrained by a small fixed table.

## KScript VM

KScript compiles to compact bytecode. The VM is sandboxed and budgeted.

Baseline values: signed integers, booleans and bounded strings. Bytecode has explicit stack/local limits. Each invocation receives an instruction budget and memory budget. Exceeding either terminates only that script.

Initial operations include constants, locals, arithmetic/comparison, conditional/unconditional branch, API call and return. Loops are compiler constructs over branches and therefore remain subject to the instruction budget.

## Capability API

Scripts do not access raw hardware. API capabilities are granted by invocation context. Initial namespaces:

- terminal: print, input, ANSI asset;
- user/session/node: read permitted properties;
- menu/bulletin: show/navigate;
- message/file: authorized canonical operations;
- door: launch/chain and door-local state;
- scheduler/event: register/inspect permitted events;
- stats: permitted counters;
- log: scoped logging.

A login hook receives fewer capabilities than a trusted Sysop script. A scripted door receives door/session capabilities, not arbitrary administration.

## Scripted doors

Simple interactive doors are a first-class KScript use case. Door state is namespaced per door. The VM supplies bounded pseudo-random values, timers and terminal I/O through APIs. A door crash/budget violation returns the caller to the BBS instead of taking down the node.

## Event hooks

Initial hooks: node connect/disconnect, pre-login, login, logout, new-user, message-posted, upload, download, door-start/exit, scheduled event and sysop invocation.

Hooks are queued/bounded; a slow hook cannot stall UART/network interrupt handling.

## M2.9 acceptance

- data-driven menus: PASS
- ACL checked on invocation, not only display: PASS
- ANSI + text bulletin fallback: PASS
- 32-bit bulletin IDs / no small fixed table: PASS
- budgeted sandbox VM: PASS
- capability-scoped BBS API: PASS
- simple scripted doors: PASS
- bounded event hooks: PASS
