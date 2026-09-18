"""K8T M2.13 portable terminal engine host model."""
from dataclasses import dataclass

@dataclass
class Cell:
 ch:str=" "; fg:int=7; bg:int=0; bold:bool=False; reverse:bool=False

class Screen:
 def __init__(self,w=80,h=25):
  self.w=w; self.h=h; self.x=0; self.y=0; self.cells=[[Cell() for _ in range(w)] for _ in range(h)]
 def put(self,ch):
  self.cells[self.y][self.x]=Cell(ch); self.x+=1
  if self.x>=self.w: self.x=0; self.y=min(self.h-1,self.y+1)
 def clear(self):
  self.cells=[[Cell() for _ in range(self.w)] for _ in range(self.h)]; self.x=self.y=0

class ANSI:
 def __init__(self,screen): self.s=screen; self.state="text"; self.csi=""
 def feed(self,data):
  for ch in data:
   if self.state=="text":
    if ch=="\x1b": self.state="esc"
    elif ch=="\r": self.s.x=0
    elif ch=="\n": self.s.y=min(self.s.h-1,self.s.y+1)
    elif ch>=" ": self.s.put(ch)
   elif self.state=="esc":
    if ch=="[": self.state="csi"; self.csi=""
    else: self.state="text"
   else:
    if ch.isdigit() or ch==";": self.csi+=ch
    else: self._csi(ch); self.state="text"
 def _nums(self): return [int(x) if x else 0 for x in self.csi.split(";")] if self.csi else [0]
 def _csi(self,final):
  n=self._nums()
  if final in "Hf":
   row=(n[0] or 1)-1; col=((n[1] if len(n)>1 else 1) or 1)-1
   self.s.y=max(0,min(self.s.h-1,row)); self.s.x=max(0,min(self.s.w-1,col))
  elif final=="A": self.s.y=max(0,self.s.y-(n[0] or 1))
  elif final=="B": self.s.y=min(self.s.h-1,self.s.y+(n[0] or 1))
  elif final=="C": self.s.x=min(self.s.w-1,self.s.x+(n[0] or 1))
  elif final=="D": self.s.x=max(0,self.s.x-(n[0] or 1))
  elif final=="J" and (n[0] in (0,2)): self.s.clear()

class PETSCII:
 @staticmethod
 def decode(b):
  if b==0x93:return ("clear",None)
  if 0x41<=b<=0x5a:return ("char",chr(b))
  if 0x20<=b<=0x7e:return ("char",chr(b))
  return ("control",b)
