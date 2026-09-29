# Development

Prerequisites: Python 3.10+, Git, the GitHub CLI, and Bash.

```bash
git clone https://github.com/FED-OS/gh-cleaner.git
cd gh-cleaner
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest
ruff check .
ruff format .
python -m build
python -m gh_cleaner --help
```

Python code belongs in `src/gh_cleaner/`; reusable shell functions belong in `scripts/`; tests belong in `tests/`; user-facing explanations belong in `docs/`. Add tests before changing deletion behavior. Test against a throwaway repository or use dry-run first. Releases are tagged `vX.Y.Z` after the test workflow passes.
