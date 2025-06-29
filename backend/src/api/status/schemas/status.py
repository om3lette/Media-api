from typing import Literal
from pydantic import BaseModel

EventType = Literal["sub", "unsub", "sync"]


class StatusEventSchema(BaseModel):
    type: EventType
    rid: str
