import json
import logging
from typing import Any, Dict

from config.config import Config
from src.application.agent_manager import AgentManager
from src.application.coverage_agent import CoverageAgent
from src.application.mutation_test_agent import MutationTestAgent
from src.application.quality_agent import QualityAgent
from src.application.unit_test_agent import UnitTestAgent
from src.application.query_manager import QueryManager
from src.infrastructure.ai_agents import Agents
from src.interfaces.ui.stremlit_app import Index


class Main:
    def __init__(self):
        self.config = Config()
        logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    def run(self):
        try:
            coverage_agent = CoverageAgent(
                Agents.load_agent(*self.config.coverage_agent)
            )
            mutation_test_agent = MutationTestAgent(
                Agents.load_agent(*self.config.mutation_test_agent)
            )
            quality_agent = QualityAgent(Agents.load_agent(*self.config.quality_agent))
            unit_test_agent = UnitTestAgent(
                Agents.load_agent(*self.config.unit_test_agent)
            )

            logging.info("Todos os agentes carregados com sucesso")
        except Exception as e:
            logging.error(f"Erro ao carregar agentes: {e}", exc_info=True)
            return
        agent_manager = AgentManager(
            coverage_agent=coverage_agent,
            mutation_test_agent=mutation_test_agent,
            quality_agent=quality_agent,
            unit_test_agent=unit_test_agent,
        )

        query_manager = QueryManager(agent_manager=agent_manager)
        app = Index(query_manager=query_manager)
        app.render()


if __name__ == "__main__":
    Main().run()
