"""K8T M2.6 BBS persistence host model."""
from dataclasses import dataclass

BLOCK_SIZE=512
CRITICAL="critical"; RECOVERABLE="recoverable"; EPHEMERAL="ephemeral"

@dataclass(frozen=True)
class Record:
    txid:int
    kind:str
    key:str=""
    value:bytes=b""

class PersistenceStore:
    def __init__(self,capacity_records=1024):
        self.capacity_records=capacity_records
        self.log=[]
        self.data={}
        self.next_txid=1
        self.generation=0

    def _append(self,record):
        if len(self.log)>=self.capacity_records:
            raise OSError("storage full")
        self.log.append(record)

    def commit(self,key,value):
        tx=self.next_txid; self.next_txid+=1
        self._append(Record(tx,"intent",key,value))
        self._append(Record(tx,"data",key,value))
        self._append(Record(tx,"commit"))
        self.data[key]=value
        self.generation+=1
        return tx

    def inject_incomplete(self,key,value,stage="data"):
        tx=self.next_txid; self.next_txid+=1
        self._append(Record(tx,"intent",key,value))
        if stage=="data": self._append(Record(tx,"data",key,value))
        return tx

    def recover(self):
        committed={r.txid for r in self.log if r.kind=="commit"}
        rebuilt={}
        generations=0
        for r in self.log:
            if r.kind=="data" and r.txid in committed:
                rebuilt[r.key]=r.value
        for tx in sorted(committed):
            if any(r.txid==tx and r.kind=="data" for r in self.log):
                generations+=1
        self.data=rebuilt; self.generation=generations
        return rebuilt

    def snapshot_manifest(self):
        return {"generation":self.generation,"keys":tuple(sorted(self.data))}

def blocks_for(byte_count):
    if byte_count<0: raise ValueError("negative size")
    return (byte_count+BLOCK_SIZE-1)//BLOCK_SIZE
