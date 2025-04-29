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

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY pyproject.toml setup.py setup.cfg README.md ./
RUN pip install -e .

COPY waveload /app/waveload

# Install pytest and coverage for testing
RUN pip install pytest pytest-cov coverage

# Run tests and generate coverage report
RUN pytest --cov=waveload \
	  --cov-report=xml:/app/coverage.xml \
		--junitxml=/app/test_results.xml \
		/app/waveload/tests

# Stage 2: Final minimal Alpine image
FROM python:3.11-alpine3.19 AS final

WORKDIR /app

# Install minimal runtime dependencies
RUN apk add --no-cache libffi-dev openssl

# Copy virtual environment from the builder stage
COPY --from=builder /venv /venv
ENV PATH="/venv/bin:$PATH"

# Copy the application code from the builder stage
COPY --from=builder /app/waveload /app/waveload

ENTRYPOINT ["python"]
CMD ["-m", "waveload"]
