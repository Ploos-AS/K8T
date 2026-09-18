import unittest
from src.m2_9_kscript import *

class M29Tests(unittest.TestCase):
    def test_menu_acl_is_enforced_on_direct_invoke(self):
        m=Menu(1,"Main",[MenuCommand("S","menu","sysop",frozenset({"Sysop"}))])
        with self.assertRaises(PermissionError): m.invoke("S",{"User"})
        self.assertEqual(m.invoke("S",{"Sysop"}),("menu","sysop"))

    def test_bulletin_plain_fallback(self):
        b=Bulletin(1,"News","ANSI","PLAIN")
        self.assertEqual(b.render(False),"PLAIN"); self.assertEqual(b.render(True),"ANSI")

    def test_vm_budget_stops_loop(self):
        vm=KScriptVM(budget=5)
        with self.assertRaises(BudgetExceeded): vm.run([("JMP",0)])

    def test_capability_denied(self):
        vm=KScriptVM(capabilities=())
        with self.assertRaises(CapabilityError): vm.run([("PUSH","hi"),("API","terminal.print"),("RET",)])

    def test_scripted_terminal_output(self):
        vm=KScriptVM(capabilities={"terminal.print"})
        vm.run([("PUSH","Welcome"),("API","terminal.print"),("RET",)])
        self.assertEqual(vm.output,["Welcome"])

if __name__=="__main__": unittest.main()
