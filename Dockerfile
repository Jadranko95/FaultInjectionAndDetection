# ==========================================
# STAGE 1: Builder
# ==========================================
FROM python:3.13-slim AS builder

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIPENV_VENV_IN_PROJECT=1

WORKDIR /app

RUN pip install --no-cache-dir pipenv

COPY Pipfile Pipfile.lock ./
RUN pipenv install --dev

# ==========================================
# STAGE 2: Runtime
# ==========================================
FROM python:3.13-slim AS runtime

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/app/.venv/bin:$PATH" \
    PYTHONPATH="/app"

WORKDIR /app

# Kopiujemy gotowe wirtualne środowisko z fazy builder
COPY --from=builder /app/.venv /app/.venv

# Kopiujemy kod źródłowy oraz testy
COPY src/ ./src
COPY tests/ ./tests
COPY pytest.ini ./

# Domyślny punkt wejścia - aplikacja CLI
ENTRYPOINT ["python", "-m", "src.main"]
CMD ["--help"]
