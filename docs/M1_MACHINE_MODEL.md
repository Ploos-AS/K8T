# M1 Executable Machine Model

M1 freezes the first register-level machine contract. Addresses are stable for the M1 model; later incompatible changes require an explicit architecture revision.

## CPU-visible reset state

- PC: F000
- SP: DFFF
- A/X/Y: 00
- supervisor mode: enabled

The final ISA remains M2 work. M1 deliberately models programmer-visible state without prematurely freezing instruction encoding.

## Memory map

| Range | Function |
|---|---|
| 0000-7FFF | local RAM |
| 8000-BFFF | 16 KiB bank window |
| C000-DFFF | shared/kernel RAM |
| E000-EFFF | I/O |
| F000-FFFF | ROM |

The initial model contains 1 MiB RAM. A 16 KiB bank window selects physical pages. The bank register contract reserves enough bits for future expansion.

## Core registers

| Address | Name | Meaning |
|---|---|---|
| E000 | BANK_LO | bank selector bits 7:0 |
| E001 | BANK_HI | bank selector extension |
| E010 | IRQ_PENDING | pending IRQ bitmap; write 1 to clear |
| E011 | IRQ_MASK | enabled IRQ bitmap |
| E020 | TIMER_LO | timer reload low byte |
| E021 | TIMER_HI | timer reload high byte |

## UART windows

Four UARTs occupy 16-byte windows:

- UART1 E100-E10F
- UART2 E110-E11F
- UART3 E120-E12F
- UART4 E130-E13F

M1 guarantees independent register storage/windows. FIFO behaviour, modem signals and detailed UART bit definitions are refined in the next device milestone.

## Model purpose

The Python model is a deterministic architecture oracle for register maps, banking, reset semantics and future peripheral tests. It is not intended to become the production emulator.
