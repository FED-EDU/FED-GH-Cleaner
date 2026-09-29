# Public release checklist

## Before tagging

- [ ] `ruff check .` passes.
- [ ] `pytest -q` passes.
- [ ] Every Bash script passes `bash -n`.
- [ ] Workflow and action YAML parse successfully.
- [ ] `python -m build` succeeds.
- [ ] Review the dry-run behavior and permissions block.
- [ ] Confirm no token or private repository data is committed.
- [ ] Update `CHANGELOG.md` and release notes.

## Tagging

Create and push the release tags from a trusted maintainer checkout:

```bash
git tag -a v0.2.0 -m "gh-cleaner v0.2.0"
git tag -fa v0 -m "gh-cleaner major release line"
git push origin v0.2.0 v0
```

Do not create or move tags from an untrusted pull request workflow.

## Release assets

Publish the wheel, source distribution, and a SHA-256 checksum file. Release notes must state:

- Scheduled mode is preview-only by default.
- Destructive deletion requires deliberate confirmation.
- Deleted Actions data cannot be restored.
- The exact archive checksum is included with the assets.

## After release

- [ ] Test installation from the wheel in a clean environment.
- [ ] Test the manual workflow in a disposable repository or with a long retention period.
- [ ] Confirm the moving `v0` tag points to the intended release.
- [ ] Record any GitHub Enterprise Server differences before claiming support.
