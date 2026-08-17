import threading
import time

from .fault_scenario import FaultScenario


class RaceConditionScenario(FaultScenario):
    """
    Class for managing scenarios of the RaceCondition class.

    Scenario: Many threads modify the same variable (counter) without synchronization.
    Symptom: The counter value is non-deterministic.
    """

    def __init__(self, threads_count: int, increments_per_thread: int) -> None:
        self.threads_count = threads_count
        self.increments_per_thread = increments_per_thread
        self.lock = threading.Lock()
        self.counter = 0
        self.barrier = None

    def _buggy_worker(self):
        if self.barrier:
            self.barrier.wait()

        for _ in range(self.increments_per_thread):
            temp = self.counter
            time.sleep(0)
            self.counter = temp + 1

    def _fixed_worker(self):
        if self.barrier:
            self.barrier.wait()

        for _ in range(self.increments_per_thread):
            with self.lock:
                self.counter += 1

    def run(self, buggy: bool = True) -> int:
        self.counter = 0
        threads = []

        self.barrier = threading.Barrier(self.threads_count)

        worker = self._buggy_worker if buggy else self._fixed_worker

        for _ in range(self.threads_count):
            t = threading.Thread(target=worker)
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        return self.counter
