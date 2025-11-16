import subprocess
from src.domain.state import State
from src.utils.file_manager import FileManager


class TestExecutor:

    def execute(self, state: State):
        print("TestExecutor: Executing tests...")
        test_file_path = "src/environment/python/tests/test_input_code.py"
        FileManager.writeFile(test_file_path, state.test_generator_response)

        command = ["make", "python-test"]

        result = subprocess.run(command, capture_output=True, text=True)
        response = {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode,
        }
        return {"test_executor_response": response}

    def tests_passed(self, state: State) -> bool:
        logs = state.test_executor_response
        if logs["returncode"] != 0:
            return False
        return True
