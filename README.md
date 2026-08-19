# DRL_skills

Published at **https://github.com/JanCas/claude-skills** (public).

A personal Claude Code **plugin marketplace**. Skills live here once and get
installed into individual projects as plugins, instead of being copied into each
project's `.claude/skills/`.

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

## Plugins

| Plugin | Skills | What it covers |
| --- | --- | --- |
| `research-figures` | `figure-versioning` | Filing generated plots into numbered version folders with a `MANIFEST.md` and a rolled-up `INDEX.md`, so every figure traces back to the run that produced it. |

## How to add a skill

**Default: add it to an existing bundle.** Drop the skill directory into that
plugin's `skills/` folder. Nothing else needs to change — plugins pick up every
subdirectory of `skills/` automatically, and `plugin.json` does not enumerate
them.

```text
plugins/research-figures/skills/<new-skill-name>/SKILL.md
```

Bump the plugin's `version` in its `plugin.json` when you do.

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
3. Validate (see below) and commit.

## Validating

Run from the repo root. Both manifests should pass, including `--strict`:

```bash
claude plugin validate . --strict
```

```bash
claude plugin validate ./plugins/research-figures --strict
```

`--strict` treats warnings (unrecognized fields, missing metadata) as errors.
Use it — the non-strict run tolerates things the runtime merely shrugs at.

## Installing into a project

Run these **from inside the target project's root**, not from this repo.

### 1. Register this marketplace

From the local path — picks up edits immediately, no push needed:

```bash
claude plugin marketplace add ~/code/claude-skills --scope project
```

Or from GitHub — resolves on any machine, and for anyone who clones the project:

```bash
claude plugin marketplace add JanCas/claude-skills --scope project
```

Use the local path while iterating on a skill; use the GitHub form for anything
whose `.claude/settings.json` gets committed and shared. The two write different
`source` blocks (see below).

`--scope` takes `user` (default, applies to you everywhere), `project`
(committed with the repo, applies to anyone who clones it), or `local`
(this checkout only, not committed). Use `project` when the project's skills
should follow the repo; use `user` for something you want everywhere.

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
        "source": "directory",
        "path": "/Users/janlukacas/code/claude-skills"
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

**Note the absolute path.** That is what the *local path* form writes, and a
`directory` source is machine-local — a collaborator cloning the project gets a
marketplace entry pointing at a path that does not exist for them. The GitHub
form writes a portable source instead:

```json
{
  "extraKnownMarketplaces": {
    "DRL_skills": {
      "source": { "source": "github", "repo": "JanCas/claude-skills" }
    }
  }
}
```

Rule of thumb: local path for a project only you touch, `JanCas/claude-skills`
for anything you commit and share. The GitHub form serves whatever is pushed, so
a skill edited locally will not appear until it is committed and pushed.

### Undoing

```bash
claude plugin uninstall research-figures@DRL_skills --scope project
```

```bash
claude plugin marketplace remove DRL_skills --scope project
```

### After editing a skill in this repo

Changes are picked up from the local path, but the marketplace metadata is
cached. If a new skill or a changed description does not show up:

```bash
claude plugin marketplace update DRL_skills
```
