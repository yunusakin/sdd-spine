## Quick Start

1. Install Spectra in your project:

```bash
bash scripts/init.sh /path/to/your-project

# Optional adapters:
bash scripts/init.sh /path/to/your-project --agents claude,cursor,windsurf,copilot,codex,antigravity

# Optional brownfield discovery:
bash scripts/init.sh /path/to/your-project --adopt
```

2. Resolve bootstrap context:

```bash
bash scripts/context-pack.sh --task bootstrap
```

3. Type `init`.
   This is a chat/runtime message, not a shell command.
4. Answer Phase 1 (Core) questions.
5. For technical choices, confirm recommendations before persistence.
6. Ensure `sdd/memory-bank/core/intake-state.md` has:
   - `Decision Log` entries for confirmed choices
   - no unresolved blockers before approval
7. Run checks:

```bash
bash scripts/validate-repo.sh --strict
bash scripts/check-policy.sh
```

8. When specs are correct and checks pass, reply `approved`.
   This is also a chat/runtime message, not a shell command.
9. Before implementation work, write an implementation brief:

```bash
bash scripts/discuss-task.sh --item TASK-001 --task-type bugfix --goal "Describe intended change"
```

10. After `approved`, Spectra scaffolds under `app/` and starts sprint execution.

## Open Question Workflow

If a technical question is unresolved:
1. Add it to `Open Technical Questions` with status `open`.
2. Attach an issue reference.
3. Resolve and set status to `resolved`.
4. Re-run policy checks.

Health check anytime:

```bash
bash scripts/health-check.sh
```
