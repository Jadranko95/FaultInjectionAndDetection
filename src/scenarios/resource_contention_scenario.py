import threading
import time
from typing import Any

from .fault_scenario import FaultScenario


class ResourceContentionScenario(FaultScenario):
    """
    Resource Contention: Severe latency degrade caused by holding a coarse-grained lock
    during long-running, non-critical operations (e.g., I/O or heavy computation).

    Root Cause:
    Holding a shared lock while performing time-consuming tasks (simulated I/O) forces
    all threads to queue up and execute sequentially instead of concurrently.

    Symptom:
    Extreme thread contention, high latency, and severe performance drop where N threads
    take N times longer than a single thread execution.
    """

    def __init__(
        self, threads_count: int = 10, task_duration: float = 0.05
    ) -> None:
        self.threads_count = threads_count
        self.task_duration = task_duration
        self.processed_items = 0
        self.lock = threading.Lock()

    @staticmethod
    def _simulate_io_bound_work() -> int:
        """Simulate slow external resource access or computation."""
        time.sleep(0.05)
        return 42

    def _worker(self, buggy: bool) -> None:
        if buggy:
            # BUGGY VERSION: Holding the lock across the entire long-running operation.
            # Forces sequential execution of all threads.
            with self.lock:
                result = self._simulate_io_bound_work()
                self.processed_items += result
        else:
            # FIXED VERSION: Minimize critical section duration.
            # Perform slow I/O out-of-lock, acquire lock ONLY to update shared state.
            result = self._simulate_io_bound_work()
            with self.lock:
                self.processed_items += result

    def run(self, buggy: bool) -> float:
        """
        Executes the scenario and returns total elapsed execution time in seconds.

        :param buggy: If True, uses coarse-grained locking. If False, uses minimal critical section.
        :return: Execution time in seconds.
        """
        self.processed_items = 0
        threads = []

        start_time = time.perf_counter()

        for _ in range(self.threads_count):
            thread = threading.Thread(
                target=self._worker, args=(buggy,), daemon=True
            )
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        elapsed_time = time.perf_counter() - start_time
        return elapsed_time