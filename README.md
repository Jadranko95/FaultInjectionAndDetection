# ⚡ Concurrency Fault Injection & Detection Engine

[![CI/CD Pipeline](https://github.com/YOUR_USERNAME/YOUR_REPO_NAME/actions/workflows/test.yml/badge.svg)](https://github.com/YOUR_USERNAME/YOUR_REPO_NAME/actions)
![Python Version](https://img.shields.io/badge/python-3.13-blue.svg)
![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

A production-grade Python framework designed to simulate, detect, and remediate fundamental multithreading concurrency faults. This project demonstrates real-world concurrent execution bugs, thread liveness issues, performance bottlenecks, and deterministic unit testing in Python 3.13.

---

## 🎯 Architectural Overview & Scenarios

The engine implements three classical concurrent computing bug patterns, providing both a **buggy** (faulty) and a **fixed** (remediated) execution mode for each scenario:

| Scenario | Variant | Root Cause | Expected Symptom | Remediation Pattern | CLI Command |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Race Condition** | Default | Unsynchronized concurrent state mutation of shared memory without atomic guards. | Data corruption & lost updates under high thread volume. | Mutual exclusion locking via `threading.Lock`. | `python -m src.main race --buggy` |
| **Deadlock** | Default | Inconsistent lock acquisition order across threads accessing multiple resources. | Indefinite thread hanging / system Liveness failure. | **Global Lock Acquisition Ordering** by unique resource ID. | `python -m src.main deadlock --buggy` |
| **Resource Contention** | `thread` | Over-scoped lock holding synchronization during long-running work/sleep. | Lock saturation & severe request latency ($O(N)$ sequential delay). | **Fine-grained locking** (minimal critical section). | `python -m src.main contention --variant thread --buggy` |
| **Resource Contention** | `io` | Unbuffered concurrent disk file access with forced OS flushes per thread. | Disk I/O thrashing, high system write overhead & latency spikes. | **Producer-Consumer Pattern** with background worker and async `Queue`. | `python -m src.main contention --variant io --buggy` |
| **Resource Contention** | `cpu` | Multithreaded execution of CPU-bound operations bound by Python's GIL. | Context switching overhead & CPU core underutilization. | **Process Pool Execution** (`ProcessPoolExecutor`) bypassing the GIL. | `python -m src.main contention --variant cpu --buggy` |
---

---

## 🔬 Analysis Methods & Diagnostic Tools

This framework integrates specialized diagnostics for each concurrency fault type:

* 💥 **Race Conditions / Data Hazards:**
  * **Deterministic Scheduling:** Uses `threading.Barrier` to synchronize all worker threads, releasing them simultaneously at the exact same instant to reliably trigger race conditions.
  * **Stress Testing:** Configurable thread volume (`--threads`) and iteration counts (`--increments`).

* 🔒 **Deadlocks:**
  * **Timeout Watchdog:** Prevents permanent pipeline hanging by interrupting blocked threads after a configured threshold (`--timeout`).
  * **Thread Dump / Stack Analysis:** Captures and prints stack traces (`sys._current_frames()`) for all running threads upon deadlock detection to pinpoint exact lock acquisition sites.
  * **Lock-Order Validation:** Enforces strict global lock sorting (`sorted([res1, res2], key=lambda r: r.id)`).

* ⚡ **Resource Contention:**
  * **Built-in Profiler:** Enable `cProfile` performance analysis via the `--profile` flag to inspect top cumulative execution calls and lock waiting times.
  * **Latency & Throughput Benchmarking:** Precise high-resolution timing (`time.perf_counter()`) measuring execution duration across variants.
  * **Load Generators:** Adjustable thread counts and write iterations (`--variant [thread|io|cpu]`).

* 🧪 **Regression Detection:**
  * **Automated CI Integration:** Pre-configured GitHub Actions workflow executing Pytest suites on every push/PR.
  * **Baselines & Thresholds:** Isolated unit tests covering both buggy and fixed execution paths with precise timing assertions.

---

## 🛠 Tech Stack & Tools

* **Language:** Python 3.13
* **Dependency Management:** Pipenv (`Pipfile` / `Pipfile.lock`)
* **Testing & Coverage:** `pytest`, `pytest-cov`
* **Code Formatting & Quality:** `black`, PEP8 compliance
* **Containerization:** Multi-stage `Dockerfile`, `docker-compose`
* **CI/CD:** GitHub Actions (Automated Linting, Testing, Markdown Coverage Summaries, and Docker Builds)

---

## 🚀 Quick Start (Local Setup)

### Prerequisites
* Python 3.13+
* Pipenv (`pip install pipenv`)

### 1. Installation
Clone the repository and install all dependencies (including developer tools):

```bash
git clone [https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git](https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git)
cd YOUR_REPO_NAME

pipenv install --dev
```

### 2. Running Tests & Coverage

Run the test suite inside the Pipenv virtual environment:

```bash
# Run all unit tests
pipenv run pytest -v

# Run tests with code coverage output
pipenv run pytest --cov=src --cov-report=term-missing
```

### 3. CLI Usage

Execute scenarios directly via the Command Line Interface (src/main.py):

```bash
# 1. Race Condition (with deterministic Barrier scheduling)
PYTHONPATH=. python -m src.main race --buggy --threads 10 --increments 1000
PYTHONPATH=. python -m src.main race --threads 10 --increments 1000

# 2. Deadlock (with Watchdog & Stack Trace Dump)
PYTHONPATH=. python -m src.main deadlock --buggy --timeout 0.5
PYTHONPATH=. python -m src.main deadlock

# 3. Resource Contention - Thread (Hot Lock Saturation)
PYTHONPATH=. python -m src.main contention --variant thread --buggy --profile
PYTHONPATH=. python -m src.main contention --variant thread

# 4. Resource Contention - I/O (Disk Thrashing)
PYTHONPATH=. python -m src.main contention --variant io --buggy
PYTHONPATH=. python -m src.main contention --variant io

# 5. Resource Contention - CPU (GIL Thrashing)
PYTHONPATH=. python -m src.main contention --variant cpu --buggy --profile
PYTHONPATH=. python -m src.main contention --variant cpu
```

## 🐳 Running with Docker & Docker Compose

No local Python installation required. The application and test suite are fully containerized using a multi-stage Dockerfile.

```bash
# Run the Pytest suite in an isolated container
docker compose run --rm test

# Run CLI scenarios via Docker Compose
docker compose run --rm app race --buggy
docker compose run --rm app deadlock --buggy --timeout 0.5
docker compose run --rm app contention --variant thread --buggy --profile
```

## ⚙️ CI/CD Pipeline Architecture

Automated checks run on every push and pull_request via GitHub Actions (.github/workflows/test.yml):

1. Code Formatting: Validated via black --check.

2. Unit Tests: Verified via pytest with automatic Step Summary markdown reports.

3. Docker Build: Verifies containerization integrity.

## 📁 Repository Structure

```text
.
├── .github/
│   └── workflows/
│       └── test.yml          # GitHub Actions CI/CD pipeline
├── src/
│   ├── scenarios/            # Concurrency fault implementations
│   │   ├── fault_scenario.py # Abstract base class
│   │   ├── race_condition_scenario.py
│   │   ├── deadlock_scenario.py
│   │   └── resource_contention_scenario.py
│   └── main.py               # CLI Application entry point
├── tests/                    # Pytest test suites
│   ├── test_race_condition.py
│   ├── test_deadlock.py
│   └── test_resource_contention.py
├── Dockerfile                # Multi-stage Docker configuration
├── docker-compose.yml        # Orchestration for app and test services
├── Pipfile                   # Pipenv dependency declaration
├── Pipfile.lock              # Frozen dependency tree
├── pytest.ini                # Pytest configuration
└── README.md
```
