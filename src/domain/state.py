from dataclasses import dataclass, field
from typing import Dict


@dataclass
class State:
    code: str = ""
    coverage_agent_response: str = ""
    mutation_agent_response: str = ""
    performance_agent_response: str = ""
    unit_agent_response: str = ""
    quality_agent_response: str = ""
    final_code: str = ""