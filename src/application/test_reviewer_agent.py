import json
from src.domain.state import State


class TestReviewer:
    def __init__(self, agent):
        self.agent = agent

    def respond(self, state: State):
        prompt = f'User code: "{state.code}".\n Test code: "{state.test_generator_response}".\n Test strategist analysis: "{state.test_strategist_response}".\n Coverage: "{state.coverage_agent_response}".\n'
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
        content_json = json.loads(content)
        return {"test_reviewer_response": content_json}

    def hasFinalCode(self, state: State) -> bool:
        review = state.test_reviewer_response
        final_code = review.get("final_code")
        if final_code:
            state.final_code = str(final_code)
            return True
        return False
