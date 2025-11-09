import subprocess
from src.domain.state import State
from src.utils.file_manager import FileManager
import re


class TestExecutor:

    def execute(self, state: State):
        test_file_path = "src/environment/python/input_code_test.py"
        FileManager.writeFile(test_file_path, state.test_generator_response)

        command = ["make", "python-test"]

        result = subprocess.run(command, capture_output=True, text=True)
        response = {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode,
        }
        return {"test_executor_response": response}

    def verifyLogs(self, state: State) -> bool:
        logs = state.test_executor_response
        if logs["returncode"] != 0:
            return False
        return True

    def execute_mutation_test(self, state: State):
        mutation_code: str = str(state.mutation_agent_response)
        FileManager.writeFile("src/environment/python/input_code.py", mutation_code)

        command = ["make", "python-test"]

        result = subprocess.run(command, capture_output=True, text=True)
        response = {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode,
        }
        pattern = (
            r"(=+ short test summary info =+\n[\s\S]+?=+\s*\d+\sfailed,.*?passed.*?=+)"
        )
        match = re.search(pattern, result.stdout)
        if match:
            response["stdout"] = match.group(1)
        return {"test_executor_mutation_response": response.get("stdout")}
