# agent_manager.py
from langgraph.graph import END, START, StateGraph

from src.domain.state import State
from src.application.coverage_analyzer import CoverageAnalyzer
from src.application.mutation_test_agent import MutationTestAgent
from src.application.test_generator import TestGenerator
from src.application.quality_agent import QualityAgent
from src.application.code_analyzer import CodeAnalyzer
from src.application.test_strategist import TestStrategist


class AgentManager:

    def __init__(
        self,
        coverage_agent: CoverageAnalyzer,
        mutation_test_agent: MutationTestAgent,
        quality_agent: QualityAgent,
        unit_test_agent: TestGenerator,
        code_analyzer_agent: CodeAnalyzer,
        test_strategist_agent: TestStrategist,
    ):
        self.coverage_agent = coverage_agent
        self.mutation_test_agent = mutation_test_agent
        self.unit_test_agent = unit_test_agent
        self.code_analyzer_agent = code_analyzer_agent
        self.test_strategist_agent = test_strategist_agent
        self.quality_agent = quality_agent
        self.workflow = StateGraph(State)
        self._build_workflow()
        self.chain = self.workflow.compile()

    def _build_workflow(self):
        self.workflow.add_node("test_coverage", self.coverage_agent.respond)
        self.workflow.add_node("mutation_testing", self.mutation_test_agent.respond)
        self.workflow.add_node("unit_test", self.unit_test_agent.respond)
        self.workflow.add_node("code_analysis", self.code_analyzer_agent.respond)
        self.workflow.add_node("test_strategy", self.test_strategist_agent.respond)
