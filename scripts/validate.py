#!/usr/bin/env python3
"""Validate this repo against both formats it ships in.

Every plugin here carries two manifests — a root `plugin.json` for the Agent
Plugins 1.0.0 standard and a `.claude-plugin/plugin.json` for Claude Code — plus
an entry in the marketplace. Three files repeating the same name, version, and
description will drift. This checks that they do not.

Usage:  python3 scripts/validate.py
Exit 0 if everything agrees, 1 otherwise.
"""

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCHEMA = Path(__file__).resolve().parent / "plugin.schema.1.0.0.json"

errors: list[str] = []
notes: list[str] = []


def err(msg: str) -> None:
    errors.append(msg)


def load_json(path: Path):
    try:
        return json.loads(path.read_text())
    except FileNotFoundError:
        err(f"missing file: {path.relative_to(ROOT)}")
    except json.JSONDecodeError as e:
        err(f"invalid JSON in {path.relative_to(ROOT)}: {e}")
    return None


def frontmatter(path: Path) -> dict:
    """Parse the leading YAML frontmatter block as flat key: value pairs."""
    text = path.read_text()
    if not text.startswith("---\n"):
        err(f"{path.relative_to(ROOT)}: no YAML frontmatter")
        return {}
    end = text.find("\n---", 4)
    if end == -1:
        err(f"{path.relative_to(ROOT)}: unterminated frontmatter")
        return {}
    out, key = {}, None
    for line in text[4:end].splitlines():
        if line[:1] in (" ", "\t") and key:      # continuation of a wrapped value
            out[key] += " " + line.strip()
        elif ":" in line:
            key, _, value = line.partition(":")
            key = key.strip()
            out[key] = value.strip()
    return out


def run(cmd: list[str]) -> tuple[int, str]:
    p = subprocess.run(cmd, capture_output=True, text=True)
    return p.returncode, (p.stdout + p.stderr).strip()


# ---------------------------------------------------------------- marketplace
market = load_json(ROOT / ".claude-plugin" / "marketplace.json") or {}
entries = {e.get("name"): e for e in market.get("plugins", [])}

plugin_dirs = sorted(p for p in (ROOT / "plugins").iterdir() if p.is_dir())
if not plugin_dirs:
    err("no plugins found under plugins/")

for pdir in plugin_dirs:
    rel = pdir.relative_to(ROOT)

    # ------------------------------------------------ Agent Plugins manifest
    portable = load_json(pdir / "plugin.json")
    if portable is not None:
        try:
            import jsonschema

            schema = json.loads(SCHEMA.read_text())
            jsonschema.validate(portable, schema)
            notes.append(f"{rel}/plugin.json conforms to Agent Plugins 1.0.0")
        except ImportError:
            notes.append("jsonschema not installed — skipped schema validation")
        except jsonschema.ValidationError as e:
            err(f"{rel}/plugin.json violates Agent Plugins 1.0.0: {e.message}")

    # ------------------------------------------------------ Claude Code manifest
    claude = load_json(pdir / ".claude-plugin" / "plugin.json")

    # -------------------------------------------------------------- agreement
    if portable and claude:
        for field in ("name", "version", "description"):
            a, b = portable.get(field), claude.get(field)
            if a != b:
                err(
                    f"{rel}: {field} disagrees between manifests\n"
                    f"      plugin.json:                {a!r}\n"
                    f"      .claude-plugin/plugin.json: {b!r}"
                )

    name = (portable or claude or {}).get("name")
    if name and name != pdir.name:
        err(f"{rel}: manifest name {name!r} does not match directory name {pdir.name!r}")

    entry = entries.get(name)
    if entry is None:
        err(f"{rel}: no entry named {name!r} in marketplace.json")
    else:
        if portable and entry.get("description") != portable.get("description"):
            err(
                f"{rel}: description disagrees with its marketplace.json entry\n"
                f"      plugin.json:      {portable.get('description')!r}\n"
                f"      marketplace.json: {entry.get('description')!r}"
            )
        source = (ROOT / entry.get("source", "")).resolve()
        if source != pdir.resolve():
            err(f"{rel}: marketplace source {entry.get('source')!r} does not point here")

    # ----------------------------------------------------------------- skills
    skills_dir = pdir / "skills"
    if not skills_dir.is_dir():
        err(f"{rel}: no skills/ directory (Agent Plugins discovers skills there)")
        continue

    skills = sorted(s for s in skills_dir.iterdir() if s.is_dir())
    if not skills:
        err(f"{rel}/skills: contains no skills")
    for sdir in skills:
        srel = sdir.relative_to(ROOT)
        skill_md = sdir / "SKILL.md"
        if not skill_md.is_file():
            err(f"{srel}: missing SKILL.md")
            continue
        fm = frontmatter(skill_md)
        for field in ("name", "description"):
            if not fm.get(field):
                err(f"{srel}/SKILL.md: frontmatter missing required {field!r}")
        if fm.get("name") and fm["name"] != sdir.name:
            err(
                f"{srel}/SKILL.md: frontmatter name {fm['name']!r} "
                f"does not match directory name {sdir.name!r}"
            )
        notes.append(f"{srel}: SKILL.md ok")

# --------------------------------------------------------------- Claude Code CLI
for target in [ROOT] + plugin_dirs:
    code, out = run(["claude", "plugin", "validate", str(target), "--strict"])
    label = target.relative_to(ROOT) if target != ROOT else "."
    if code != 0:
        err(f"claude plugin validate --strict failed for {label}:\n{out}")
    else:
        notes.append(f"claude plugin validate --strict passed for {label}")

# ----------------------------------------------------------------------- report
for n in notes:
    print(f"  ok    {n}")
if errors:
    print()
    for e in errors:
        print(f"  FAIL  {e}")
    print(f"\n{len(errors)} problem(s) found.")
    sys.exit(1)
print("\nAll checks passed.")
