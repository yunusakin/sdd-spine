# Quick Start

This is the fastest CLI-only path through Spectra v2.

## 1. Initialize a repo

```bash
npx spectra-pack@latest init my-product
cd my-product
```

Existing codebase:

```bash
npx spectra-pack@latest adopt .
```

## 2. Create your first feature bundle

```bash
spectra feature init demo-intake --name "Demo Intake Assistant" --type assistant
```

## 3. Load planning context

```bash
spectra context --role planner --goal discover
```

## 4. Validate the current state

```bash
spectra validate
spectra status
```

## 5. Advance staged approvals

```bash
spectra approve --stage product-approved
spectra approve --stage technical-approved
spectra approve --stage implementation-approved
```

## 6. Create an implementation brief

```bash
spectra task --item FEAT-001 --task-type feature --goal "Implement demo intake assistant"
```

## 7. Load implementation context

```bash
spectra context --role implementer --goal implement
```

## 8. Run eval and verify

```bash
spectra eval demo-intake --suite smoke
spectra verify --profile release
```

## 9. Mark release approval

```bash
spectra approve --stage release-approved
```

## Next

- [CLI Reference](cli-reference.md)
- [Workflow](workflow.md)
- [Minimal Feature Example](examples/minimal-feature/README.md)
