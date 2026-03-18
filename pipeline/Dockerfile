# Start with slim Python 3.13 image
FROM python:3.13.11-slim

# Copy uv binary from official uv image (multi-stage build pattern)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

# Set a current working directory
WORKDIR /code

# Add virtual environment to PATH so we can use installed packages
ENV PATH="/code/.venv/bin:$PATH"

# Copy dependency files first (better layer caching) in the cwd
COPY "pyproject.toml" "uv.lock" ".python-version" ./

# Install dependencies from the uv.lock file (ensures reproductible builds)
RUN uv sync --locked

# Copy application code
COPY pipeline.py .

# Set entry point 
ENTRYPOINT ["python", "pipeline.py"]