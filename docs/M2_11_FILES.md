# M2.11 — File areas, transfer queues and X/Y/ZMODEM

Status: **IMPLEMENTED / HOST-QUALIFIED**

## Scale and canonical file records

File areas and file records use stable unsigned 32-bit IDs. There is no small fixed area table or per-area file ceiling. Metadata/indexes are disk-backed and paged; RAM scales with active searches/listings/transfers rather than total library size.

A canonical file record contains ID, area ID, display filename, storage object/reference, byte size, uploader, upload time, description, content hash, download count and flags. Physical storage paths are not user-visible authority.

## File-area policy

Every area has ACL actions for list, download, upload and administer. Optional policies include upload approval/quarantine, per-user quota/accounting, filename rules and publication surfaces. Protocol adapters cannot bypass area policy.

## Index/search contract

Disk-backed indexes support ID, normalized filename, upload time and configurable metadata search. Listing is paged. Indexes are rebuildable from canonical records and do not require an O(total files) RAM table.

## Transfer jobs

Transfers are explicit per-session jobs with direction, protocol, file(s), byte counters, state and cancellation. A caller disconnect cancels only that caller's jobs. Scheduler/device work is bounded so four serial nodes and network callers can transfer concurrently.

## Protocols

Required serial/terminal transfer protocols:
- XMODEM checksum/CRC compatibility;
- YMODEM batch/metadata;
- ZMODEM as the preferred first-class protocol, including streaming and resume where interoperable.

Protocol state machines use bounded buffers and timeouts. No transfer loop may busy-wait or monopolize the scheduler. Exact interoperability is a later runtime qualification target against established implementations.

## Upload transaction

An upload is not published merely because bytes arrived:
1. receive into staging;
2. validate size/policy and compute content hash;
3. optional quarantine/approval policy;
4. durable storage commit;
5. canonical metadata/index transaction;
6. publish atomically to the area.

Interrupted/incomplete uploads remain invisible and are reclaimable.

## Downloads

Download authorization is checked when the job starts and again before opening the storage object. Successful completion updates accounting/download count transactionally; partial/cancelled transfers do not masquerade as completed downloads.

## Network transfers

The canonical transfer/job layer is transport-neutral. Future HTTP or other download/upload adapters reuse the same ACL, accounting and storage objects rather than maintaining a second file database.

## M2.11 acceptance

- 32-bit file and area IDs: PASS
- no small fixed file/area limits: PASS
- paged disk-backed listing/index contract: PASS
- canonical storage metadata: PASS
- bounded concurrent transfer jobs: PASS
- XMODEM/YMODEM/ZMODEM state contract: PASS
- staged atomic upload publication: PASS
- resume/accounting hooks: PASS
