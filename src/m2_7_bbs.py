"""K8T M2.7 canonical BBS core host model."""
from dataclasses import dataclass, field

BUILTIN_GROUPS={"Guest","User","Trusted","Sysop"}
ACTIONS={"read","post","upload","download","list","moderate","administer","publish"}
SURFACES={"bbs","serial","telnet","fidonet","gopher","http","rss","atom","irc"}
NODE_STATES={"idle","connected","authenticating","online","closing"}

@dataclass(frozen=True)
class ACLRule:
    subject:str
    action:str
    allow:bool

@dataclass
class Area:
    aid:int
    name:str
    rules:list=field(default_factory=list)
    surfaces:set=field(default_factory=lambda:{"bbs"})

@dataclass
class User:
    uid:int
    name:str
    groups:set=field(default_factory=lambda:{"User"})

@dataclass
class Node:
    nid:int
    transport:str
    state:str="idle"
    session_id:int|None=None

@dataclass
class Session:
    sid:int
    node_id:int
    user_id:int|None=None
    terminal:str="ansi"

@dataclass(frozen=True)
class Message:
    mid:int; area_id:int; author:int|None; subject:str; body:str; created:int; reply_to:int|None=None

@dataclass
class FileEntry:
    fid:int; area_id:int; filename:str; storage_ref:str; size:int; uploader:int|None; uploaded:int
    description:str=""; downloads:int=0

def allowed(user,area,action):
    if action not in ACTIONS: return False
    subjects={"Guest"} if user is None else ({f"user:{user.uid}"} | set(user.groups))
    matching=[r for r in area.rules if r.action==action and r.subject in subjects]
    if any(not r.allow for r in matching): return False
    return any(r.allow for r in matching)

class BBSCore:
    def __init__(self):
        self.nodes={i:Node(i,"serial") for i in range(1,5)}
        self.sessions={}
        self.next_network_node=100
        self.next_session=1

    def new_network_node(self):
        nid=self.next_network_node; self.next_network_node+=1
        self.nodes[nid]=Node(nid,"telnet")
        return self.nodes[nid]

    def connect(self,nid):
        n=self.nodes[nid]
        if n.session_id is not None: raise ValueError("node busy")
        sid=self.next_session; self.next_session+=1
        self.sessions[sid]=Session(sid,nid)
        n.session_id=sid; n.state="connected"
        return self.sessions[sid]

    def disconnect(self,nid):
        n=self.nodes[nid]
        sid=n.session_id
        if sid is not None: self.sessions.pop(sid,None)
        n.session_id=None; n.state="idle"
