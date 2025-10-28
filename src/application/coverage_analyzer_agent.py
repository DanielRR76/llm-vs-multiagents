import subprocess
from src.domain.state import State
from src.utils.file_manager import FileManager


class CoverageAnalyzer:
    def __init__(self, agent):
        self.agent = agent

    def respond(self, state: State):
        coverage = self.runCoverageAnalysis("src/environment/python/coverage.json")
        prompt = f'User code: "{state.code}".\n Coverage: "{coverage}".\n'
        response = self.agent.chat.completions.create(
            model="n/a",
            messages=[{"role": "user", "content": prompt}],
            extra_body={"include_retrieval_info": True},
        )
        content = (
            response.choices[0].message.content.strip()
            if response.choices and hasattr(response.choices[0].message, "content")
            else ""
        )
        return {"coverage_agent_response": content}

    def runCoverageAnalysis(self, path: str) -> str:
        command = ["make", "python-coverage"]
        subprocess.run(command)

        coverage_content = FileManager.readFile(path)
        coverage_json_string = FileManager.jsonStringify(coverage_content)
        return coverage_json_string
