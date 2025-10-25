# query_manager.py
from src.application.orchestrator import Orchestrator
from src.domain.state import State
from src.utils.file_manager import FileManager


class QueryManager:

    def __init__(self, agent_manager: Orchestrator):
        self.agent_manager = agent_manager

    def multi_agent_response(self, code: str) -> dict[str, object]:
        state = State(code=code)
        FileManager.writeFile("src/environment/python/input_code.py", code)
        try:
            result = self.agent_manager.chain.invoke(state)
            return {
                "success": True,
                "code": result.get("final_code", {}),
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def unique_llm_response(self, code: str) -> dict[str, object]:
        state = State(code=code)
        try:
            result = self.agent_manager.quality_agent.respond(state)
            return {
                "success": True,
                "code": result.quality_agent_response,
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
