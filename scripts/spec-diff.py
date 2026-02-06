#!/usr/bin/env python3
"""
SDD Spine spec diff report generator.

Purpose:
- Generate a readable Markdown report of spec changes under `sdd/memory-bank/`.
- Keep a baseline in the report itself so downstream projects can track deltas over time.

Usage:
  python3 scripts/spec-diff.py --init
  python3 scripts/spec-diff.py --update

Notes:
- This script uses git to compute diffs. Run it inside a git repo.
- It writes to `sdd/memory-bank/core/spec-diff.md` by default.
"""

from __future__ import annotations

import argparse
import datetime as dt
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


DEFAULT_REPORT = Path("sdd/memory-bank/core/spec-diff.md")
DEFAULT_SCOPE_ROOT = Path("sdd/memory-bank")

# These files change frequently and make diffs noisy. They are still useful, but
# the default report focuses on "spec content" rather than process logs/state.
DEFAULT_EXCLUDES = {
    Path("sdd/memory-bank/core/intake-state.md"),
    Path("sdd/memory-bank/core/progress.md"),
    Path("sdd/memory-bank/core/progress-archive.md"),
    Path("sdd/memory-bank/core/sprint-current.md"),
    Path("sdd/memory-bank/core/sprint-plan.md"),
    Path("sdd/memory-bank/core/backlog.md"),
    Path("sdd/memory-bank/core/spec-diff.md"),  # avoid self-diff recursion
}


@dataclass(frozen=True)
class DiffSummary:
    added: list[Path]
    modified: list[Path]
    deleted: list[Path]
    renamed: list[str]


