# Architecture

Components: pure Bash workflow, reusable shell functions, optional Python API client, and tests. Data flow: GitHub runner → gh API list → filter by UTC cutoff → delete selected IDs.
