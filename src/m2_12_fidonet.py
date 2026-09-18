"""K8T M2.12 FidoNet host model."""
from dataclasses import dataclass, field
@dataclass(frozen=True)
class FidoAddress:
 zone:int; net:int; node:int; point:int=0
 def __str__(self): return f"{self.zone}:{self.net}/{self.node}"+(f".{self.point}" if self.point else "")
@dataclass(frozen=True)
class FidoEnvelope:
 msgid:str; origin:FidoAddress; dest:FidoAddress|None; area:str|None; body:str
class DupeIndex:
 def __init__(self): self.ids=set()
 def accept(self,msgid):
  if msgid in self.ids:return False
  self.ids.add(msgid); return True
@dataclass
class Link:
 address:FidoAddress; areas:set=field(default_factory=set); enabled:bool=True
 def permits(self,area): return self.enabled and area in self.areas
class Router:
 def __init__(self,routes): self.routes=routes
 def next_hop(self,address):
  return self.routes.get((address.zone,address.net)) or self.routes.get((address.zone,None))
