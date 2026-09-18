"""K8T M2.4 four-port BBS serial subsystem host model."""
from dataclasses import dataclass, field
from collections import deque

PORT_COUNT=4
RING_SIZE=1024
HIGH_WATER=768
LOW_WATER=256
MAX_BAUD=115200
MODES={"modem","terminal","null_modem","sysop","disabled"}

@dataclass
class ModemSignals:
    rts: bool=True
    cts: bool=True
    dtr: bool=True
    dsr: bool=False
    dcd: bool=False
    ri: bool=False

@dataclass
class SerialPort:
    number:int
    mode:str="disabled"
    baud:int=115200
    signals:ModemSignals=field(default_factory=ModemSignals)
    rx:deque=field(default_factory=lambda:deque(maxlen=RING_SIZE))
    tx:deque=field(default_factory=lambda:deque(maxlen=RING_SIZE))
    framing_errors:int=0
    parity_errors:int=0
    overruns:int=0
    hangup_pending:bool=False

    def configure(self,mode,baud):
        if mode not in MODES: raise ValueError("invalid serial node mode")
        if baud <= 0 or baud > MAX_BAUD: raise ValueError("unsupported baseline baud")
        self.mode,self.baud=mode,baud

    def receive(self,data):
        accepted=0
        for b in data:
            if len(self.rx)>=RING_SIZE:
                self.overruns+=1
                break
            self.rx.append(b & 0xff); accepted+=1
        if len(self.rx)>=HIGH_WATER: self.signals.rts=False
        return accepted

    def read(self,count):
        out=bytes(self.rx.popleft() for _ in range(min(count,len(self.rx))))
        if len(self.rx)<=LOW_WATER: self.signals.rts=True
        return out

    def queue_tx(self,data):
        if not self.signals.cts: return 0
        room=RING_SIZE-len(self.tx)
        data=data[:room]
        self.tx.extend(data)
        return len(data)

    def set_dcd(self,value):
        old=self.signals.dcd
        self.signals.dcd=bool(value)
        if self.mode=="modem" and old and not value:
            self.hangup_pending=True

class SerialSubsystem:
    def __init__(self):
        self.ports=[SerialPort(i+1) for i in range(PORT_COUNT)]
