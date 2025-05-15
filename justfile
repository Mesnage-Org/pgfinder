watch-py:
    watchexec -e py,pyi,toml just test-py check-py

test-py:
    cd lib && uv run pytest

regtest-approve-py:
    cd lib && uv run pytest --regtest-reset

check-py:
    cd lib && uv run ruff check

fmt-py:
    cd lib && uv run ruff format

install-py:
    cd lib && uv pip install -e ".[dev,docs,tests]"

watch-web:
    cd web && pnpm dev --open
