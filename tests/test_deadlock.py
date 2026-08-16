import pytest
from hamcrest import assert_that, equal_to

from src.scenarios.deadlock_scenario import DeadlockScenario


class TestDeadlockScenario:
    @pytest.fixture
    def scenario(self):
        return DeadlockScenario(timeout_seconds=0.5)

    def test_fixed_implementation_completes_without_deadlock(self, scenario):
        """
        Verifies that the fixed implementation (buggy=False) completes successfully
        without deadlocking threads.
        """
        success = scenario.run(buggy=False)
        assert_that(success, equal_to(True))
        assert_that(scenario.acc_a.balance, equal_to(950.0))
        assert_that(scenario.acc_b.balance, equal_to(1050.0))

    def test_buggy_implementation_causes_deadlock(self, scenario):
        """
        Verifies that the buggy implementation (buggy=True) triggers a deadlock
        (threads remain alive after timeout).
        """
        success = scenario.run(buggy=True)
        assert_that(success, equal_to(False))
