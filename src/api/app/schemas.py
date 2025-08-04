# src/api/app/schemas.py
# This file defines the data schemas used in the API for validating and serializing data.
# It uses Pydantic to define models for the data structures.
from pydantic import BaseModel
from typing import List, Optional

class CPUInfo(BaseModel):
    physical_cores: int
    total_cores: int
    max_frequency: Optional[float]
    current_frequency: Optional[float]
    cpu_usage_percent: float

class ProcessInfo(BaseModel):
    pid: int
    name: str
    username: Optional[str]

class UserSession(BaseModel):
    name: str
    terminal: Optional[str]
    host: Optional[str]
    started: float

class OSInfo(BaseModel):
    system: str
    version: str
    hostname: str

class AgentData(BaseModel):
    cpu_info: CPUInfo
    processes: List[ProcessInfo]
    users: List[UserSession]
    os_info: OSInfo