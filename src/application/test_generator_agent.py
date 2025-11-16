from src.domain.state import State


class TestGenerator:
    def __init__(self, agent):
        self.agent = agent

    def respond(self, state: State):
        print("TestGenerator: Generating tests...")
        prompt = f'User code: "{state.code_refactor_response or state.code}".\n Test strategist analysis: "{state.test_strategist_response}".\n'
        if state.test_executor_response.get("stderr"):
            prompt += f'Previous test execution errors: "{state.test_executor_response.get("stderr")}".\n'
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
        return {"test_generator_response": clean_code}
