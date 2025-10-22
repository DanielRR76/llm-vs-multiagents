# src/infrastructure/config.py
import os

from dotenv import load_dotenv


class Config:
    def __init__(self):
        load_dotenv()
        self.coverage_agent = (
            os.getenv("COVERAGE_AGENT_ENDPOINT"),
            os.getenv("COVERAGE_AGENT_API_KEY"),
        )
        self.mutation_test_agent = (
            os.getenv("MUTATION_TEST_AGENT_ENDPOINT"),
            os.getenv("MUTATION_TEST_AGENT_API_KEY"),
        )
        self.quality_agent = (
            os.getenv("QUALITY_AGENT_ENDPOINT"),
            os.getenv("QUALITY_AGENT_API_KEY"),
        )
        self.unit_test_agent = (
            os.getenv("UNIT_TEST_AGENT_ENDPOINT"),
            os.getenv("UNIT_TEST_AGENT_API_KEY"),
        )
        self.code_analyzer_agent = (
            os.getenv("CODE_ANALYZER_AGENT_ENDPOINT"),
            os.getenv("CODE_ANALYZER_AGENT_API_KEY"),
        )
        self.test_strategist_agent = (
            os.getenv("TEST_STRATEGIST_AGENT_ENDPOINT"),
            os.getenv("TEST_STRATEGIST_AGENT_API_KEY"),
        )
