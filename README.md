<p align="center">
  <img src="assets/logo.png" alt="Spectra Logo" width="200">
</p>

# Spectra

Spectra is a spec-driven workflow for AI-assisted development.

The idea is simple:

1. Define the product in specs first.
2. Validate those specs.
3. Approve the plan.
4. Let AI implement inside that boundary.

Spectra is not “just generate code.” It is “make AI behave through specs.”

## What Spectra Gives You

When Spectra is added to a project, it gives you:

- `sdd/system/` for the workflow rules and runtime
- `sdd/memory-bank/` for specs, decisions, context, and progress
- `scripts/` for install, validation, policy, discovery, and verification
- `app/` as the place for application code after approval

## The Basic Flow

### 1. Install Spectra into your project

From this Spectra repository:

```bash
bash scripts/init.sh /path/to/your-project
```

Optional:

```bash
# existing repo? create discovery notes first
bash scripts/init.sh /path/to/your-project --adopt

# generate AI tool adapters
bash scripts/init.sh /path/to/your-project --agents claude,cursor,windsurf,copilot,codex,antigravity
```

### 2. Go to your project and start intake

```bash
cd /path/to/your-project
bash scripts/context-pack.sh --task bootstrap
```

Then, in your AI chat/runtime, send:

```text
init
```

The AI should now ask intake questions and write the project specs under `sdd/memory-bank/`.

### 3. Validate the specs

Run:

```bash
bash scripts/validate-repo.sh --strict
bash scripts/check-policy.sh
```

If the specs are correct and validation passes, send this in your AI chat/runtime:

```text
approved
```

Only after approval should application code be created or changed under `app/`.

### 4. Implement and verify

Before implementation work, capture intent:

```bash
bash scripts/discuss-task.sh --item TASK-001 --task-type bugfix --goal "Describe intended change"
```

Before handoff, run:

```bash
bash scripts/verify-work.sh --scope app
```

## Important

- `init` and `approved` are chat messages, not shell commands.
- `validate-repo.sh`, `check-policy.sh`, and `verify-work.sh` are shell commands.
- Spectra should control AI behavior through specs before code is written.

## If Your Repo Already Has Code

Use discovery mode:

```bash
bash scripts/map-codebase.sh --root /path/to/your-project
```

This creates discovery notes under `sdd/memory-bank/discovery/`.

Those notes are hints, not final decisions.

## AI Tool Adapters

Spectra can generate optional adapters for:

- `Claude Code`
- `Cursor`
- `Windsurf`
- `GitHub Copilot`
- `Codex`
- `Antigravity`

Generate them with:

```bash
bash scripts/generate-adapters.sh --agents claude,cursor,windsurf,copilot,codex,antigravity --target /path/to/your-project
```

## Project Shape After Install

```text
your-project/
├── sdd/
│   ├── system/
│   └── memory-bank/
├── scripts/
└── app/
```

## If You Are Changing Spectra Itself

If you are working on this repository, use:

```bash
bash scripts/validate-repo.sh --strict
bash scripts/check-policy.sh
bash scripts/verify-work.sh --scope spec
```

## Read Next

- `docs/quick-start.md`
- `docs/getting-started.md`
- `docs/workflow.md`
- `CHANGELOG.md`

## License

MIT. See [`LICENSE`](LICENSE).
