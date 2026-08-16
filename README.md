# ⚡ Concurrency Fault Injection & Detection Engine

[![CI/CD Pipeline](https://github.com/YOUR_USERNAME/YOUR_REPO_NAME/actions/workflows/test.yml/badge.svg)](https://github.com/YOUR_USERNAME/YOUR_REPO_NAME/actions)
![Python Version](https://img.shields.io/badge/python-3.13-blue.svg)
![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

A production-grade Python framework designed to simulate, detect, and remediate fundamental multithreading concurrency faults. This project demonstrates real-world concurrent execution bugs, thread liveness issues, performance bottlenecks, and deterministic unit testing in Python 3.13.

---

## 🎯 Architectural Overview & Scenarios

The engine implements three classical concurrent computing bug patterns, providing both a **buggy** (faulty) and a **fixed** (remediated) execution mode for each scenario:

| Scenario | Root Cause | Symptom | Remediation Pattern |
| :--- | :--- | :--- | :--- |
| **1. Race Condition** | Unsynchronized concurrent mutation of shared memory. | Data corruption / lost updates. | Synchronized execution via `threading.Lock`. |
| **2. Deadlock** | Circular wait condition caused by inconsistent lock acquisition order across threads. | Indefinite execution freeze / thread hang. | **Global Lock Acquisition Ordering** by resource unique ID. |
| **3. Resource Contention** | Coarse-grained lock scoping holding locks during long-running I/O tasks. | Lock saturation & high latency ($O(N)$ sequential delay). | **Minimal Critical Sections** (fine-grained lock scoping). |

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
# Race Condition: Observe lost updates
pipenv run python -m src.main race --buggy --threads 10 --increments 1000
pipenv run python -m src.main race --threads 10 --increments 1000

# Deadlock: Observe thread deadlock timeout vs. ordered execution
pipenv run python -m src.main deadlock --buggy --timeout 0.5
pipenv run python -m src.main deadlock

# Resource Contention: Measure latency difference between coarse vs fine locks
pipenv run python -m src.main contention --buggy --threads 10
pipenv run python -m src.main contention --threads 10
```

## 🐳 Running with Docker & Docker Compose

No local Python installation required. The application and test suite are fully containerized using a multi-stage Dockerfile.

```bash
# Run the Pytest suite in an isolated container
docker compose run --rm test

# Run CLI scenarios via Docker Compose
docker compose run --rm app race --buggy
docker compose run --rm app deadlock --buggy --timeout 0.5
docker compose run --rm app contention --buggy
```

## ⚙️ CI/CD Pipeline Architecture

Every push and pull_request triggers an automated GitHub Actions workflow (.github/workflows/test.yml) executing two sequential jobs:

```bash
[ Git Push ] ──► Job 1: Code Quality (Black Check) ──► Job 2: Pytest Suite & Coverage Report ──► Docker Build Verification
```

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
