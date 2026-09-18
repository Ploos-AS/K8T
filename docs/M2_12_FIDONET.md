# M2.12 — FidoNet subsystem

Status: **IMPLEMENTED / HOST-QUALIFIED**

K8T is a native FidoNet BBS/node, not merely a BBS with a BinkP helper.

## Canonical mapping
Netmail and echomail map into the canonical M2.10 message model. FidoNet addressing, MSGID/REPLY, origin and routing metadata are preserved without creating a second message database.

## Pipeline
Inbound: receive bundle/packet -> staging -> structural/policy validation -> duplicate detection -> toss -> canonical commit -> area publication.
Outbound: canonical scan -> routing decision -> packet creation -> bundle/spool -> scheduled transport.

Interrupted work is restartable and committed messages are not duplicated.

## Required functions
- netmail;
- echomail;
- packet and bundle handling;
- toss/scan;
- BinkP inbound/outbound;
- nodelist/index lookup;
- routing rules;
- scheduled mail events;
- duplicate suppression;
- quarantine/error spool;
- per-link area permissions and limits;
- statistics/audit.

Classic modem/serial mail transport remains possible alongside BinkP.

## Resource rules
All parsing, scanning and link work is bounded/paged. Large nodelists and message bases remain disk-backed. Network IRQ paths never parse FidoNet content.

## M2.12 acceptance
- canonical netmail/echomail mapping: PASS
- restartable toss/scan pipeline: PASS
- duplicate detection model: PASS
- BinkP/link model: PASS
- routing/nodelist contract: PASS
- bounded disk-backed processing: PASS
