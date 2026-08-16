import pytest
from hamcrest import less_than, assert_that, greater_than_or_equal_to

from src.scenarios.resource_contention_scenario import ResourceContentionScenario


class TestResourceContentionScenario:
    @pytest.fixture
    def scenario(self):
        # 10 threads, each doing 0.05s of I/O work
        # Sequential execution = ~0.50s | Parallel execution = ~0.05s-0.10s
        return ResourceContentionScenario(threads_count=10, task_duration=0.05)

    def test_fixed_implementation_runs_concurrently(self, scenario):
        """
        Verifies that minimal lock scoping allows true concurrency.
        Execution time should be significantly lower than sequential processing.
        """
        elapsed_time = scenario.run(buggy=False)

        # Expected execution time should be close to a single task duration (~0.05s - 0.15s)
        # We assert it finishes in less than half of sequential time (< 0.25s)
        max_acceptable_time = (scenario.threads_count * scenario.task_duration) / 2
        assert_that(
            elapsed_time,
            less_than(max_acceptable_time),
            f"Optimized execution was too slow: {elapsed_time:.2f}s",
        )

    def test_buggy_implementation_exhibits_lock_contention(self, scenario):
        """
        Verifies that coarse lock scoping causes contention and forces sequential execution.
        """
        elapsed_time = scenario.run(buggy=True)

        # Buggy execution forces threads to queue up sequentially (>= 0.50s)
        min_expected_time = scenario.threads_count * scenario.task_duration * 0.8
        assert_that(
            elapsed_time,
            greater_than_or_equal_to(min_expected_time),
            f"Buggy version did not exhibit contention: {elapsed_time:.2f}s",
        )
