# Contributing

Welcome. Contributions include issues, pull requests, documentation, translations, and sponsorships.

## Development

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest
ruff check .
```

Use branches such as `feat/...` and `fix/...`, and Conventional Commits. The core cleanup workflow intentionally has no third-party `uses:` entries; do not add them in PRs.

