from pydantic import BaseModel
from typing import Optional
from enum import Enum

class Webhook(BaseModel):
    id: int
    branch_id: int
    workstation_id: int
    rawdata: str

class Operator(BaseModel):
    id: Optional[int] = None
    branch_id: int
    workstation_id: int
    laptop_ip: str
    laptop_port: int

class AudioStatus(str, Enum):
    started = "started"
    stopped = "stopped"
    uploaded = "uploaded"

class Audio(BaseModel):
    id: Optional[int] = None
    operator_id: int
    webhook_id: int
    audio: Optional[str] = None
    status:AudioStatus = AudioStatus.started
