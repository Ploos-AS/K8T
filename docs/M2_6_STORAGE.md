# M2.6 — BBS storage and persistence architecture

Status: **IMPLEMENTED / HOST-QUALIFIED**

## Purpose

K8T storage is designed around a BBS that may run unattended for months. Messages, users, file metadata, FidoNet queues and configuration must survive crashes and power loss without turning every write into a heavyweight transaction.

## Media roles

K8T has three distinct storage roles:

1. **Internal SSD** — primary writable BBS storage and normal boot/runtime data.
2. **SD card** — removable import/export, recovery, upgrades and offline backup transfer.
3. **Onboard flash** — immutable/recovery boot and diagnostics; not the normal BBS database.

The BBS must be able to boot into recovery without either SSD or SD.

## Block layer

K8T-OS exposes asynchronous block devices through the M2.2 handle/event model. Baseline logical block size is 512 bytes. Drivers queue requests and complete them via events; the scheduler must not busy-wait for media.

The primary SSD interface/controller is selected later from hardware that can provide buffered block transfers without requiring a hidden general-purpose computer.

## Persistence classes

BBS data is divided by durability need:

### Critical
- user/account database
- message-base indexes and committed messages
- configuration and ACLs
- FidoNet queue state
- filesystem allocation/metadata

Critical updates use write-ahead intent/commit records or equivalent atomic metadata protocol.

### Recoverable
- indexes that can be rebuilt
- search caches
- generated RSS/Atom state
- derived statistics

Recoverable data may be recreated after an unclean shutdown.

### Ephemeral
- active session scratch
- transient protocol buffers
- temporary render data

Ephemeral state need not survive reboot.

## Commit model

A persistence transaction follows:

1. append intent record;
2. flush intent;
3. write new data/metadata;
4. flush affected blocks;
5. append commit record;
6. flush commit.

Recovery replays committed transactions and discards incomplete ones. The design does not require a full general-purpose journaling filesystem to protect the BBS database.

## BBS object layout

The logical storage namespace keeps these concerns separate:

- /system — OS/runtime/configuration
- /bbs/users — accounts and ACL state
- /bbs/messages — message bases
- /bbs/files — file-area metadata
- /files — downloadable file payloads
- /fidonet — inbound/outbound/netmail/echomail queues
- /logs — operational/audit logs
- /spool — protocol and publication queues
- /backup — local backup staging

Exact filesystem format remains open until implementation benchmarking.

## Backup

A running BBS can create a consistent snapshot manifest by briefly freezing commits, recording the committed generation, then resuming. Copying payloads can continue while the board is online.

Backup targets may include SD, another mounted block device or a network service in later milestones.

## Fault behaviour

- failed SSD: serial console/recovery remains available from flash;
- absent SD: no effect on normal BBS operation;
- full filesystem: reject new durable writes cleanly while keeping existing sessions/reads alive where possible;
- incomplete transaction: rollback/discard on recovery;
- corrupt rebuildable index: regenerate from canonical records;
- repeated block errors: mark device degraded and surface a sysop alert.

## Host qualification target

M2.6 models atomic BBS transactions, crash-before-commit recovery, clean commit recovery, storage-full rejection and snapshot generation consistency.

## M2.6 acceptance

- SSD/SD/flash roles separated: PASS
- asynchronous 512-byte block contract: PASS
- BBS durability classes defined: PASS
- intent/data/commit persistence protocol: PASS
- crash recovery semantics defined: PASS
- consistent online snapshot model: PASS
- graceful full/degraded-media behaviour: PASS

Exact SSD controller, filesystem and on-disk binary format are deferred to implementation/BOM qualification.
