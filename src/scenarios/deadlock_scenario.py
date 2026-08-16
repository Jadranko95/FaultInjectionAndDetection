import sys
import threading
import time
import traceback
from dataclasses import dataclass, field

from .fault_scenario import FaultScenario


@dataclass
class Account:
    id: int
    balance: float
    lock: threading.Lock = field(default_factory=threading.Lock, repr=False)


class DeadlockScenario(FaultScenario):
    """
    Deadlock: Classic circular-wait deadlock via inconsistent lock ordering.

    Root Cause:
    Two threads attempt to acquire locks on the same two resources (Account A and Account B),
    but acquire them in reverse order.
    Thread 1 locks Account A and waits for B. Simultaneously, Thread 2 locked Account B
    and waits for A. This creates a circular wait condition from which neither thread can exit.

    Symptom:
    The application hangs indefinitely, and threads remain stuck waiting for lock acquisition.
    """

    def __init__(self, timeout_seconds: float = 1.0):
        self.timeout_seconds = timeout_seconds
        self.acc_a = Account(id=1, balance=1000.0)
        self.acc_b = Account(id=2, balance=1000.0)

    @staticmethod
    def _dump_thread_stacks():
        current_thread_id = threading.get_ident()
        print("\n🚨 [DEADLOCK DETECTED] Thread Stack Dump:")

        for thread_id, frame in sys._current_frames().items():
            if thread_id == current_thread_id:
                continue

            print(f"\n--- Thread ID: {thread_id} ---")
            stack_trace = "".join(traceback.format_stack(frame)).strip()
            print(stack_trace if stack_trace else "  (No stack trace available)")

    @staticmethod
    def _transfer(from_acc: Account, to_acc: Account, amount: float, buggy: bool):
        if buggy:
            with from_acc.lock:
                time.sleep(0.01)
                with to_acc.lock:
                    from_acc.balance -= amount
                    to_acc.balance += amount
        else:
            # Block account with lower ID
            first_acc, second_acc = (
                (from_acc, to_acc) if from_acc.id < to_acc.id else (to_acc, from_acc)
            )

            with first_acc.lock:
                with second_acc.lock:
                    from_acc.balance -= amount
                    to_acc.balance += amount

    def run(self, buggy: bool) -> bool:
        """
        Executes bank transfers across two separate threads.

        :param buggy: If True, uses inconsistent lock ordering. If False, uses ordered locks.
        :return: True if transfers completed successfully, False if a deadlock occurred (timeout).
        """

        self.acc_a.balance = 1000.0
        self.acc_b.balance = 1000.0

        t1 = threading.Thread(
            target=self._transfer,
            args=(self.acc_a, self.acc_b, 100.0, buggy),
            daemon=True,
        )
        t2 = threading.Thread(
            target=self._transfer,
            args=(self.acc_b, self.acc_a, 50.0, buggy),
            daemon=True,
        )

        t1.start()
        t2.start()

        t1.join(timeout=self.timeout_seconds)
        t2.join(timeout=self.timeout_seconds)

        is_deadlocked = t1.is_alive() or t2.is_alive()

        if is_deadlocked:
            self._dump_thread_stacks()

        return not is_deadlocked
