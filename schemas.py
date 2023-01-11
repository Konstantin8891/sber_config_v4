from typing import List

from pydantic import BaseModel


class KeySchema(BaseModel):
    service_key: str
    service_value: str


class ServiceSchema(BaseModel):
    name: str
    version: str
    is_used: bool
    keys: List[KeySchema]

    class Config:
        orm_mode = True
