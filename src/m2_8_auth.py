"""K8T M2.8 admission/authentication policy host model."""
from dataclasses import dataclass, field

MAX_CANDIDATES=16
PER_SOURCE_MAX=3
TOKENS_MAX=5
FAILURES_BEFORE_COOLDOWN=4
COOLDOWN_TICKS=300

@dataclass
class Source:
    active:int=0
    tokens:int=TOKENS_MAX
    failures:int=0
    cooldown_until:int=0

class Admission:
    def __init__(self):
        self.sources={}
        self.total=0
        self.denied=0

    def source(self,key):
        return self.sources.setdefault(key,Source())

    def try_connect(self,key,now):
        s=self.source(key)
        if now < s.cooldown_until or self.total>=MAX_CANDIDATES or s.active>=PER_SOURCE_MAX or s.tokens<=0:
            self.denied+=1; return False
        s.tokens-=1; s.active+=1; self.total+=1
        return True

    def disconnect(self,key):
        s=self.source(key)
        if s.active:
            s.active-=1; self.total-=1

    def auth_failure(self,key,now):
        s=self.source(key); s.failures+=1
        if s.failures>=FAILURES_BEFORE_COOLDOWN:
            s.cooldown_until=now+COOLDOWN_TICKS
            s.failures=0

    def auth_success(self,key):
        self.source(key).failures=0

    def refill(self,key,tokens=1):
        s=self.source(key); s.tokens=min(TOKENS_MAX,s.tokens+tokens)
