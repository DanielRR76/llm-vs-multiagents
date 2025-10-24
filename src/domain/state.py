from dataclasses import dataclass, field
from typing import Dict


@dataclass
class State:
    code: str = ""
    coverage_agent_response: str = ""
    mutation_agent_response: str = ""
    performance_agent_response: str = ""
    test_generator_response: str = ""
    test_executor_response: Dict[str, object] = field(default_factory=dict)
    quality_agent_response: str = ""
    final_code: str = ""
