"""K8T M2.5 BBS-first network ingress model."""
from dataclasses import dataclass, field
from collections import deque

MAX_CONNECTIONS=32
QUEUE_BYTES=2048
SERVICES={"telnet","binkp","gopher","http","irc","admin"}

@dataclass
class Connection:
    cid:int
    service:str
    rx:deque=field(default_factory=deque)
    tx:deque=field(default_factory=deque)
    closed:bool=False

    def _queue(self,q,data):
        room=QUEUE_BYTES-len(q)
        accepted=data[:room]
        q.extend(accepted)
        return len(accepted)

    def queue_rx(self,data): return self._queue(self.rx,data)
    def queue_tx(self,data): return self._queue(self.tx,data)

class NetworkIngress:
    def __init__(self,max_connections=MAX_CONNECTIONS):
        self.max_connections=max_connections
        self.connections={}
        self.next_cid=1
        self.listeners={23:"telnet",24554:"binkp",70:"gopher",80:"http"}

    def listen(self,port,service):
        if service not in SERVICES: raise ValueError("unknown service")
        self.listeners[port]=service

    def accept(self,port):
        service=self.listeners.get(port)
        if service is None: raise KeyError("no listener")
        if len(self.connections)>=self.max_connections:
            return None
        c=Connection(self.next_cid,service)
        self.connections[c.cid]=c; self.next_cid+=1
        return c

    def close(self,cid):
        c=self.connections.pop(cid)
        c.closed=True
        return c

    def bbs_node(self,connection):
        return connection.service=="telnet"
