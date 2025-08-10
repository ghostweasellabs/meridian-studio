FROM python:3.11-slim
WORKDIR /app

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl && rm -rf /var/lib/apt/lists/*

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:${PATH}"

# Copy backend code
COPY . /app

# Create venv and install
RUN uv venv && . .venv/bin/activate && uv pip install -e .

EXPOSE 8000
CMD ["sh", "-lc", ". .venv/bin/activate && uvicorn app.main:app --host 0.0.0.0 --port 8000"]


