"""K8T M2.14 terminal profiles and portable transfer framework."""
from dataclasses import dataclass
PROTOCOLS=("xmodem","xmodem-crc","xmodem-1k","ymodem","zmodem","kermit")

class UTF8Decoder:
 def __init__(self): self.buf=b""
 def feed(self,data):
  self.buf+=data; out=""
  while self.buf:
   try: out+=self.buf.decode("utf-8"); self.buf=b""; break
   except UnicodeDecodeError as e:
    if e.reason=="unexpected end of data": out+=self.buf[:e.start].decode("utf-8"); self.buf=self.buf[e.start:]; break
    out+=self.buf[:e.start].decode("utf-8",errors="replace")+"�"; self.buf=self.buf[e.end:]
  return out

class InputEncoder:
 def __init__(self,profile="ansi"): self.profile=profile
 def key(self,name):
  maps={
   "ansi":{"UP":b"\x1b[A","DOWN":b"\x1b[B","LEFT":b"\x1b[D","RIGHT":b"\x1b[C"},
   "petscii":{"UP":bytes([0x91]),"DOWN":bytes([0x11]),"LEFT":bytes([0x9d]),"RIGHT":bytes([0x1d])},
  }
  return maps.get(self.profile,{}).get(name,b"")

@dataclass
class Transfer:
 protocol:str; total:int=0; done:int=0; retries:int=0; cancelled:bool=False
 def __post_init__(self):
  if self.protocol not in PROTOCOLS: raise ValueError("protocol")
 def progress(self,n): self.done=min(self.total,self.done+n) if self.total else self.done+n
 def retry(self): self.retries+=1
 def cancel(self): self.cancelled=True

class TransferRegistry:
 def __init__(self): self.protocols=set(PROTOCOLS)
 def supports(self,name): return name.lower() in self.protocols
