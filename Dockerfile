FROM python:3.12-slim

# UV_NO_SYNC: deps are synced at build time; otherwise `uv run` installs the project itself on every start.
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    TZ=Europe/Kyiv \
    UV_NO_SYNC=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends tzdata \
    && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Install dependencies before copying app code so this layer is cached
# independently and only rebuilds when pyproject.toml or uv.lock changes.
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

# links.json is optional and gitignored: the [n] glob lets the build pass without it.
COPY main.py links.jso[n] ./
COPY bot ./bot
COPY locales ./locales

CMD ["uv", "run", "python", "main.py"]
