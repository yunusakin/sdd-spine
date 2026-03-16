<p align="center">
  <img src="assets/logo.png" alt="Spectra Logo" width="200">
</p>

# Spectra

Spectra is the CLI operating system for AI-assisted product development.

<p align="center">
  <a href="https://www.npmjs.com/package/spectra-pack">
    <img src="https://img.shields.io/npm/v/spectra-pack?color=cb3837&label=npm" alt="npm version">
  </a>
  <a href="https://www.npmjs.com/package/spectra-pack">
    <img src="https://img.shields.io/npm/dm/spectra-pack" alt="npm downloads">
  </a>
  <a href="LICENSE">
    <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="MIT License">
  </a>
</p>

Spectra turns product intent into executable specs, staged approvals, implementation guidance, evals, and release confidence.

## Install With npx

```bash
npx spectra-pack@latest init my-product
cd my-product
spectra feature init demo-intake --name "Demo Intake Assistant" --type assistant
spectra validate
spectra status
```

Already have a repo?

```bash
npx spectra-pack@latest adopt .
```

## The v2 Story

Spectra is built around one flow:

1. Define a feature as executable specs.
2. Validate structure, policy, and approval state.
3. Advance staged approvals before implementation.
4. Load token-aware context packs by role and goal.
5. Evaluate behavior and verify release confidence before shipping.

This is not a shell-script toolkit and not a markdown-only process template. The product surface is the `spectra` CLI.

## Golden Path

```bash
npx spectra-pack@latest init my-product
cd my-product

spectra feature init demo-intake --name "Demo Intake Assistant" --type assistant
spectra context --role planner --goal discover

spectra validate
spectra approve --stage product-approved
spectra approve --stage technical-approved

spectra task --item FEAT-001 --task-type feature --goal "Implement demo intake assistant"
spectra approve --stage implementation-approved

spectra context --role implementer --goal implement
spectra eval demo-intake --suite smoke
spectra verify --profile release
spectra approve --stage release-approved
```

## What Spectra Creates

```text
your-project/
├── .spectra/
├── app/
├── docs/
└── sdd/
    ├── features/
    │   └── <feature-id>/
    ├── governance/
    └── system/
```

Important directories:

- `sdd/features/`: executable feature bundles
- `sdd/governance/`: staged approval state and decision graph
- `sdd/system/`: runtime rules, prompts, adapters, and scaffolds

Optional supporting context may also exist under `sdd/memory-bank/`, but the v2 source of truth is the feature bundle plus governance YAML.

## Core Commands

Setup:

```bash
spectra init [path]
spectra adopt [path]
spectra feature init <feature-id>
```

Workflow:

```bash
spectra context --role <role> --goal <goal>
spectra task --item <id> --task-type <type> --goal "<goal>"
spectra approve --stage <stage>
spectra validate
spectra eval <feature-id> --suite smoke
spectra verify --profile release
spectra status
```

Utilities:

```bash
spectra adapters --agents codex,cursor --target .
spectra diff semantic
spectra doctor
spectra quick --type docs --task "refresh docs"
```

## Brownfield Adoption

Use `spectra adopt` when code already exists.

```bash
spectra adopt .
spectra validate
spectra diff semantic
spectra status
```

Adoption outputs live under:

- `sdd/adoption/current-state.summary.yaml`
- `sdd/adoption/gap-analysis.yaml`
- `sdd/adoption/review-queue.yaml`

## Read Next

- [Quick Start](docs/quick-start.md)
- [CLI Reference](docs/cli-reference.md)
- [Structure](docs/structure.md)
- [Workflow](docs/workflow.md)
- [Minimal Feature Example](docs/examples/minimal-feature/README.md)

## Local Development

If you are changing Spectra itself:

```bash
npm install
./node_modules/.bin/spectra validate
./node_modules/.bin/spectra verify --scope spec
```

## License

MIT. See [`LICENSE`](LICENSE).
