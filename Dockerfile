# Stage 1: Builder image for compiling and building
FROM python:3.11-slim-buster AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /venv

# Activate virtual environment
ENV PATH="/venv/bin:$PATH"

# Install pip and upgrade
RUN pip install --upgrade pip

# Install testing, coverage, linting, and formatting tools
RUN pip install pytest pytest-cov coverage pylint autopep8

# Copy project files (excluding tests)
COPY requirements.txt .
COPY pyproject.toml setup.py setup.cfg README.md ./
COPY waveload /app/waveload

# Run linting only on the waveload directory
RUN pylint waveload

# Run code formatting (apply changes directly to all .py files in waveload)
RUN find /app/waveload -name "*.py" -exec autopep8 --in-place {} +

# Install your module in editable mode
RUN pip install -e .

# Copy the tests directory for running tests
COPY tests /app/tests

# Run tests and generate reports
RUN pytest --cov=waveload --cov-report=xml:/app/coverage.xml --junitxml=/app/test_results.xml /app/tests

# Stage 2: Final minimal Alpine image
FROM python:3.11-alpine3.19 AS final

WORKDIR /app

# Install minimal runtime dependencies
RUN apk add --no-cache libffi-dev openssl

# Copy virtual environment from the builder stage
COPY --from=builder /venv /venv
ENV PATH="/venv/bin:$PATH"

# Copy only the application code (waveload) from the builder stage
COPY --from=builder /app/waveload /app/waveload

ENTRYPOINT ["python"]
CMD ["-m", "waveload"]
