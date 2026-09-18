import unittest

from src.m1_6_w65c265s_feasibility import CPU_HZ, baseline_loads, report, uart_load


class W65C265SFeasibilityTests(unittest.TestCase):
    def test_four_uart_full_duplex_rx_budget_is_bursted(self):
        load = uart_load()
        self.assertGreater(load.events_per_second, 0)
        self.assertLess(load.cycles_per_second, CPU_HZ * 0.10)

    def test_reference_workload_has_required_headroom(self):
        r = report()
        # Analytical gate: keep >=25% CPU unallocated before real-hardware tests.
        self.assertLessEqual(r["utilization"], 0.75)
        self.assertGreaterEqual(r["headroom"], 0.25)

    def test_model_covers_all_major_workload_classes(self):
        names = " ".join(x.name for x in baseline_loads()).lower()
        for term in ("uart", "scheduler", "ethernet", "storage", "ansi", "bbs"):
            self.assertIn(term, names)


if __name__ == "__main__":
    unittest.main()
