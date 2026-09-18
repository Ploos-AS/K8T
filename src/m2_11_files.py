"""K8T M2.11 scalable file-area and transfer host model."""
from dataclasses import dataclass, field
from enum import Enum, auto
MAX_ID=0xFFFFFFFF; PAGE_SIZE=64

@dataclass(frozen=True)
class FileRecord:
    fid:int; area:int; name:str; size:int; sha256:str; uploader:int|None
    downloads:int=0
    def __post_init__(self):
        if not(0<self.fid<=MAX_ID and 0<self.area<=MAX_ID): raise ValueError("32-bit id")
        if self.size<0: raise ValueError("size")

@dataclass
class FileArea:
    aid:int; name:str; files:dict=field(default_factory=dict)
    ordered:list=field(default_factory=list)
    def publish(self,f):
        if f.area!=self.aid or f.fid in self.files: raise ValueError("file")
        self.files[f.fid]=f; self.ordered.append(f.fid)
    def page(self,offset=0,limit=PAGE_SIZE):
        return [self.files[i] for i in self.ordered[offset:offset+limit]]

class TransferState(Enum): QUEUED=auto(); ACTIVE=auto(); COMPLETE=auto(); CANCELLED=auto(); FAILED=auto()
@dataclass
class TransferJob:
    jid:int; session:int; direction:str; protocol:str; total:int
    done:int=0; state:TransferState=TransferState.QUEUED
    def start(self): self.state=TransferState.ACTIVE
    def advance(self,n):
        if self.state!=TransferState.ACTIVE: raise RuntimeError("not active")
        self.done=min(self.total,self.done+n)
        if self.done==self.total: self.state=TransferState.COMPLETE
    def cancel(self): self.state=TransferState.CANCELLED

class TransferQueue:
    def __init__(self): self.jobs={}
    def add(self,j): self.jobs[j.jid]=j
    def disconnect(self,session):
        for j in self.jobs.values():
            if j.session==session and j.state in (TransferState.QUEUED,TransferState.ACTIVE): j.cancel()

class UploadStage:
    def __init__(self): self.ready=False; self.published=False
    def validate(self,ok):
        if not ok: raise ValueError("upload policy")
        self.ready=True
    def publish(self):
        if not self.ready: raise RuntimeError("not validated")
        self.published=True
