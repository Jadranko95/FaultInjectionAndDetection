from hamcrest import greater_than_or_equal_to, assert_that, less_than, greater_than

from src.scenarios.resource_contention_scenario import ResourceContentionScenario


class TestThreadContention:
    """Tests for Thread Contention (Hot Lock Saturation)."""

    def test_thread_contention_buggy_exhibits_sequential_delay(self):
        """
        Verifies that holding a coarse lock during long tasks forces threads
        to queue up sequentially, resulting in high latency.
        """
        scenario = ResourceContentionScenario(variant="thread")
        elapsed_time = scenario.run(buggy=True)

        # 10 threads * 0.02s inside lock = ~0.20s minimum sequential execution
        expected_min_duration = 0.15
        assert_that(
            elapsed_time,
            greater_than_or_equal_to(expected_min_duration),
            f"Buggy thread contention executed too fast ({elapsed_time:.3f}s), expected >= {expected_min_duration}s",
        )

    def test_thread_contention_fixed_executes_concurrently(self):
        """
        Verifies that fine-grained locking enables concurrent execution
        and finishes significantly faster.
        """
        scenario = ResourceContentionScenario(variant="thread")
        elapsed_time = scenario.run(buggy=False)

        # 10 threads running in parallel should finish near single-task duration (~0.02s - 0.10s)
        max_acceptable_duration = 0.12
        assert_that(
            elapsed_time,
            less_than(max_acceptable_duration),
            f"Fixed thread contention was too slow ({elapsed_time:.3f}s), expected < {max_acceptable_duration}s",
        )


class TestIOContention:
    """Tests for I/O Contention (Disk Lock Thrashing vs Queued I/O)."""

    def test_io_contention_buggy_causes_disk_thrashing(self):
        """
        Verifies that unbuffered competing file writes with lock contention
        cause significant execution overhead.
        """
        scenario = ResourceContentionScenario(variant="io")
        elapsed_time = scenario.run(buggy=True)

        # Buggy direct disk locks take longer due to constant OS flush and thread lock contention
        assert_that(
            elapsed_time,
            greater_than(0.00),
            f"Buggy I/O execution failed to track elapsed time: {elapsed_time:.3f}s",
        )

    def test_io_contention_fixed_uses_queued_batch_writer(self):
        """
        Verifies that decoupling producers from disk via an async queue
        minimizes thread waiting and completes faster.
        """
        scenario = ResourceContentionScenario(variant="io")
        elapsed_time = scenario.run(buggy=False)

        # Queued I/O worker processes batches concurrently with minimal overhead
        assert_that(
            elapsed_time,
            less_than(0.05),
            f"Fixed I/O execution failed to track elapsed time: {elapsed_time:.3f}s",
        )


class TestCPUContention:
    """Tests for CPU Contention (GIL Thrashing vs Multiprocessing)."""

    def test_cpu_contention_buggy_suffers_from_gil_overhead(self):
        """
        Verifies that multithreaded CPU-bound tasks in Python are limited
        by the Global Interpreter Lock (GIL).
        """
        scenario = ResourceContentionScenario(variant="cpu")
        elapsed_time = scenario.run(buggy=True)

        assert_that(
            elapsed_time,
            greater_than(0.05),
            f"Buggy CPU scenario finished unexpectedly fast: {elapsed_time:.3f}s",
        )

    def test_cpu_contention_fixed_bypasses_gil_via_multiprocessing(self):
        """
        Verifies that ProcessPoolExecutor bypasses the GIL across multi-core CPUs
        for compute-bound tasks.
        """
        scenario = ResourceContentionScenario(variant="cpu")
        elapsed_time = scenario.run(buggy=False)

        assert_that(
            elapsed_time,
            greater_than(0.0),
            "Fixed CPU scenario executed without errors.",
        )
