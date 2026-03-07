# Spectra Core Instructions

Use Spectra's canonical system files as the source of truth.

## Required Behavior

- Start from `bash scripts/context-pack.sh --task <pack_id>` to determine what to read.
- Do not generate application code before explicit `approved`.
- Keep project state in `sdd/memory-bank/`.
- In consumer repositories, update `sdd/memory-bank/core/activeContext.md` and `sdd/memory-bank/core/progress.md` after significant work.
- Use `bash scripts/verify-work.sh` before marking work ready.
