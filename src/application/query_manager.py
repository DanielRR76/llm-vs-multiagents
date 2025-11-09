# query_manager.py
import time
from src.application.orchestrator import Orchestrator
from src.domain.state import State
from src.utils.file_manager import FileManager
from src.domain.output_dto import OutputDTO


class QueryManager:

    def __init__(self, agent_manager: Orchestrator):
        self.agent_manager = agent_manager

    def multi_agent_response(self, code: str) -> OutputDTO:
        state = State(code=code)
        FileManager.writeFile("src/environment/python/input_code.py", code)
        try:
            inicio = time.time()
            result = self.agent_manager.chain.invoke(state)
            fim = time.time()
            metrics = {
                "coverage": result.get("test_reviewer_response", {}).get("coverage", 0),
                "killed_mutation": result.get("test_reviewer_response", {}).get(
                    "killed_mutation", 0
                ),
                "survived_mutation": result.get("test_reviewer_response", {}).get(
                    "survived_mutation", 0
                ),
                "performance": fim - inicio,
            }
            print(f"Metrics: {metrics}")
            return OutputDTO(
                success=True,
                code=result.get("test_generator_response", ""),
                state=State.from_dict(result),
            )
        except Exception as e:
            return OutputDTO(success=False, error=str(e))

    def unique_llm_response(self, code: str) -> OutputDTO:
        state = State(code=code)
        try:
            inicio = time.time()
            result = self.agent_manager.quality_agent.respond(state)
            fim = time.time()
            print(f"Tempo de execução: {fim - inicio} segundos")
            return OutputDTO(success=True, code=result.quality_agent_response)
        except Exception as e:
            return OutputDTO(success=False, error=str(e))
