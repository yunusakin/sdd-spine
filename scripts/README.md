# Scripts

This directory contains helper scripts for development and maintenance.

## Conventions
- Prefer small, single-purpose scripts.
- Document inputs, outputs, and side effects at the top of each script.
- Do not write to `app/` unless explicitly intended.

## Scripts
- `validate-repo.py`: Validate rule/spec index references, adapter consistency, and template formatting.
- `spec-diff.py`: Append a markdown diff entry for spec changes under `sdd/memory-bank/`.
