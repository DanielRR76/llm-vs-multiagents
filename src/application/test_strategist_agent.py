from src.domain.state import State


class TestStrategist:
    def __init__(self, agent):
        self.agent = agent

    def respond(self, state: State):
        prompt = f'User code: "{state.code}".\n Code analyst analysis: "{state.code_analyzer_response}".\n'
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
        return {"test_strategist_response": content}
