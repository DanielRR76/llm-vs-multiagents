from src.domain.state import State
from src.utils.file_manager import FileManager


class CodeRefactor:
    def __init__(self, agent):
        self.agent = agent

    def respond(self, state: State):
        print("CodeRefactor: Refactoring code...")
        prompt = f'User code: "{state.code}".\n Test strategist analysis: "{state.test_strategist_response}".\n'
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
        clean_code = content.replace("```python", "").replace("```", "").strip()
        print(f"Refactored code:\n{clean_code}")
        hasCodeRefactor = self.hasCodeRefactorResponse(clean_code)
        if hasCodeRefactor:
            FileManager.writeFile(
                "src/environment/python/app/input_code.py", clean_code
            )
        return {"code_refactor_response": clean_code}

    def hasCodeRefactorResponse(self, response: str):
        if response and response.strip():
            return True
        return False
