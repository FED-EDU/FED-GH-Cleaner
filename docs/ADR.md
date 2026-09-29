# Architecture Decision Records

## ADR-0001: No third-party GitHub Actions in cleanup.yml

**Status:** accepted.

**Context:** cleanup deletes data and should be easy to audit.

**Decision:** use only runner-provided Bash, `date`, and `gh api` in the core workflow.

**Consequences:** the workflow is transparent and independent, but the shell code needs local maintenance.
