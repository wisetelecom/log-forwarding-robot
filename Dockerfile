# syntax=docker/dockerfile:1
ARG PYTHON_VERSION=3.11

FROM python:${PYTHON_VERSION}-slim-bookworm AS builder

WORKDIR /app

COPY ./pyproject.toml ./uv.lock ./README.md ./
COPY src/ src/

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

RUN uv build


FROM python:${PYTHON_VERSION}-slim-bookworm

# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/go/dockerfile-user-best-practices/
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser


COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

# 从构建阶段复制虚拟环境
COPY --from=builder /app/dist/*.whl /tmp/
RUN --mount=type=cache,target=/root/.cache/uv \
    uv pip install --system /tmp/*.whl

# Switch to the non-privileged user to run the application.
USER appuser

ARG HTTP_PORT=80


# Expose the port that the application listens on.
EXPOSE ${HTTP_PORT}/tcp

CMD ["ptb", "--port=80"]
