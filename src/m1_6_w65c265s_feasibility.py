"""Analytical M1.6 W65C265S workload feasibility model.

This is intentionally conservative and transparent.  It is not a cycle-accurate
65C816 emulator.  It converts device/event rates into an explicit CPU-cycle
budget so assumptions can be reviewed and replaced by measurements on hardware.
"""

from dataclasses import dataclass

CPU_HZ = 8_000_000
UARTS = 4
UART_BAUD = 115_200
BITS_PER_CHARACTER = 10          # 8N1
UART_FIFO_SERVICE_BYTES = 16     # service in bursts, not per byte

@dataclass(frozen=True)
class Load:
    name: str
    events_per_second: float
    cycles_per_event: int

    @property
    def cycles_per_second(self) -> float:
        return self.events_per_second * self.cycles_per_event

def uart_load() -> Load:
    chars_per_second = UART_BAUD / BITS_PER_CHARACTER
    events = UARTS * chars_per_second / UART_FIFO_SERVICE_BYTES
    # Includes interrupt entry/exit plus copying a FIFO burst to/from a ring.
    return Load("4x UART 115200 RX service", events, 260)

def baseline_loads():
    return [
        uart_load(),
        Load("1 kHz scheduler tick/context accounting", 1_000, 220),
        Load("Ethernet packet service", 1_000, 650),
        Load("storage block completions", 250, 500),
        Load("ANSI/text rendering batches", 500, 550),
        Load("BBS/protocol application work", 1_000, 900),
    ]

def utilization(loads=None):
    loads = baseline_loads() if loads is None else loads
    used = sum(x.cycles_per_second for x in loads)
    return used / CPU_HZ, used

def report():
    loads = baseline_loads()
    util, used = utilization(loads)
    return {
        "cpu_hz": CPU_HZ,
        "used_cycles_per_second": used,
        "utilization": util,
        "headroom": 1.0 - util,
        "loads": loads,
    }

if __name__ == "__main__":
    r = report()
    for item in r["loads"]:
        print(f"{item.name}: {item.cycles_per_second:,.0f} cycles/s")
    print(f"TOTAL: {r['used_cycles_per_second']:,.0f}/{r['cpu_hz']:,} cycles/s")
    print(f"UTILIZATION: {r['utilization']:.1%}")
    print(f"HEADROOM: {r['headroom']:.1%}")
