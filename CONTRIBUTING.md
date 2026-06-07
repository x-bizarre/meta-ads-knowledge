# How to contribute

## Quick start

```bash
# Clone the repository
git clone https://github.com/<org>/meta-ads-knowledge.git
cd meta-ads-knowledge

# Create a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
# .venv\Scripts\activate    # Windows

# Install dependencies + test dependencies
pip install -r requirements.txt
pip install pytest
```

## Running the tests

```bash
pytest
```

All tests run without API tokens and without network access. If a test requires external services, that's a bug in the test.

## Code style

- Python 3.9+, no external linters (no CI yet).
- Comments and docstrings — in Russian.
- User-facing error messages — in Russian.
- Imports: standard library, then third-party, then local.
- No secrets in code: tokens, keys, passwords — only via environment variables.

## How to propose a change

1. Fork the repository.
2. Create a branch off `main`: `git checkout -b fix/description`.
3. Make your changes and make sure `pytest` passes.
4. Open a Pull Request describing what changed and why.

## What could be improved

- Add tests for `generate_creative.py` and `host_image.py` (with mocks).
- Add CI (GitHub Actions: lint + pytest).
- Translate the documentation to English (or make it bilingual).
- Extend `_ACTION_ALIASES` in `meta_client.py` with new event types.
- Add a `--dry-run` mode to the scripts that talk to the API.
