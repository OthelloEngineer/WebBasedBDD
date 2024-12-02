from dataclasses import dataclass


@dataclass
class NewResponse:
    message: str
    context: list[str]
    user: str
