import logging

from config.config import Config
from src.application.agent_manager import AgentManager
from src.application.coverage_analyzer import CoverageAnalyzer
from src.application.mutation_test_agent import MutationTestAgent
from src.application.quality_agent import QualityAgent
from src.application.test_generator import TestGenerator
from src.application.query_manager import QueryManager
from src.application.test_reviewer import TestReviewer
from src.infrastructure.ai_agents import Agents
from src.interfaces.ui.stremlit_app import Index
from src.application.code_analyzer import CodeAnalyzer
from src.application.test_strategist import TestStrategist
from src.application.test_executor import TestExecutor


class Main:
    def __init__(self):
        self.config = Config()
        logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    def run(self):
        try:
            coverage_agent = CoverageAnalyzer(
                Agents.load_agent(*self.config.coverage_agent)
            )
            mutation_test_agent = MutationTestAgent(
                Agents.load_agent(*self.config.mutation_test_agent)
            )
            unit_test_agent = TestGenerator(
                Agents.load_agent(*self.config.unit_test_agent)
            )
            code_analyzer_agent = CodeAnalyzer(
                Agents.load_agent(*self.config.code_analyzer_agent)
            )
            test_strategist_agent = TestStrategist(
                Agents.load_agent(*self.config.test_strategist_agent)
            )
            reviewer_agent = TestReviewer(
                Agents.load_agent(*self.config.reviewer_agent)
            )
            quality_agent = QualityAgent(Agents.load_agent(*self.config.quality_agent))
            test_executor = TestExecutor()

            logging.info("Todos os agentes carregados com sucesso")
        except Exception as e:
            logging.error(f"Erro ao carregar agentes: {e}", exc_info=True)
            return
        agent_manager = AgentManager(
            coverage_agent=coverage_agent,
            mutation_test_agent=mutation_test_agent,
            unit_test_agent=unit_test_agent,
            quality_agent=quality_agent,
            code_analyzer_agent=code_analyzer_agent,
            test_strategist_agent=test_strategist_agent,
            test_executor=test_executor,
            reviewer_agent=reviewer_agent,
        )

        query_manager = QueryManager(agent_manager=agent_manager)
        app = Index(query_manager=query_manager)
        app.render()


if __name__ == "__main__":
    Main().run()
