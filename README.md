# SDD Spine

A spec-driven development (SDD) backbone that keeps project structure stable while working with AI agents or human-driven workflows.

- Specs live under [`sdd/memory-bank/`](sdd/memory-bank/)
- Agent rules live under [`sdd/.agent/`](sdd/.agent/)
- Application code (after approval) lives under [`app/`](app/)

## Quick Start

1. Pick your agent adapter:
   - Codex: [`AGENTS.md`](AGENTS.md)
   - Claude: [`CLAUDE.md`](CLAUDE.md)
   - Cursor: [`.cursorrules`](.cursorrules)
   - Other tools: [`AGENT.md`](AGENT.md)
2. In the repo root, run: `init`
3. Complete intake in phases (Core -> Type-specific -> Optional Advanced).
4. Fix any validation errors (rules: [`sdd/.agent/rules/intake/02-validation.md`](sdd/.agent/rules/intake/02-validation.md)).
5. When validation passes, reply `approved`.
6. After approval, all application code must be generated under `app/` only (see [`app/README.md`](app/README.md)).

> Resume: If you stop mid-intake, run `init` again. Progress is tracked in [`sdd/memory-bank/core/intake-state.md`](sdd/memory-bank/core/intake-state.md).

## Workflow Diagram (Mermaid)

```mermaid
flowchart TD
  S([Open repo]) --> A[Pick an agent adapter]
  A --> I[Run init]

  subgraph Intake["Intake and validation"]
    direction TB
    P1[Phase 1 core intake] --> V1{Validate phase 1}
    V1 -- fix --> P1
    V1 -- ok --> P2[Phase 2 type specific]
    P2 --> API[Phase 2b API style]
    API --> ADV{Advanced questions}
    ADV -- skip --> VS{Validate specs}
    ADV -- answer --> P3[Phase 3 advanced]
    P3 --> VS
    VS -- fix --> P2
    VS -- ok --> AP[Ask for approval]
    AP --> G{Approved}
    G -- no --> P2
  end

  I --> P1

  subgraph After["After approval"]
    direction TB
    APP[Ensure app directory exists] --> SK[Pick skills] --> CODE[Generate code under app only]
    CODE --> CH{Spec change later}
    CH -- yes --> UP[Update specs and spec history]
    UP --> VS
    CH -- no --> E([Continue development])
  end

  G -- yes --> APP

  %% Styling (GitHub Mermaid compatible)
  classDef phase fill:#E6F4FF,stroke:#0550AE,color:#0B2F5B
  classDef decision fill:#FFF4E5,stroke:#B54708,color:#4A2500
  classDef action fill:#ECFDF3,stroke:#027A48,color:#054F31
  classDef terminal fill:#F2F4F7,stroke:#667085,color:#101828

  class P1,P2,API,P3 phase
  class V1,ADV,VS,G,CH decision
  class S,A,I,AP,APP,SK,CODE,UP action
  class E terminal

  style Intake fill:#F8FAFC,stroke:#CBD5E1
  style After fill:#F8FAFC,stroke:#CBD5E1
```

## Docs

| Doc | Use it for |
| --- | --- |
| [`docs/overview.md`](docs/overview.md) | What this repo is and the core principles |
| [`docs/quick-start.md`](docs/quick-start.md) | Minimal path: init -> validate -> approved |
| [`docs/getting-started.md`](docs/getting-started.md) | Full walkthrough + detailed diagram |
| [`docs/workflow.md`](docs/workflow.md) | Resume, spec changes, re-approval, rollback |
| [`docs/testing.md`](docs/testing.md) | Repo validation and regression scenarios |
| [`docs/examples/`](docs/examples/) | Copy-paste scenarios for common app types |

## Repo Layout

```text
sdd/       agent rules + memory bank specs
app/       application code (only after approval)
docs/      documentation
scripts/   repo validation helpers
```

## Core Rules

- No application code before explicit approval.
- Update specs first, then validate, then implement.
- Keep all application code under `app/` only.
- If requirements change after approval:
  - update specs
  - record the change in [`sdd/memory-bank/core/spec-history.md`](sdd/memory-bank/core/spec-history.md)
  - follow [`docs/workflow.md`](docs/workflow.md)

## Example Intake (Phase 1)

- Project name: Customer Orders Service
- Primary purpose/goal: Manage customer orders, payments, and shipment status.
- App type: Backend API
- Primary language + version: Java 21
- Framework + version: Spring Boot 3.2
- Architecture style: Hexagonal
- Primary data store + version: PostgreSQL 16
- Deployment target: Kubernetes
- API style: REST
