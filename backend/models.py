from pydantic import BaseModel
from typing import Optional, List

class SignalIn(BaseModel):
    component_id: str
    severity: str

class RCA(BaseModel):
    root_cause: str
    fix: str
    prevention: str

class StatusUpdate(BaseModel):
    status: str