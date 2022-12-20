from typing import List, Optional

from pydantic import BaseModel


class Key(BaseModel):
    service_key: str
    service_value: str


class Service(BaseModel):
    name: str
    version: str
    is_used: bool
    keys: List[Key]

    class Config:
        orm_mode = True


class PatchService(BaseModel):
    name: str
    version: str
    is_used: Optional[bool]
    keys: Optional[List[Key]]

    class Config:
        orm_mode = True
