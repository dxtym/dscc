FROM python:3.12-slim AS builder

WORKDIR /app
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-dev --no-install-project

FROM python:3.12-slim AS runtime

RUN useradd --no-create-home --shell /bin/false app

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv

COPY --chown=app:app . .

RUN chmod +x entrypoint.sh && \
    mkdir -p /app/staticfiles /app/media && \
    chown -R app:app /app/staticfiles /app/media

USER app

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=shop.settings

EXPOSE 8000

CMD ["./entrypoint.sh"]
