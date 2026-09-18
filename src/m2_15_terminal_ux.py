"""K8T M2.15 terminal UX host model."""
from dataclasses import dataclass, field
from enum import Enum, auto
from collections import deque

class State(Enum): DISCONNECTED=auto(); CONNECTING=auto(); DIALING=auto(); CONNECTED=auto(); RECONNECT_WAIT=auto(); FAILED=auto(); CANCELLED=auto()

@dataclass
class Profile:
 pid:int; name:str; transport:str; endpoint:str; terminal:str="ansi"; reconnect:int=0
 def __post_init__(self):
  if self.transport not in ("serial","modem","telnet","ssh"): raise ValueError("transport")

class Connection:
 def __init__(self,profile): self.profile=profile; self.state=State.DISCONNECTED; self.attempts=0
 def start(self):
  self.state=State.DIALING if self.profile.transport=="modem" else State.CONNECTING
 def connected(self): self.state=State.CONNECTED; self.attempts=0
 def lost(self):
  if self.attempts<self.profile.reconnect: self.attempts+=1; self.state=State.RECONNECT_WAIT
  else: self.state=State.FAILED
 def retry(self):
  if self.state!=State.RECONNECT_WAIT: raise RuntimeError("not waiting")
  self.start()
 def cancel(self): self.state=State.CANCELLED

@dataclass
class ModemProfile:
 init:str="ATZ"; dial_prefix:str="ATDT"; hangup:str="+++"; require_dcd:bool=True

class Scrollback:
 def __init__(self,limit=1000): self.lines=deque(maxlen=limit)
 def add(self,line): self.lines.append(line)
 def search(self,needle): return [x for x in self.lines if needle.lower() in x.lower()]

@dataclass
class KeyMap:
 bindings:dict=field(default_factory=dict)
 def bind(self,key,value): self.bindings[key]=value
 def get(self,key): return self.bindings.get(key)
