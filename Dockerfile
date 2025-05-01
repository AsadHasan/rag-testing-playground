FROM python:3.14.0a7-slim@sha256:b096b601c605a4b7b49a67dc5d72ded9af9f86426eb9ed8a91d70cb45ef101cb

WORKDIR /app

COPY src ./src
COPY pyproject.toml .
COPY README.md .

RUN python3 -m pip install --user --no-cache-dir pipx==1.7.1 \
    && python3 -m pipx ensurepath --force \
    && export PATH="${PATH}:$(python3 -c 'import site; print(site.USER_BASE)')/bin" \
    && pipx ensurepath --global \
    && pipx install poetry==2.1.2 \
    && poetry config virtualenvs.in-project true \
    && poetry sync --no-root --without dev

ENTRYPOINT ["bash", "-c"]
