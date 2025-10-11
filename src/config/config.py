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
        self.performance_agent = (
            os.getenv("PERFORMANCE_AGENT_ENDPOINT"),
            os.getenv("PERFORMANCE_AGENT_API_KEY"),
        )
        self.quality_agent = (
            os.getenv("QUALITY_AGENT_ENDPOINT"),
            os.getenv("QUALITY_AGENT_API_KEY"),
        )
        self.unit_test_agent = (
            os.getenv("UNIT_TEST_AGENT_ENDPOINT"),
            os.getenv("UNIT_TEST_AGENT_API_KEY"),
        )