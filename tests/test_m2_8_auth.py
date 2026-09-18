import unittest
from src.m2_8_auth import *

class M28Tests(unittest.TestCase):
    def test_per_source_connection_limit(self):
        a=Admission()
        self.assertTrue(all(a.try_connect("1.2.3.4",0) for _ in range(PER_SOURCE_MAX)))
        self.assertFalse(a.try_connect("1.2.3.4",0))

    def test_rate_tokens_bound_reconnects(self):
        a=Admission()
        for _ in range(TOKENS_MAX):
            self.assertTrue(a.try_connect("x",0)); a.disconnect("x")
        self.assertFalse(a.try_connect("x",0))

    def test_failures_trigger_cooldown(self):
        a=Admission()
        for _ in range(FAILURES_BEFORE_COOLDOWN): a.auth_failure("bot",10)
        self.assertFalse(a.try_connect("bot",11))
        self.assertTrue(a.try_connect("bot",10+COOLDOWN_TICKS))

    def test_other_source_not_blocked(self):
        a=Admission()
        for _ in range(FAILURES_BEFORE_COOLDOWN): a.auth_failure("bot",0)
        self.assertTrue(a.try_connect("caller",1))

    def test_global_candidate_limit(self):
        a=Admission()
        for i in range(MAX_CANDIDATES):
            self.assertTrue(a.try_connect(str(i),0))
        self.assertFalse(a.try_connect("extra",0))

if __name__=="__main__": unittest.main()
