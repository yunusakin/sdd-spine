# Getting Started

This guide explains the end-to-end Spectra v2 workflow in the order teams should actually use it.

## 1. Initialize Spectra

New repo:

```bash
npx spectra-pack@latest init my-product
cd my-product
```

Brownfield repo:

```bash
npx spectra-pack@latest adopt .
```

## 2. Create a feature

Every meaningful change should start with a feature bundle:

```bash
spectra feature init demo-intake --name "Demo Intake Assistant" --type assistant
```

That creates:

- `sdd/features/demo-intake/feature.spec.yaml`
- `sdd/features/demo-intake/ai-behavior-spec.yaml`
- `sdd/features/demo-intake/telemetry-contract.yaml`
- `sdd/features/demo-intake/evals/*`
- `sdd/features/demo-intake/brief.md`

## 3. Plan with the minimum context

```bash
spectra context --role planner --goal discover
```

Use context packs by role and goal instead of opening the whole repo.

## 4. Validate before approval

```bash
spectra validate
spectra status
```

Validation should pass before any approval moves forward.

## 5. Advance staged approvals

```bash
spectra approve --stage product-approved
spectra approve --stage technical-approved
spectra approve --stage implementation-approved
```

Meaning:

- `product-approved`: feature intent and scope are accepted
- `technical-approved`: architecture and technical boundaries are accepted
- `implementation-approved`: implementation can start

## 6. Create implementation intent

```bash
spectra task --item FEAT-001 --task-type feature --goal "Implement demo intake assistant"
```

This writes the implementation brief used during execution and review.

## 7. Implement with role-aware context

```bash
spectra context --role implementer --goal implement
```

Use:

- `planner + discover`
- `planner + decide`
- `implementer + implement`
- `verifier + verify`
- `release-manager + ship`

## 8. Evaluate behavior

```bash
spectra eval demo-intake --suite smoke
```

This checks the feature’s eval contracts, golden scenarios, and release thresholds.

## 9. Verify release confidence

```bash
spectra verify --profile release
```

Verify is the final release gate. It should answer:

- is the repo structurally valid?
- is policy current?
- do eval and telemetry contracts exist?
- is release confidence high enough?

## 10. Mark release approval

```bash
spectra approve --stage release-approved
```

## Common Mistakes

- treating Spectra like a binary `approved / not approved` system
- editing YAML manually before using the CLI flow
- skipping `spectra validate`
- starting implementation before `implementation-approved`
- treating `verify` like a test runner instead of a release-confidence gate
