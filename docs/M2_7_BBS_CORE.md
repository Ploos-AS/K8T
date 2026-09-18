# M2.7 — BBS core object and node/session model

Status: **IMPLEMENTED / HOST-QUALIFIED**

## Principle

K8T has one BBS core. Serial, Telnet and future transports are ingress methods, not separate BBS implementations. Authentication, users, groups, ACLs, messages and files are canonical objects shared by every transport.

## Nodes and sessions

A **node** is an available endpoint. Initial node transports are serial and Telnet.

A **session** is a temporary attachment of a user (or pre-login guest) to a node. Sessions carry terminal capabilities and activity state but do not own durable user/message/file data.

Serial node IDs 1–4 are reserved for the physical RS-232 ports. Network nodes are allocated dynamically.

Node states:

- idle
- connected
- authenticating
- online
- closing

A dropped carrier/TCP connection ends only its own session.

## Users and groups

Canonical built-in groups:

- Guest
- User
- Trusted
- Sysop

Sites may define additional groups. A user may belong to multiple groups.

The Sysop group is powerful by policy, not by imaginary CPU privilege; K8T hardware has no MMU/user mode.

## ACL

Permissions are evaluated centrally against a subject (user/groups), object and action. Protocol adapters must not bypass this layer.

Initial actions:

- read
- post
- upload
- download
- list
- moderate
- administer
- publish

An area may additionally define which publication surfaces are enabled:

- bbs
- serial
- telnet
- fidonet
- gopher
- http
- rss
- atom
- irc

Default is deny when no matching allow rule exists. Explicit deny wins over allow.

## Message model

A canonical message contains:

- stable message ID
- area ID
- author user ID / external identity
- subject
- body
- created timestamp
- optional reply-to ID
- origin metadata
- flags

FidoNet, local BBS, Gopher/HTTP publication and future gateways transform this canonical object rather than maintaining unrelated copies where practical.

## File model

A canonical file entry contains:

- stable file ID
- area ID
- display filename
- storage path/object reference
- size
- uploader
- upload timestamp
- description
- hash/checksum metadata
- download count
- flags

Payload bytes remain in the file store; metadata is durable BBS state.

## Areas

Message and file areas own ACL/publication policy. This lets a sysop expose, for example, a public message area over BBS + Gopher + RSS while keeping a private sysop area local/Telnet only.

## M2.7 acceptance

- one BBS core across serial and Telnet: PASS
- four reserved physical serial nodes: PASS
- dynamic network nodes: PASS
- canonical users/groups: PASS
- central default-deny ACL: PASS
- explicit deny precedence: PASS
- canonical message/file records: PASS
- per-area publication surfaces: PASS
- session disconnect isolation: PASS

Persistence wiring to the M2.6 transaction store and full authentication/password format are later implementation milestones.
