# agent_manager.py
from langgraph.graph import END, START, StateGraph

from src.application.test_reviewer import TestReviewer
from src.domain.state import State
from src.application.coverage_analyzer import CoverageAnalyzer
from src.application.mutation_test_agent import MutationTestAgent
from src.application.test_generator import TestGenerator
from src.application.quality_agent import QualityAgent
from src.application.code_analyzer import CodeAnalyzer
from src.application.test_strategist import TestStrategist
from src.application.test_executor import TestExecutor


class AgentManager:

    def __init__(
        self,
        coverage_agent: CoverageAnalyzer,
        mutation_test_agent: MutationTestAgent,
        quality_agent: QualityAgent,
        unit_test_agent: TestGenerator,
        code_analyzer_agent: CodeAnalyzer,
        test_strategist_agent: TestStrategist,
        test_executor: TestExecutor,
        reviewer_agent: TestReviewer,
    ):
        self.coverage_agent = coverage_agent
        self.mutation_test_agent = mutation_test_agent
        self.unit_test_agent = unit_test_agent
        self.code_analyzer_agent = code_analyzer_agent
        self.test_strategist_agent = test_strategist_agent
        self.quality_agent = quality_agent
        self.test_executor = test_executor
        self.reviewer_agent = reviewer_agent
        self.workflow = StateGraph(State)
        self._build_workflow()
        self.chain = self.workflow.compile()

    def _build_workflow(self):
        self.workflow.add_node("coverage", self.coverage_agent.respond)
        # self.workflow.add_node("mutation_tester", self.mutation_test_agent.respond)
        self.workflow.add_node("generator", self.unit_test_agent.respond)
        self.workflow.add_node("analyzer", self.code_analyzer_agent.respond)
        self.workflow.add_node("strategist", self.test_strategist_agent.respond)
        self.workflow.add_node("executor", self.test_executor.execute)
        self.workflow.add_node("reviewer", self.reviewer_agent.respond)

        self.workflow.add_edge(START, "analyzer")
        self.workflow.add_edge("analyzer", "strategist")
        self.workflow.add_edge("strategist", "generator")
        # self.workflow.add_edge("strategist", "mutation_tester")
        self.workflow.add_edge("generator", "executor")
        self.workflow.add_conditional_edges(
            "executor",
            self.test_executor.verifyLogs,
            {True: "coverage", False: "generator"},
        )
        self.workflow.add_edge("coverage", "reviewer")
        self.workflow.add_conditional_edges(
            "reviewer",
            self.reviewer_agent.hasFinalCode,
            {True: END, False: "generator"},
        )
