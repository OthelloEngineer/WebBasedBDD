from dataclasses import dataclass

from pydantic import BaseModel


class Context(BaseModel):
    role: str
    content: str


class NewResponse(BaseModel):
    message: str
    context: list[Context]
    user: str
    model: str
