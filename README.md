# DRL_skills

A personal Claude Code **plugin marketplace**, published at
**https://github.com/JanCas/claude-skills**. Skills live here once and get
installed into individual projects as plugins, instead of being copied into each
project's `.claude/skills/`.

Nothing needs to be cloned to use it — Claude Code fetches the marketplace from
GitHub. See [Using it](#using-it-in-a-project). Cloning is only for
[adding or editing skills](#working-on-this-repo).

## Plugins

| Plugin | Skills | What it covers |
| --- | --- | --- |
| `research-figures` | `figure-versioning` | Filing generated plots into numbered version folders with a `MANIFEST.md` and a rolled-up `INDEX.md`, so every figure traces back to the run that produced it. |

---

## Using it in a project

Run these **from inside the target project's root**. No clone of this repo
required, on any machine.

### 1. Register the marketplace

```bash
claude plugin marketplace add JanCas/claude-skills --scope project
```

### 2. Install the plugin

```bash
claude plugin install research-figures@DRL_skills --scope project
```

The `@DRL_skills` suffix pins which marketplace it comes from. Restart Claude
Code (or start a new session) for the skill to load.

### 3. What that writes into the project's `.claude/settings.json`

Both commands edit the same file, and both keys are meant to be committed:

```json
{
  "extraKnownMarketplaces": {
    "DRL_skills": {
      "source": {
        "source": "github",
        "repo": "JanCas/claude-skills"
      }
    }
  },
  "enabledPlugins": {
    "research-figures@DRL_skills": true
  }
}
```

- `extraKnownMarketplaces` — where the project looks for plugins. Written by
  `marketplace add`.
- `enabledPlugins` — which plugins are on. Written by `install`.

A `github` source is portable: anyone who clones that project gets a working
marketplace entry, because it resolves against GitHub rather than a local disk
path. Both keys are safe and intended to commit.

### About `--scope`

| Scope | Written to | Applies to |
| --- | --- | --- |
| `user` (default) | `~/.claude/settings.json` | you, in every project |
| `project` | `<project>/.claude/settings.json` | anyone who clones that project |
| `local` | `<project>/.claude/settings.local.json` | this checkout only, not committed |

Use `project` when the skills should follow the repo — that is the usual case,
and it is what the commands above do. Use `user` for something you want
everywhere regardless of project.

### Picking up changes

The GitHub source serves **whatever has been pushed**, and the marketplace is
cached locally. After pushing a new or edited skill, pull it into a project with:

```bash
claude plugin marketplace update DRL_skills
```

### Undoing

```bash
claude plugin uninstall research-figures@DRL_skills --scope project
```

```bash
claude plugin marketplace remove DRL_skills --scope project
```

---

## Working on this repo

Only needed to add or change skills. Clone it:

```bash
git clone git@github.com:JanCas/claude-skills.git ~/code/claude-skills
```

### Layout

```text
claude-skills/
├── .claude-plugin/
│   └── marketplace.json          <- the marketplace manifest (lists plugins)
├── README.md
└── plugins/
    └── research-figures/         <- one themed bundle
        ├── .claude-plugin/
        │   └── plugin.json
        └── skills/
            └── figure-versioning/
                ├── SKILL.md
                ├── assets/
                └── references/
```

### Adding a skill

**Default: add it to an existing bundle.** Drop the skill directory into that
plugin's `skills/` folder. Nothing else needs to change — plugins pick up every
subdirectory of `skills/` automatically, and `plugin.json` does not enumerate
them.

```text
plugins/research-figures/skills/<new-skill-name>/SKILL.md
```

Bump the plugin's `version` in its `plugin.json` when you do, then commit and
push — the marketplace serves what is on GitHub, not what is on disk.

**Only create a new plugin for a genuinely separate concern.** The test is not
"is this a different topic?" — it is **"would I ever want this switched on while
the other skills in that bundle are switched off?"** If the answer is no, it
belongs in the existing bundle.

### Why bundling matters

Every enabled plugin's skill *names and descriptions* sit in context permanently,
in every session, whether or not the skill ever fires. Only the body of a
`SKILL.md` is loaded on demand. So the cost model is:

- **Always-on:** ~240 tokens per skill, paid on every single message.
- **On-invoke:** the full skill body (~2.7k tokens for `figure-versioning`), paid
  only when it actually triggers.

Check the real numbers for any plugin with:

```bash
claude plugin details research-figures
```

One plugin per skill would mean a long list of individually-toggled plugins, and
in practice you would enable them all everywhere — paying the always-on cost of
the entire library in every project. Themed bundles let you enable one thing and
get the handful of skills that genuinely belong together in that kind of work.

A new plugin is justified when a project would plausibly want bundle A without
bundle B — e.g. a `modeling-conventions` bundle is worth splitting out because a
pure data-analysis project wants figure conventions but not solver conventions.
"It's a different subject area" is not by itself a reason.

### Adding a new plugin

1. Create `plugins/<name>/.claude-plugin/plugin.json` with `name`, `version`,
   `description`, `author`.
2. Add a matching entry to the `plugins` array in
   `.claude-plugin/marketplace.json` — `name`, `description`, `source`
   (`./plugins/<name>`), `category`.
3. Validate, commit, push.

### This repo is public

Anything committed here is published. Skills often carry real numbers in their
examples — check `references/` and any worked examples for unpublished data
before pushing, and replace it with placeholders that keep the lesson intact.
`figure-versioning`'s worked example is genericized for exactly this reason.

### Validating

Run from the repo root. Both manifests should pass, including `--strict`:

```bash
claude plugin validate . --strict
```

```bash
claude plugin validate ./plugins/research-figures --strict
```

`--strict` treats warnings (unrecognized fields, missing metadata) as errors.
Use it — the non-strict run tolerates things the runtime merely shrugs at.

### Testing a skill before pushing

To try an edit without pushing, register the working copy by path in a scratch
project. This writes a machine-local `directory` source, so use it only in a
throwaway project or at `--scope local` — never in a `.claude/settings.json` you
intend to commit:

```bash
claude plugin marketplace add ~/code/claude-skills --scope local
```

It writes an absolute path, which will not resolve for anyone else:

```json
{
  "extraKnownMarketplaces": {
    "DRL_skills": {
      "source": {
        "source": "directory",
        "path": "/Users/janlukacas/code/claude-skills"
      }
    }
  }
}
```

Unlike the GitHub source, this one reflects the working tree immediately — no
commit or push needed. Remove it when done:

```bash
claude plugin marketplace remove DRL_skills --scope local
```
