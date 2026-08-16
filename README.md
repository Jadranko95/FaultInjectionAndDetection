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