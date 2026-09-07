# Merge conflict

Two branches both changed the fallback version in `dashboard/config.py`.

- `develop` had `1.0.0-dev`
- `feature/version-note` had `1.0.1`

Git stopped on that line. We kept `1.0.0` as the fallback. Runtime version still comes from `APP_VERSION`, so this only matters when the env var is missing.

Resolved on `develop`. No force push.
