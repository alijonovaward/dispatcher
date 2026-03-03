from pydantic import BaseModel

class Webhook(BaseModel):
    id:int
    branchId: int
    workstationId:int
    rawdata: str

class Operators(BaseModel):
    id:int
    branchId:int
    workstationId:int
    laptopIp:str
    laptopPort:int

class Audio(BaseModel):
    id:int
    operatorId:int
    audio:str
    status:str