def run_git(repo_root: Path, args: list[str]) -> str:
    p = subprocess.run(
        ["git", *args],
        cwd=repo_root,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if p.returncode != 0:
        raise RuntimeError(p.stderr.strip() or f"git {' '.join(args)} failed")
    return p.stdout


def utc_now_str() -> str:
    return dt.datetime.now(tz=dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ")


def repo_root_from_script() -> Path:
    return Path(__file__).resolve().parent.parent


def parse_last_head_ref(report_text: str) -> str | None:
    # Look for the most recent "Head ref:" line.
    # Format is intentionally simple and easy to parse.
    last = None
    for line in report_text.splitlines():
        if line.startswith("Head ref:"):
            val = line.split(":", 1)[1].strip()
            if val:
                last = val
    return last


def load_report_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def ensure_report_exists(report_path: Path) -> None:
    report_path.parent.mkdir(parents=True, exist_ok=True)
    if report_path.exists():
        return
    report_path.write_text(
        "# Spec Diff Report\n\n"
        "> This file is generated/updated by `python3 scripts/spec-diff.py`.\n\n",
        encoding="utf-8",
    )


def is_excluded(path: Path, excludes: set[Path]) -> bool:
    # Normalize to repo-relative forward paths (Path on mac/linux is fine).
    return path in excludes


def diff_name_status(
    repo_root: Path,
    base_ref: str,
    scope_root: Path,
    excludes: set[Path],
    use_worktree: bool,
) -> DiffSummary:
    # Base vs worktree: git diff <base>
    # Base vs committed range: git diff <base>..<head>
    args = ["diff", "--name-status", base_ref]
    if not use_worktree:
        head_ref = run_git(repo_root, ["rev-parse", "HEAD"]).strip()
        args = ["diff", "--name-status", f"{base_ref}..{head_ref}"]
    args += ["--", str(scope_root)]

    out = run_git(repo_root, args)
    added: list[Path] = []
    modified: list[Path] = []
    deleted: list[Path] = []
    renamed: list[str] = []

    for raw in out.splitlines():
        if not raw.strip():
            continue

        # Examples:
        # M\tpath/to/file.md
        # A\tpath/to/file.md
        # D\tpath/to/file.md
        # R100\told.md\tnew.md
        parts = raw.split("\t")
        status = parts[0]
        if status.startswith("R") and len(parts) >= 3:
            old_p = Path(parts[1])
            new_p = Path(parts[2])
            if not is_excluded(old_p, excludes) and not is_excluded(new_p, excludes):
                renamed.append(f"{old_p} -> {new_p}")
            continue

        if len(parts) < 2:
            continue
        p = Path(parts[1])
        if is_excluded(p, excludes):
            continue
        if status == "A":
            added.append(p)
        elif status == "D":
            deleted.append(p)
        else:
            # Treat everything else as modified (M, T, etc.)
            modified.append(p)

    added.sort()
    modified.sort()
    deleted.sort()
    renamed.sort()
    return DiffSummary(added=added, modified=modified, deleted=deleted, renamed=renamed)


def build_report_entry(
    base_ref: str,
    head_ref: str,
    summary: DiffSummary,
    use_worktree: bool,
    scope_root: Path,
    excludes: set[Path],
    include_patch: bool,
    repo_root: Path,
) -> str:
    ts = utc_now_str()
    lines: list[str] = []
    lines.append(f"## {ts}")
    lines.append("")
    lines.append(f"Base ref: {base_ref}")
    lines.append(f"Head ref: {head_ref}")
    lines.append(f"Scope: {scope_root}")
    lines.append(f"Includes worktree: {'yes' if use_worktree else 'no'}")
    if excludes:
        lines.append("Excludes:")
        for p in sorted(excludes):
            lines.append(f"- `{p}`")
    lines.append("")
    lines.append("### Summary")
    lines.append(f"- Added: {len(summary.added)}")
    lines.append(f"- Modified: {len(summary.modified)}")
    lines.append(f"- Deleted: {len(summary.deleted)}")
    lines.append(f"- Renamed: {len(summary.renamed)}")
    lines.append("")

    if summary.added:
        lines.append("### Added")
        for p in summary.added:
            lines.append(f"- `{p}`")
        lines.append("")

    if summary.modified:
        lines.append("### Modified")
        for p in summary.modified:
            lines.append(f"- `{p}`")
        lines.append("")

    if summary.deleted:
        lines.append("### Deleted")
        for p in summary.deleted:
            lines.append(f"- `{p}`")
        lines.append("")

    if summary.renamed:
        lines.append("### Renamed")
        for r in summary.renamed:
            lines.append(f"- `{r}`")
        lines.append("")

    if include_patch:
        lines.append("### Patch")
        lines.append("")
        for p in summary.added + summary.modified + summary.deleted:
            # Render a per-file diff to keep patch blocks manageable and avoid
            # pathspec exclude complexity.
            diff_args = ["diff", "--", str(p)]
            if use_worktree:
                diff_args = ["diff", base_ref, "--", str(p)]
            else:
                diff_args = ["diff", f"{base_ref}..{head_ref}", "--", str(p)]

            try:
                patch = run_git(repo_root, diff_args).rstrip()
            except RuntimeError as e:
                patch = f"Error generating diff for {p}: {e}"

            lines.append(f"#### `{p}`")
            lines.append("")
            lines.append("```diff")
            lines.append(patch if patch else "(no changes)")
            lines.append("```")
            lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", default=str(DEFAULT_REPORT), help="Path to the markdown report to update.")
    parser.add_argument("--scope", default=str(DEFAULT_SCOPE_ROOT), help="Root directory to diff (default: sdd/memory-bank).")
    parser.add_argument("--base", default=None, help="Git ref to diff from. Defaults to last recorded head ref in report.")
    parser.add_argument("--no-worktree", action="store_true", help="Compare commits only (base..HEAD), ignore uncommitted worktree changes.")
    parser.add_argument("--patch", action="store_true", help="Include per-file diff patches in the markdown report.")
    parser.add_argument("--init", action="store_true", help="Initialize baseline by recording current HEAD as the last known ref.")
    parser.add_argument("--update", action="store_true", help="Append a new diff entry to the report.")
    parser.add_argument("--stdout", action="store_true", help="Print the generated entry to stdout instead of writing the report.")
    args = parser.parse_args()

    if args.init == args.update:
        print("Error: choose exactly one of --init or --update", file=sys.stderr)
        return 2

    repo_root = repo_root_from_script()
    report_path = (repo_root / args.report).resolve()
    scope_root = Path(args.scope)
    if scope_root.is_absolute():
        try:
            scope_root = scope_root.relative_to(repo_root)
        except ValueError:
            print("Error: --scope must be inside the repository.", file=sys.stderr)
            return 2

    if not (repo_root / ".git").exists():
        print("Error: this does not look like a git repository (missing .git).", file=sys.stderr)
        return 2

    head_ref = run_git(repo_root, ["rev-parse", "HEAD"]).strip()
    report_text = load_report_text(report_path)
    last_head = parse_last_head_ref(report_text)

    excludes = {p for p in DEFAULT_EXCLUDES}

    if args.init:
        ensure_report_exists(report_path)
        report_text = load_report_text(report_path)
        entry = "\n".join(
            [
                f"## {utc_now_str()}",
                "",
                f"Base ref: {head_ref}",
                f"Head ref: {head_ref}",
                f"Scope: {scope_root}",
                "Includes worktree: no",
                "",
                "### Summary",
                "- Baseline initialized (no diff).",
                "",
            ]
        )
        if args.stdout:
            sys.stdout.write(entry)
            return 0
        report_path.write_text(report_text.rstrip() + "\n\n" + entry, encoding="utf-8")
        return 0

    # --update
    base_ref = args.base or last_head
    if not base_ref:
        print(
            "Error: no base ref found. Run once with --init (recommended after first approval),\n"
            "or pass an explicit --base <git-ref>.\n",
            file=sys.stderr,
        )
        return 2

    use_worktree = not args.no_worktree
    summary = diff_name_status(repo_root, base_ref, scope_root, excludes, use_worktree=use_worktree)

    if not (summary.added or summary.modified or summary.deleted or summary.renamed):
        entry = "\n".join(
            [
                f"## {utc_now_str()}",
                "",
                f"Base ref: {base_ref}",
                f"Head ref: {head_ref}",
                f"Scope: {scope_root}",
                f"Includes worktree: {'yes' if use_worktree else 'no'}",
                "",
                "### Summary",
                "- No changes detected in the default scope.",
                "",
            ]
        )
    else:
        entry = build_report_entry(
            base_ref=base_ref,
            head_ref=head_ref,
            summary=summary,
            use_worktree=use_worktree,
            scope_root=scope_root,
            excludes=excludes,
            include_patch=args.patch,
            repo_root=repo_root,
        )

    if args.stdout:
        sys.stdout.write(entry)
        return 0

    ensure_report_exists(report_path)
    report_text = load_report_text(report_path).rstrip()
    report_path.write_text(report_text + "\n\n" + entry, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
