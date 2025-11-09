from dataclasses import dataclass, field
from typing import Any, Dict
from .state import State


@dataclass
class OutputDTO:
    success: bool = False
    code: str = ""
    state: State = field(default_factory=State)
    error: str = ""
