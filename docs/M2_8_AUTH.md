# M2.8 — Authentication, login and admission control

Status: **IMPLEMENTED / HOST-QUALIFIED**

## Goals

M2.8 makes serial, Telnet and SSH callers enter the same canonical BBS authentication/session system while protecting public network listeners from automated connection and password abuse.

SSH is a required K8T feature, not an optional product goal. Exact cryptographic implementation must still be benchmarked/qualified on target hardware.

## Login flow

1. transport establishes a candidate connection;
2. admission control evaluates source and current load;
3. terminal profile/banner is selected;
4. username/handle is requested;
5. authentication policy is applied;
6. successful authentication binds canonical user to the node session;
7. login bulletins/scripts run;
8. caller enters the BBS menu.

Serial callers are not subject to IP admission controls, but use the same user authentication policy where configured.

## Users

User records support:

- stable 32-bit user ID;
- login name/handle and display alias;
- group membership;
- enabled/disabled/locked state;
- password verifier metadata;
- failed-login counters/timestamps;
- created/last-login/last-call metadata;
- optional expiration;
- sysop notes/flags.

Password storage uses a salted, versioned password-verifier format. The exact KDF is selected only after target-hardware benchmarking; plaintext or reversible password storage is forbidden.

## New users

Configurable modes:

- closed — sysop-created accounts only;
- application — caller submits new-user application for approval;
- open — immediate account creation subject to policy.

New users begin with explicitly configured groups/ACLs, never implicit Sysop/Trusted access.

## Admission control / anti-bot

Public Telnet and SSH listeners share a lightweight pre-auth admission layer designed to protect an 8 MHz machine from bot banging.

Required controls:

- global candidate-connection ceiling;
- per-source concurrent connection ceiling;
- per-source token-bucket connection rate;
- authentication failure tracking;
- escalating temporary source cooldown after repeated failures;
- global authentication-work budget;
- short pre-auth idle timeout;
- bounded banner/input sizes;
- reject work before allocating a full BBS node/session where possible;
- counters exported to audit/Prometheus;
- allow/deny lists;
- configurable trusted-management sources without bypassing password/SSH authentication.

The implementation must prefer cheap rejection before expensive cryptographic/password work.

## SSH

SSH is mandatory for encrypted BBS/sysop access.

Requirements:

- same canonical K8T users/sessions as Telnet/serial;
- modern algorithms only from the subset demonstrated feasible on target hardware;
- password authentication may be supported;
- public-key authentication is a target requirement, especially for Sysop;
- host-key management and regeneration;
- no shell escape into raw kernel/hardware unless an explicitly authorized management interface provides it;
- admission controls apply before/through SSH handshake as far as protocol implementation permits;
- handshake concurrency and crypto work are strictly budgeted.

If native SSH performance cannot meet acceptance at 8 MHz, the architecture must be optimized or hardware assistance considered without replacing K8T with a hidden general-purpose computer. External SSH gateways remain deployable but do not satisfy the product's native SSH requirement.

## KScript doors

KScript is explicitly allowed to implement **simple doors**, not only background automation.

A scripted door receives the same controlled Door API/session context as a native door and may:

- render ANSI/text UI;
- read caller input;
- maintain door-local persistent state through approved APIs;
- inspect permitted user/node/session properties;
- use timers/randomness;
- access permitted message/file APIs;
- participate in scores/statistics;
- chain to another door/menu.

Examples include trivia, voting, questionnaires, simple adventure/card/dice games, polls and utility doors.

CPU-intensive games, custom binary protocols or applications needing low-level performance remain native-door territory.

## Sysop management

Sysop tools must support user lookup/edit, group membership, lock/unlock, ban/cooldown inspection, password reset/invalidation, session/node inspection and forced disconnect. Administrative actions are audit logged.

## M2.8 acceptance

- canonical login flow across transports: PASS
- user/account state model defined: PASS
- versioned salted verifier requirement: PASS
- new-user modes defined: PASS
- shared Telnet/SSH anti-bot admission policy: PASS
- cheap-before-expensive rejection policy: PASS
- SSH is mandatory architecture requirement: PASS
- KScript simple doors are first-class: PASS
- sysop user/session management defined: PASS
