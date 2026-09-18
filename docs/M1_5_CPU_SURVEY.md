# M1.5 CPU Market Survey

Status: **SURVEY COMPLETE — W65C265S SELECTED AFTER M1.6 ANALYTICAL PASS**

## Goal

K8T should use a real, commercially available processor where practical. A custom FPGA CPU is no longer the preferred direction. FPGA use should be minimized; ordinary logic, CPLD and dedicated peripheral ICs are preferred when they keep the machine understandable and maker-friendly.

Hard requirements:

- retro 8/16-bit machine identity; strict 8-bit CPU operation is not required
- total system/BOM cost matters more than CPU unit price alone
- suitable for a new design rather than depending on obsolete stock
- documented architecture and toolchain
- maker/education friendly
- enough performance for four RS-232 ports, Ethernet, storage, local terminal and a multitasking BBS
- external hardware must remain understandable and serviceable
- practical path to more than 64 KiB RAM through banking or native addressing
- no hidden Linux/ARM computer implementing K8T services

## Survey

| Candidate | Production/longevity | Bus / memory fit | Communications fit | Maker fit | Result |
|---|---|---|---|---|---|
| WDC W65C02S | Strong current WDC ecosystem; current 2024 datasheet and current package listings | 8-bit data, 16-bit address; external banking required | External UART/NIC/storage controllers required | Excellent: PDIP-40, static CPU, visible buses, 1.8–5 V | **Primary pure-8-bit candidate** |
| Microchip ATmega128/128A | Manufacturer lists In Production | 8-bit AVR; external memory interface provides external SRAM/peripheral space, banking still needed for large RAM | Integrated UARTs/timers help, but four serial channels still need support | Good ecosystem, but MCU integration hides more of the computer than W65C02S | **Secondary candidate** |
| Microchip AVR128DA64 | Current family, 24 MHz, 128 KiB flash, 16 KiB SRAM, six USARTs | Excellent MCU resources but no classic full external address/data bus like a traditional MPU | Excellent serial capability | Easy modern design, but substantially less transparent as a retro computer | **Useful benchmark, not preferred architecture** |
| WDC W65C265S | Current WDC ecosystem; external bus, 4 UARTs, 29 prioritized interrupts, timers/watchdog | 8-bit data bus, 24-bit address bus, up to 16 MiB | Outstanding match to K8T peripherals | Very attractive hardware integration | **Strong candidate only if 8/16-bit W65C816 core is acceptable** |
| Digi Rabbit 6000 | Historically almost purpose-built for communications | Powerful and highly integrated | Excellent | Poor long-term choice | **Reject: Rabbit chips have an EOL notice / obsolete status** |
| Z80 / Z180 family | Historically excellent fit | Excellent retro architecture | Good | Excellent historical ecosystem | **Reject for new long-life design: product discontinuation/EOL risk** |
| eZ80 family | High performance and strong communications heritage | Very capable | Excellent | More complex and supply status must be treated cautiously | **Do not select without confirmed long-term production commitment** |

## Important finding: W65C265S

The W65C265S deserves a separate decision because its peripheral set almost reads like a K8T requirement list: external memory bus, 8-bit data bus, 24-bit address bus, four UARTs, 29 priority-encoded interrupts, eight timers and watchdog.

Its W65C816-derived 8/16-bit core is acceptable. This removes the earlier strict-8-bit objection and makes its integration especially attractive because total system cost and component count matter.

## Current direction

Strict 8-bit CPU semantics are not required. **W65C265S is the selected baseline candidate after M1.6 analytical qualification.**

For comparison, a W65C02S design would place substantially more complexity in external peripheral hardware:

- W65C02S CPU
- external bank/page memory controller using ordinary logic or a small CPLD
- dedicated multi-UART hardware with FIFOs
- prioritized interrupt controller
- Ethernet controller with packet buffering/offload appropriate to an 8-bit host
- dedicated storage/block controller
- video/text controller
- DMA only where measurements show it is needed

This preserves the educational value: address bus, data bus, memory decode and I/O transactions remain visible and teachable.

## Performance question to prove before selection

The remaining selection risk was CPU throughput at the W65C265S maximum specified 8 MHz. M1.6 therefore models the target workload:

1. four simultaneous 115200-bit/s serial RX/TX streams with FIFO-backed UARTs;
2. timer-driven preemption and context switching;
3. buffered Ethernet TCP traffic;
4. SSD/block I/O;
5. ANSI terminal rendering;
6. BBS message/file activity.

The CPU does not need to bit-bang these interfaces. Dedicated controllers and FIFOs are part of the architecture. Qualification measures whether the CPU can service the resulting interrupts, buffers and protocol work without serial loss.

## Decision gate

M1.6 produced an analytical PASS for W65C265S with 63.5% reference headroom at 8 MHz. W65C265S is therefore selected as the M2 baseline, while physical hardware qualification remains mandatory before release.
