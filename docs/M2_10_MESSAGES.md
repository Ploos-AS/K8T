# M2.10 — Message bases, editor and scalable indexing

Status: **IMPLEMENTED / HOST-QUALIFIED**

## Scale

Messages and message areas use stable unsigned 32-bit IDs. There is no per-area 16-bit message ceiling and no small fixed area table. Durable records and indexes are disk-backed; RAM tracks pages/caches and active editor/session state.

## Canonical message

A message contains stable ID, area ID, author/local or external identity, subject, body reference, creation time, reply-to ID, thread root ID, origin metadata and flags. Local, FidoNet and publication adapters map to this canonical representation.

## Indexing

Each area maintains disk-backed ordered indexes for message ID/time and thread relationships. The host model uses sorted pages to express the contract; the target implementation may use B-tree/B+tree or another measured structure.

Requirements:
- bounded page cache;
- logarithmic/page-oriented lookup rather than loading the whole area;
- append without rewriting all existing messages;
- rebuildable indexes from canonical records;
- pagination forward/backward;
- last-read cursors stored per user/area;
- no O(total BBS messages) RAM structure.

## Threads

Replies retain reply-to and thread-root IDs. Readers can show chronological, threaded or unread views without duplicating message bodies.

## Editor

The built-in editor is terminal-aware and supports ANSI-capable and plain terminals. Baseline:
- insert/delete text;
- line editing and navigation;
- word wrap;
- quote selected parent-message text;
- subject editing;
- abort/save confirmation;
- draft state isolated per session;
- configurable body-size policy rather than a tiny format limit.

The editor operates on bounded chunks/lines so a large draft does not require an unbounded contiguous buffer.

## FidoNet readiness

Canonical origin metadata reserves external network identity, message IDs and routing/kludge metadata needed by later FidoNet mapping. FidoNet-specific wire formats do not leak into local message-area storage.

## Publication

Area ACL/publication policy remains authoritative for Gopher/HTTP/RSS/Atom/IRC views. A publication adapter may render messages but cannot bypass read/publish authorization.

## M2.10 acceptance

- 32-bit message and area IDs: PASS
- no small fixed message/area tables: PASS
- paged disk-backed index contract: PASS
- bounded RAM working set: PASS
- reply/thread model: PASS
- per-user last-read cursor: PASS
- ANSI/plain terminal editor contract: PASS
- FidoNet-ready canonical metadata: PASS
