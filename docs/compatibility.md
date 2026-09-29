# Compatibility matrix

| Component | Tested or supported target | Notes |
|---|---|---|
| Python | 3.10, 3.11, 3.12 | CI matrix target; Python 3.10+ is required. |
| GitHub-hosted runner | `ubuntu-latest` | The core workflow uses Bash, `date`, `jq`, and the preinstalled `gh` CLI. |
| Self-hosted Linux runner | Supported when those tools are installed | Ensure `gh auth`/`GH_TOKEN`, GNU `date`, Bash, and `jq` are available. |
| Windows/macOS local CLI | Python CLI supported | Bash scripts require a compatible Bash environment; GNU `date` is recommended. |
| GitHub Enterprise Server | Not certified | The REST API version and Actions cache behavior should be tested against the target GHES release before production use. |
| GitHub token | `GITHUB_TOKEN`, classic PAT, fine-grained PAT, or GitHub App token | The token must be able to read and delete Actions data in the target repository. |

## Scope

This matrix describes the project’s intended compatibility, not a guarantee that every GitHub Enterprise configuration behaves identically. Run a dry-run against a disposable repository before adopting a new runner or GitHub environment.
