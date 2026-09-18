# M2.5 — Ethernet and BBS network ingress

Status: **IMPLEMENTED / HOST-QUALIFIED**

## Decision

K8T does **not** use a hardwired-TCP controller as its primary network architecture.

A W5500-class controller is attractive for small embedded systems, but its eight hardware sockets would put an artificial ceiling on a machine whose purpose is multi-user BBSing. K8T instead requires a packet-level Ethernet controller: the W65C265S receives/transmits Ethernet frames through buffered controller memory, while K8T-OS owns ARP, IPv4, ICMP, UDP, TCP and the connection table.

This keeps Telnet/BinkP/Gopher/HTTP/IRC concurrency limited by K8T resources and software policy rather than by eight silicon sockets.

## Hardware contract

Baseline Ethernet:

- 10/100BASE-TX
- RJ45 with magnetics
- packet/frame-level controller interface
- controller RX/TX buffering
- interrupt on useful packet/event batches
- MAC address stored in board configuration
- no hidden general-purpose CPU running the network stack
- no requirement for FPGA

Exact controller part is deferred to BOM/lifecycle/electrical qualification.

## OS network ingress

The Ethernet driver feeds packet buffers into K8TNet. K8TNet owns:

- Ethernet II framing
- ARP
- IPv4
- ICMP
- UDP
- TCP
- DNS client
- listening endpoints
- connection table
- timers/retransmission
- socket-like handles/events exposed through the M2.2 kernel ABI

IPv6 is a later extension, not an M2.5 requirement.

## BBS service model

Network connections are independent of the four physical serial nodes.

Initial service classes include:

- Telnet BBS nodes
- BinkP inbound/outbound sessions
- Gopher
- lightweight HTTP
- IRC client/gateway
- RSS/Atom publication fetch/push where applicable
- administration/diagnostics when enabled

A listener does not consume a permanently dedicated hardware TCP socket. Accepted connections become K8TNet connection objects and may scale until RAM/CPU/service limits are reached.

## Resource policy

M2.5 host qualification sets an initial software target of **32 concurrent TCP connections**, excluding listeners. This is not the final product maximum; it is a design floor chosen to prove that the architecture is not constrained to eight sessions.

Each connection has bounded RX/TX queues. Services may impose lower per-service limits and idle timeouts. Under memory pressure, new connections fail cleanly rather than corrupting existing BBS sessions.

## Ingress routing

A completed TCP accept is routed by listening port/service identity into a service task. Telnet sessions are handed to the BBS node manager and become network BBS nodes using the same authentication/session core as serial nodes.

BinkP, Gopher, HTTP and IRC use their own protocol tasks but share the kernel handle/event model and central BBS ACL/publication policy.

## Fault isolation

Malformed packets, connection resets and a failed network service must not terminate serial BBS nodes. Driver interrupt work remains bounded; protocol parsing occurs in tasks.

## Why not W5500 as baseline?

W5500 integrates IPv4/TCP/UDP and provides eight simultaneous hardware sockets. That is excellent for many MCU products, but the fixed socket count conflicts with K8T's BBS-first concurrency goal. It remains a possible development/debug adapter, not the motherboard network architecture.

## M2.5 acceptance

- packet-level Ethernet architecture: PASS
- OS-owned TCP/IP connection table: PASS
- no eight-socket hardware ceiling: PASS
- 32 concurrent TCP connection design floor: PASS
- Telnet ingress maps to BBS nodes: PASS
- BinkP/Gopher/HTTP/IRC service routing defined: PASS
- bounded packet queues and clean resource exhaustion: PASS
- serial/network fault isolation: PASS

Exact Ethernet IC selection and electrical schematic are deferred to hardware BOM qualification.
