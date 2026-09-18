# M2.1 — Scheduler and context ABI

Status: **IMPLEMENTED / HOST-QUALIFIED**

K8T-OS uses the real W65C265S/W65C816 execution model. Reset begins in emulation mode; the kernel switches to native mode before starting normal multitasking.

## Task context

A schedulable task owns:

- 16-bit A accumulator
- 16-bit X and Y index registers
- 16-bit stack pointer S
- 16-bit Direct Page register D
- 8-bit Data Bank register DBR
- 8-bit Program Bank register PBR
- 16-bit program counter PC
- processor status P

The scheduler contract assumes native mode and normally keeps M=0 and X=0 so A/X/Y are 16-bit. Code that temporarily changes register width must restore the kernel ABI width before entering kernel services.

## Stack model

Each task has a private native-mode 16-bit stack allocation. The kernel never relies on the emulation-mode page-1 stack for normal tasks.

Interrupt/trap entry creates the architectural hardware frame first. The K8T interrupt prologue then saves the remaining task-visible state. A context switch changes to the next task's saved stack/context and restores in the reverse order before RTI.

## Kernel entry

Preemption and device interrupts use the W65C265S priority-encoded interrupt vectors. BRK/COP are reserved as software-controlled kernel/trap entry mechanisms; their exact syscall allocation is deferred to M2.2.

The interrupt path is split:

1. minimal assembly prologue;
2. acknowledge/source capture;
3. bounded device service into ring/block/packet buffers;
4. scheduler decision;
5. optional context switch;
6. restore and RTI.

Long protocol, filesystem and BBS work is never performed in interrupt context.

## Scheduler

Baseline tick: **1 kHz**.

Default task quantum: **10 ticks / 10 ms**.

A higher-priority ready task may preempt immediately when an interrupt makes it runnable. Device service tasks should block on events rather than poll.

The scheduler is priority-based round-robin within equal priority. Starvation prevention and exact priority count are M2.2 policy details.

## Context image

The host-side ABI model uses this canonical logical image:

| Field | Width |
|---|---:|
| A | 16 |
| X | 16 |
| Y | 16 |
| S | 16 |
| D | 16 |
| PC | 16 |
| DBR | 8 |
| PBR | 8 |
| P | 8 |

This is a logical ABI, not a claim that every field is pushed by hardware in this exact order. Low-level assembly must follow W65C816/W65C265S interrupt semantics.

## Design consequences

- No fictional supervisor bit or MMU is assumed.
- Direct Page is task context and may be used as a fast per-task/kernel workspace.
- DBR/PBR are context and allow tasks/code/data to live across the 24-bit address space.
- Native 16-bit stack support makes nested calls and preemptive tasks substantially cleaner than the old provisional M1 model.
- Four UART RX/TX vectors can feed per-channel ring buffers with bounded interrupt work.
- The scheduler ABI is independent of a future project/repository rename.

## Qualification

Host tests verify that a full context round-trip preserves all task-visible fields, stack allocations do not overlap, the 1 kHz/10 ms scheduling constants are stable, and an interrupt wakeup can request immediate preemption.

Physical timing and instruction-level save/restore qualification remain a later hardware/runtime test.
