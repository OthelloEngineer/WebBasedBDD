from dataclasses import dataclass


@dataclass
class NewResponse:
    message: str
    context: list[str]
    user: str


@dataclass
class Context:
    role: str
    content: str

