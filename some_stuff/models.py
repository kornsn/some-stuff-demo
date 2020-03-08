from typing import List

from pydantic import BaseModel


class SomeStuff(BaseModel):
    id: int
    name: str


class CreateSomeStuffRequest(BaseModel):
    name: str


class UpdateSomeStuffRequest(CreateSomeStuffRequest):
    pass


class SomeStuffList(BaseModel):
    items: List[SomeStuff]
    limit: int
    offset: int
