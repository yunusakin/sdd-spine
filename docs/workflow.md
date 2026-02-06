# Workflow Guide

This guide explains how to resume intake, how to change specs after approval, and how to track and roll back changes.

## Resume Intake
- Intake progress is tracked in `sdd/memory-bank/core/intake-state.md`.
- If you stop mid-intake, re-run `init`. The agent should:
  - read existing spec files
  - ask only for missing mandatory answers first
  - continue with the next phase in small question batches

## Spec Changes After Approval
If you change requirements or technical choices after you have replied `approved`:

1. Update the relevant spec files under `sdd/memory-bank/` first.
2. Record the change in `sdd/memory-bank/core/spec-history.md`.
3. Update the spec diff report (recommended): `bash scripts/spec-diff.sh --update` (report: `sdd/memory-bank/core/spec-diff.md`).
4. Re-run validation rules (`sdd/.agent/rules/intake/02-validation.md`) for impacted mandatory fields.
5. If the change affects behavior or any mandatory field, the agent should pause and ask for explicit re-approval (`approved`) before continuing.

## Change Tracking
Use `sdd/memory-bank/core/spec-history.md` to track:
- initial approval (v1)
- major spec changes (v2, v3, ...)
- any re-approvals

## Rollback
If a change was wrong or premature:
- prefer a new commit that reverts the change (avoid rewriting git history)
- update specs to reflect the intended state after rollback
- record the rollback in `sdd/memory-bank/core/spec-history.md`
