from hamcrest import assert_that, equal_to, less_than

import pytest
from src.scenarios.race_condition_scenario import RaceConditionScenario


class TestRaceConditionScenario:

    @pytest.fixture
    def scenario(self):
        return RaceConditionScenario(threads_count=10, increments_per_thread=100000)

    def test_positive_scenario(self, scenario: RaceConditionScenario):
        expected = scenario.threads_count * scenario.increments_per_thread

        for _ in range(4):
            actual = scenario.run(buggy=False)
            assert_that(actual, equal_to(expected))

    def test_buggy_scenario(self, scenario: RaceConditionScenario):
        expected = scenario.threads_count * scenario.increments_per_thread
        actual = scenario.run(buggy=True)

        assert_that(actual, less_than(expected))
