# M2.3 — External bus and memory baseline

Status: **IMPLEMENTED / HOST-QUALIFIED**

## Priority

K8T is a BBS and communications computer. M2.3 optimises the motherboard for low BOM, reliable 24/7 operation and communications throughput. Educational visibility is not a design requirement; K8 and K16 cover that role.

## Memory baseline

The W65C265S native 24-bit address space is used directly.

Initial motherboard target:

- 2 MiB SRAM standard
- footprint/decoder path for 4 MiB SRAM without changing software architecture
- 512 KiB boot/diagnostic flash
- sparse external I/O window for Ethernet, storage, video and expansion
- no 64 KiB bank-switching scheme

SRAM is preferred over DRAM for the first board: no refresh controller, deterministic access, simple standby/recovery behaviour and lower firmware/hardware complexity. Capacity can be revised after BOM qualification.

## Address map

| Range | Size | Use |
|---|---:|---|
| 00:0000–00:FFFF | 64 KiB | low memory, vectors, kernel/direct-page structures |
| 01:0000–20:FFFF | 2 MiB | standard SRAM |
| 21:0000–40:FFFF | 2 MiB | optional SRAM expansion |
| 80:0000–8F:FFFF | 1 MiB | video subsystem aperture |
| 90:0000–9F:FFFF | 1 MiB | Ethernet aperture |
| A0:0000–AF:FFFF | 1 MiB | storage aperture |
| B0:0000–BF:FFFF | 1 MiB | general expansion |
| E0:0000–EF:FFFF | 1 MiB | platform/external I/O |
| F8:0000–FF:FFFF | 512 KiB | boot/diagnostic flash |

Unassigned ranges read as open bus and are reserved for later expansion.

## Decode policy

The motherboard should use the least expensive reliable solution after PCB/BOM comparison. A small CPLD is explicitly acceptable if it replaces enough discrete decode/glue parts to reduce total BOM, routing and failure opportunities. There is no requirement to use 74xx logic for teaching value.

An FPGA is not required for M2.3.

## BBS reliability requirements

- watchdog recovery must not depend on writable volatile configuration
- flash boot path remains available when SSD/SD is absent or corrupt
- RAM test can run before starting BBS services
- external device windows are isolated enough that a missing expansion device cannot alias RAM/ROM
- bus timeouts/error handling are required for external controllers that can stall
- warm restart should preserve diagnostic/reset-cause information where silicon permits

## Throughput requirements

UART traffic uses the four W65C265S serial channels and does not traverse the external expansion bus byte-by-byte except when software drains/fills buffers. Ethernet, storage and video controllers should provide buffering so bus transactions move useful units of work.

## M2.3 acceptance

- direct 24-bit memory map: PASS
- 2 MiB standard / 4 MiB expansion SRAM policy: PASS
- 512 KiB recovery flash region: PASS
- dedicated buffered apertures for video/Ethernet/storage: PASS
- CPLD permitted when it lowers total BOM/complexity: PASS
- no FPGA requirement: PASS
- BBS/24x7 reliability requirements documented: PASS

Final SRAM/flash part numbers and electrical timing are deferred to schematic/BOM qualification.
