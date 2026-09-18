"""K8T M2.9 menu, bulletin and budgeted KScript host model."""
from dataclasses import dataclass, field

@dataclass(frozen=True)
class MenuCommand:
    key:str; action:str; target:str; groups:frozenset=frozenset({"Guest","User","Trusted","Sysop"})

@dataclass
class Menu:
    mid:int; title:str; commands:list=field(default_factory=list)
    def invoke(self,key,groups):
        for c in self.commands:
            if c.key.lower()==key.lower():
                if not (set(groups)&set(c.groups)): raise PermissionError("menu ACL")
                return (c.action,c.target)
        raise KeyError(key)

@dataclass
class Bulletin:
    bid:int; title:str; ansi:str|None=None; text:str=""
    def render(self,ansi_capable=True):
        return self.ansi if ansi_capable and self.ansi is not None else self.text

class BudgetExceeded(RuntimeError): pass
class CapabilityError(PermissionError): pass

class KScriptVM:
    def __init__(self,budget=1000,capabilities=()):
        self.budget=budget; self.capabilities=set(capabilities); self.output=[]
    def run(self,program):
        pc=0; stack=[]
        while pc<len(program):
            if self.budget<=0: raise BudgetExceeded()
            self.budget-=1
            op,*args=program[pc]; pc+=1
            if op=="PUSH": stack.append(args[0])
            elif op=="ADD": stack.append(stack.pop()+stack.pop())
            elif op=="JMP": pc=args[0]
            elif op=="JZ":
                if not stack.pop(): pc=args[0]
            elif op=="API":
                cap=args[0]
                if cap not in self.capabilities: raise CapabilityError(cap)
                if cap=="terminal.print": self.output.append(str(stack.pop()))
            elif op=="RET": return stack[-1] if stack else None
            else: raise ValueError(op)
        return stack[-1] if stack else None
