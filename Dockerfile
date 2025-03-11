FROM python:3.12-slim

ARG template=${template}

# Install uv
COPY --from=ghcr.io/astral-sh/uv:0.5.29 /uv /uvx /bin/

# Install build dependencies and uv
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy the project into the image
ADD templates/${template} /app

# Copy any common files
COPY pyproject.toml /app/pyproject.toml
COPY uv.lock /app/uv.lock

# Sync the project into a new environment, using the frozen lockfile
RUN uv sync --frozen

EXPOSE 21120

CMD ["uv", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "21120", "--reload"]
