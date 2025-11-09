from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass
class State:
    code: str = ""
    code_analyzer_response: str = ""
    coverage_agent_response: Dict[str, Any] = field(default_factory=dict)
    test_strategist_response: str = ""
    mutation_agent_response: str = ""
    test_generator_response: str = ""
    test_executor_response: Dict[str, object] = field(default_factory=dict)
    test_executor_mutation_response: Dict[str, object] = field(default_factory=dict)
    mutation_analysis_response: Dict[str, object] = field(default_factory=dict)
    code_refactor_response: str = ""
    test_reviewer_response: Dict[str, object] = field(default_factory=dict)
    quality_agent_response: str = ""
    final_code: str = ""

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "State":
        return State(
            code=data.get("code", ""),
            code_analyzer_response=data.get("code_analyzer_response", ""),
            coverage_agent_response=data.get("coverage_agent_response", ""),
            test_strategist_response=data.get("test_strategist_response", ""),
            mutation_agent_response=data.get("mutation_agent_response", ""),
            test_generator_response=data.get("test_generator_response", ""),
            test_executor_response=data.get("test_executor_response", {}),
            test_executor_mutation_response=data.get(
                "test_executor_mutation_response", {}
            ),
            test_reviewer_response=data.get("test_reviewer_response", {}),
            quality_agent_response=data.get("quality_agent_response", ""),
            final_code=data.get("final_code", ""),
            code_refactor_response=data.get("code_refactor_response", ""),
            mutation_analysis_response=data.get("mutation_analysis_response", {}),
        )
