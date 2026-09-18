"""K8T M2.10 scalable message-base host model."""
from dataclasses import dataclass, field
from bisect import bisect_left, insort

MAX_ID=0xFFFFFFFF
PAGE_SIZE=64

@dataclass(frozen=True)
class Message:
    mid:int; area:int; author:int|None; subject:str; body:str; created:int
    reply_to:int|None=None; thread_root:int|None=None
    def __post_init__(self):
        if not (0 < self.mid <= MAX_ID and 0 < self.area <= MAX_ID): raise ValueError("32-bit id")

@dataclass
class MessageArea:
    aid:int; name:str
    messages:dict=field(default_factory=dict)
    ordered:list=field(default_factory=list)
    def add(self,m):
        if m.area!=self.aid or m.mid in self.messages: raise ValueError("message")
        self.messages[m.mid]=m; insort(self.ordered,(m.created,m.mid))
    def page(self,offset=0,limit=PAGE_SIZE):
        return [self.messages[mid] for _,mid in self.ordered[offset:offset+limit]]
    def reply(self,mid,new_mid,author,body,created,subject=None):
        parent=self.messages[mid]
        root=parent.thread_root or parent.mid
        m=Message(new_mid,self.aid,author,subject or parent.subject,body,created,parent.mid,root)
        self.add(m); return m

class LastRead:
    def __init__(self): self.cursors={}
    def set(self,user,area,mid): self.cursors[(user,area)]=mid
    def get(self,user,area): return self.cursors.get((user,area),0)

class Draft:
    def __init__(self,max_line=160): self.lines=[]; self.max_line=max_line
    def append(self,line):
        if len(line)>self.max_line: raise ValueError("line too long")
        self.lines.append(line)
    def quote(self,text,prefix="> "):
        for line in text.splitlines(): self.append((prefix+line)[:self.max_line])
    def body(self): return "\n".join(self.lines)
