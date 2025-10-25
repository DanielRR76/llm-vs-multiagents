from src.domain.state import State


class CodeAnalyzer:
    def __init__(self, agent):
        self.agent = agent

    def respond(self, state: State):
        prompt = f'Código: "{state.code}".\n'
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
        return {"code_analyzer_response": content}
