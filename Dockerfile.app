# FROM --platform=$TARGETPLATFORM python:3.11-slim-buster AS builder
FROM --platform=linux/amd64 python:3.11-slim-buster AS builder

RUN groupadd -r ai4b_group && useradd -r -g ai4b_group ai4b_user

WORKDIR /app

RUN pip install --no-cache-dir poetry
RUN python -m venv /app/.venv
ENV VIRTUAL_ENV=/app/.venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY poetry.lock pyproject.toml ./

RUN poetry install --no-root --no-interaction --only main

RUN chown -R ai4b_user:ai4b_group /app



FROM --platform=linux/amd64 python:3.11-slim-buster AS runtime

RUN groupadd -r ai4b_group && useradd -r -g ai4b_group ai4b_user

ENV ENV="dev"

WORKDIR /app

COPY --from=builder /app /app

COPY configs ./configs
COPY . .

RUN chown -R ai4b_user:ai4b_group /app

ENV VIRTUAL_ENV=/app/.venv
ENV PATH="/app/.venv/bin:$PATH"

USER ai4b_user

EXPOSE 8000

CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]

HEALTHCHECK --interval=30s --timeout=10s --retries=3 CMD curl -f http://localhost:8000/health || exit 1