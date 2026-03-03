from pydantic import BaseModel
from enum import Enum

class Webhook(BaseModel):
    id:int
    branch_id: int
    workstation_id:int
    rawdata: str

class Operator(BaseModel):
    id:int
    branch_id:int
    workstation_id:int
    laptop_ip:str
    laptop_port:int

class AudioStatus(str, Enum):
    started = "started"
    stopped = "stopped"
    uploaded = "uploaded"

class Audio(BaseModel):
    id:int
    operator_id:int
    audio:str
    status:AudioStatus = AudioStatus.started
