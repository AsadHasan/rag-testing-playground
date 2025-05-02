FROM python:3.13.3@sha256:884da97271696864c2eca77c6362b1c501196d6377115c81bb9dd8d538033ec3 AS builder

WORKDIR /app

COPY pyproject.toml .

RUN python3 -m pip install --user --no-cache-dir pipx==1.7.1 \
    && python3 -m pipx ensurepath --force \
    && export PATH="${PATH}:$(python3 -c 'import site; print(site.USER_BASE)')/bin" \
    && pipx ensurepath --global \
    && pipx install poetry==2.1.2 \
    && poetry config virtualenvs.in-project true \
    && poetry sync --no-root --without dev

FROM python:3.13.3-slim@sha256:60248ff36cf701fcb6729c085a879d81e4603f7f507345742dc82d4b38d16784 AS final

WORKDIR /app

COPY --from=builder /app/.venv/ ./.venv
COPY ./src/ ./src

ENTRYPOINT ["bash", "-c"]
