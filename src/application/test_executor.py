import subprocess
from src.domain.state import State
from src.utils.file_manager import FileManager


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
