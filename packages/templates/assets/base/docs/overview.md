# Spectra Overview

Spectra is the CLI operating system for AI-assisted product development.

It gives teams one opinionated flow:

1. define executable specs
2. validate structure and policy
3. advance staged approvals
4. implement with role-aware context
5. evaluate and verify before release

## What Makes v2 Different

### CLI-first

The product entry point is `spectra`, not `bash scripts/...` and not chat-only magic phrases.

### Executable specs

Feature state lives under `sdd/features/<feature-id>/` as YAML contracts plus a short Markdown brief.

### Staged approvals

Spectra uses:

- `draft`
- `product-approved`
- `technical-approved`
- `implementation-approved`
- `release-approved`

Implementation is blocked until `implementation-approved`.

### Eval and verify

`spectra eval` measures behavior contracts.  
`spectra verify` aggregates validation, policy, tests, eval readiness, telemetry coverage, and release confidence.

### Token-aware context

`spectra context --role <role> --goal <goal>` loads the minimum useful context instead of dumping the whole repo into every agent.

## Canonical State

Structured source of truth:

- `sdd/features/<feature-id>/feature.spec.yaml`
- `sdd/features/<feature-id>/ai-behavior-spec.yaml`
- `sdd/features/<feature-id>/telemetry-contract.yaml`
- `sdd/features/<feature-id>/evals/*`
- `sdd/governance/approval-state.yaml`
- `sdd/governance/decision-graph.yaml`

Human-readable support context:

- `sdd/features/<feature-id>/brief.md`
- optional supporting notes under `sdd/memory-bank/`

## Recommended Reading Order

1. [Quick Start](quick-start.md)
2. [CLI Reference](cli-reference.md)
3. [Structure](structure.md)
4. [Workflow](workflow.md)
5. [Minimal Feature Example](examples/minimal-feature/README.md)
