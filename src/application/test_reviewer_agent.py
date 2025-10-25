from src.domain.state import State


class TestReviewer:
    def __init__(self, agent):
        self.agent = agent

    def respond(self, state: State):
        prompt = f'Código: "{state.code}".\n Código de teste gerado: "{state.test_generator_response}".\n Estratégias de teste: "{state.test_strategist_response}".\n Cobertura de teste: "{state.coverage_agent_response}".\n Resultados da execução dos testes: "{state.test_executor_response}".\n'
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
        return {"test_reviewer_response": content}

    def hasFinalCode(self, state: State) -> bool:
        review = state.test_reviewer_response
        final_code = review.get("final_code")
        if final_code:
            state.final_code = str(final_code)
            return True
        return False
