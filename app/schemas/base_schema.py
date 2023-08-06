from uuid import UUID

import orjson
from pydantic import BaseModel, Field


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class BaseOrJSONModel(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class Base(BaseOrJSONModel):
    id: UUID
    title: str = Field(examples=['Some title'])
    description: str = Field(examples=['Some description'])
