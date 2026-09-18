"""K8T M2.16 portable platform API host contract."""
from dataclasses import dataclass, field
@dataclass(frozen=True)
class Capabilities:
 mouse:bool=False; clipboard:bool=False; network:bool=False; utf8_font:bool=False
@dataclass
class Platform:
 name:str; caps:Capabilities=field(default_factory=Capabilities)
 streams:set=field(default_factory=set)
 def supports(self,feature): return bool(getattr(self.caps,feature,False))
 def open_stream(self,kind):
  allowed={"serial","modem"}|({"telnet","ssh"} if self.caps.network else set())
  if kind not in allowed: raise ValueError("unsupported stream")
  self.streams.add(kind); return kind
 def close_stream(self,kind): self.streams.discard(kind)
def frontend_contract(name):
 n=name.lower()
 if n=="k8t": return Capabilities(True,True,True,True)
 if n=="amiga": return Capabilities(True,True,True,False)
 if n=="atari-st": return Capabilities(True,False,False,False)
 raise ValueError("platform")
