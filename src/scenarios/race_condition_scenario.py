import sys
import threading
import time
from typing import Any

from .fault_scenario import FaultScenario


class RaceConditionScenario(FaultScenario):
    """
    Class for managing scenarios of the RaceCondition class.

    Scenario: Many threads modify the same variable (counter) without synchronization.
    In Python the operation '+=' is not fully atomic, it contains bytecode instructions.
    Symptom: The counter value is non-deterministic.
    """

    def __init__(self, threads_count: int, increments_per_thread: int) -> None:
        self.threads_count = threads_count
        self.increments_per_thread = increments_per_thread
        self.lock = threading.Lock()
        self.counter = 0

    def _worker(self, buggy: bool, barrier: threading.Barrier) -> None:
        barrier.wait()

        for _ in range(self.increments_per_thread):
            if buggy:
                temp = self.counter
                time.sleep(0.00001)
                temp += 1
                self.counter = temp
            else:
                with self.lock:
                    self.counter += 1

    def run(self, buggy: bool) -> Any:
        self.counter = 0
        threads = []
        barrier = threading.Barrier(self.threads_count)

        old_interval = sys.getswitchinterval()
        sys.setswitchinterval(0.000001)

        try:
            for _ in range(self.threads_count):
                thread = threading.Thread(target=self._worker, args=(buggy, barrier,))
                threads.append(thread)
                thread.start()

            for thread in threads:
                thread.join()
        finally:
            sys.setswitchinterval(old_interval)

        return self.counter
