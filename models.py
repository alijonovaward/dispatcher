from pydantic import BaseModel
from enum import Enum

class Webhook(BaseModel):
    id:int
    branchId: int
    workstationId:int
    rawdata: str

class Operator(BaseModel):
    id:int
    branchId:int
    workstationId:int
    laptopIp:str
    laptopPort:int

class AudioStatus(str, Enum):
    started = "started"
    stopped = "stopped"
    uploaded = "uploaded"

class Audio(BaseModel):
    id:int
    operatorId:int
    audio:str
    status:AudioStatus = AudioStatus.started
