watch-py:
    watchexec -e py,pyi,toml just test-py check-py

watch-web:
    cd web && pnpm dev --open

################################################################################

test: test-py test-web

check: check-py check-web

format: format-py format-web

install: install-py install-web

################################################################################

test-py:
    cd lib && uv run pytest

regtest-approve-py:
    cd lib && uv run pytest --regtest-reset

check-py:
    cd lib && uv run ruff format --check
    cd lib && uv run ruff check

format-py:
    cd lib && uv run ruff format

install-py:
    cd lib && uv pip install -e ".[dev,docs,tests]"

################################################################################

test-web:
    cd web && pnpm test

check-web:
    cd web && pnpm check
    cd web && pnpm lint

format-web:
    cd web && pnpm format
    
install-web:
    cd web && pnpm install
