# FAQ

**What is this?** A cleanup tool for old Actions runs and artifacts.

**Does it delete workflow files?** No. It deletes history and generated artifacts only.

**Do I need a PAT?** Only for local use; the Action uses `GITHUB_TOKEN`.

**Can I undo deletion?** No. Test with dry-run and a long retention period first.

**Does it delete in-progress runs?** No.
