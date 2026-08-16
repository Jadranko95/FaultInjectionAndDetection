import concurrent.futures
import math
import os
import queue
import tempfile
import threading
import time

from .fault_scenario import FaultScenario


def _cpu_heavy_task(n: int = 10_000_000) -> float:
    """CPU-bound task: Calculate prime/square root sums."""
    return sum(math.sqrt(i) for i in range(n))


class ResourceContentionScenario(FaultScenario):
    """
    Resource Contention Engine covering 3 distinct variants:
    1. Thread Contention: Heavy lock saturation/over-contention vs fine-grained locking.
    2. I/O Contention: Direct concurrent unbuffered disk access vs Queued/Batched I/O.
    3. CPU Contention: Multi-threaded CPU-bound work (GIL thrashing) vs Multiprocessing.
    """

    def __init__(self, variant: str = "thread") -> None:
        if variant not in ("thread", "io", "cpu"):
            raise ValueError("Variant must be one of: 'thread', 'io', 'cpu'")
        self.variant = variant

    # ------------------------------------------------------------------
    # VARIANT 1: Thread Contention (Hot Lock Saturation)
    # ------------------------------------------------------------------
    @staticmethod
    def _run_thread_contention(buggy: bool) -> float:
        threads_count = 10
        lock = threading.Lock()
        counter = 0

        def worker():
            nonlocal counter
            if buggy:
                # BUGGY: Coarse lock held during simulated I/O / work
                with lock:
                    time.sleep(0.02)
                    counter += 1
            else:
                # FIXED: Fine-grained lock scope
                time.sleep(0.02)
                with lock:
                    counter += 1

        start_time = time.perf_counter()
        threads = [
            threading.Thread(target=worker, daemon=True) for _ in range(threads_count)
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        return time.perf_counter() - start_time

    # ------------------------------------------------------------------
    # VARIANT 2: I/O Contention (Disk I/O Thrashing)
    # ------------------------------------------------------------------
    @staticmethod
    def _run_io_contention(buggy: bool) -> float:
        threads_count = 20
        iterations = 200

        with tempfile.NamedTemporaryFile(mode="w+", delete=False) as tmp_file:
            file_path = tmp_file.name

        start_time = time.perf_counter()

        if buggy:
            # BUGGY: Competing threads opening, writing, and flushing to disk directly
            file_lock = threading.Lock()

            def io_worker(thread_id: int):
                for i in range(iterations):
                    with file_lock:
                        with open(file_path, "a") as f:
                            f.write(f"Thread-{thread_id} line {i}\n")
                            f.flush()  # Force OS disk flush

            threads = [
                threading.Thread(target=io_worker, args=(i,), daemon=True)
                for i in range(threads_count)
            ]
            for t in threads:
                t.start()
            for t in threads:
                t.join()

        else:
            # FIXED: Single dedicated I/O background worker consuming from Queue
            io_queue = queue.Queue()

            def disk_writer():
                with open(file_path, "a") as f:
                    while True:
                        item = io_queue.get()
                        if item is None:
                            break
                        f.write(item)
                        io_queue.task_done()

            writer_thread = threading.Thread(target=disk_writer, daemon=True)
            writer_thread.start()

            def producer_worker(thread_id: int):
                for i in range(iterations):
                    io_queue.put(f"Thread-{thread_id} line {i}\n")

            producers = [
                threading.Thread(target=producer_worker, args=(i,), daemon=True)
                for i in range(threads_count)
            ]
            for p in producers:
                p.start()
            for p in producers:
                p.join()

            io_queue.put(None)  # Sentinel to stop writer
            writer_thread.join()

        if os.path.exists(file_path):
            os.remove(file_path)

        return time.perf_counter() - start_time

    # ------------------------------------------------------------------
    # VARIANT 3: CPU Contention (GIL Thrashing vs Multiprocessing)
    # ------------------------------------------------------------------
    @staticmethod
    def _run_cpu_contention(buggy: bool) -> float:
        tasks = [3_000_000] * 4
        start_time = time.perf_counter()

        if buggy:
            # BUGGY: Using threading for CPU-bound tasks causes GIL contention overhead
            threads = [
                threading.Thread(target=_cpu_heavy_task, args=(n,), daemon=True)
                for n in tasks
            ]
            for t in threads:
                t.start()
            for t in threads:
                t.join()
        else:
            # FIXED: Bypassing GIL using ProcessPoolExecutor across multicore CPUs
            with concurrent.futures.ProcessPoolExecutor(
                max_workers=os.cpu_count()
            ) as executor:
                list(executor.map(_cpu_heavy_task, tasks))

        return time.perf_counter() - start_time

    def run(self, buggy: bool) -> float:
        if self.variant == "thread":
            return self._run_thread_contention(buggy)
        elif self.variant == "io":
            return self._run_io_contention(buggy)
        elif self.variant == "cpu":
            return self._run_cpu_contention(buggy)
        return 0.0
