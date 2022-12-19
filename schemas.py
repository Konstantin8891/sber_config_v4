from typing import List

from pydantic import BaseModel


class Key(BaseModel):
    service_key: str
    service_value: str


class CreateService(BaseModel):
    name: str
    version: str
    is_used: bool
    keys: List[Key]

    class Config:
        orm_mode = True
