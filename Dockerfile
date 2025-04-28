FROM python:3.11-slim-buster

WORKDIR /app

# Create a non-root user
RUN adduser --disabled-password --gecos "" appuser

# Change ownership of /app to appuser
RUN chown -R appuser:appuser /app

# Set the user for subsequent commands
USER appuser

# Create and activate a virtual environment
RUN python -m venv venv
RUN . venv/bin/activate && python -m pip install -U pip

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY pyproject.toml setup.py setup.cfg README.md ./
RUN pip install -e .

COPY waveload /app/waveload

RUN pip install pytest pytest-cov pylint

ENTRYPOINT ["python"]
CMD ["-m", "waveload"]
