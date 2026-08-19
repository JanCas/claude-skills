# DRL_skills

A personal **agent skills** repo, published at
**https://github.com/JanCas/claude-skills**. Skills live here once and get
installed into individual projects as plugins, instead of being copied into each
project's `.claude/skills/`.

Each plugin ships in two formats at once: **Agent Plugins 1.0.0** (the
vendor-neutral standard, read by ChatGPT, Codex, Cursor, Copilot, VS Code and
Kiro) and **Claude Code**'s own plugin + marketplace format. The skills
themselves are shared, not duplicated.

Nothing needs to be cloned to use it — Claude Code fetches the marketplace from
GitHub. If you are not the author, start with [For collaborators](#for-collaborators).
Cloning is only for [adding or editing skills](#working-on-this-repo).

---

## For collaborators

No clone, no GitHub account, no access request — the repo is public. Two commands,
run from anywhere. *(Using something other than Claude Code? See
[other agent clients](#using-it-in-other-agent-clients).)*

```bash
claude plugin marketplace add https://github.com/JanCas/claude-skills --scope user
```

```bash
claude plugin install research-figures@DRL_skills --scope user
```

Restart Claude Code (or start a new session), then confirm:

```bash
claude plugin list
```

You should see `research-figures@DRL_skills`, version 1.0.0, enabled.

**Why the full HTTPS URL and not the `JanCas/claude-skills` shorthand.** The
shorthand picks its transport from your own `gh` config. If
`gh config get git_protocol --host github.com` returns `ssh` and you have not
added an SSH key to GitHub, the clone fails. The HTTPS URL needs no auth at all
for a public repo. The outcome is otherwise identical — the two just record
different `source` blocks in settings (`git`/`url` versus `github`/`repo`).

**Why `--scope user`.** It installs into your own `~/.claude/settings.json`, so
the skill follows you into every project and imposes nothing on anyone else.
Reach for `--scope project` only if the convention should bind one shared repo —
that writes into *that repo's* `.claude/settings.json` and applies to everyone
who clones it. The scope table further down has the details.

### Using it

There is nothing to invoke. The skill fires on its own during figure work — after
a plotting script runs, when a results directory has loose PNGs that need
organizing, or when someone asks which run produced a given figure. You can also
just ask for it directly: *"set up figure versioning in `results/`"*.

It costs about 240 tokens of always-on context; the full body (~2.7k) loads only
when it actually triggers.

### Getting updates

New and changed skills arrive when you refresh the marketplace:

```bash
claude plugin marketplace update DRL_skills
```

Restart afterwards. The marketplace serves whatever has been pushed to GitHub, so
if something looks missing, it may not be pushed yet.

## Plugins

| Plugin | Skills | What it covers |
| --- | --- | --- |
| `research-figures` | `figure-versioning` | Filing generated plots into numbered version folders with a `MANIFEST.md` and a rolled-up `INDEX.md`, so every figure traces back to the run that produced it. |

---

## Using it in a project

The reference version of the above, for binding the skills to a specific repo
rather than to yourself. Run these **from inside the target project's root**. No
clone of this repo required, on any machine.

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

Pick by what should own the decision. `user` when *you* want a skill available
everywhere you work — the right default for your own machine. `project` when the
*repo* should carry the convention, so everyone who clones it gets the same
skills; that is what the commands in this section do. `local` for a one-off you
do not want committed.

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

## Using it in other agent clients

`plugins/research-figures/` is a valid **Agent Plugins 1.0.0** package — the
vendor-neutral standard published in August 2026 by Anthropic, OpenAI, AWS,
Cursor, GitHub/Microsoft and Vercel. Clients that read it include ChatGPT,
Codex, Cursor, GitHub Copilot, VS Code and Kiro.

Point the client at **`plugins/research-figures/`** — the plugin root — or zip
that directory. Not the repo root: the standard has no marketplace concept, so
`marketplace.json` is ignored outside Claude Code and each plugin installs on its
own.

The skill needs no conversion. `SKILL.md` with `name`/`description` frontmatter
alongside `assets/` and `references/` is exactly what the standard specifies, so
the same directory serves both formats.

**Two caveats, both unverified here.** The package is checked against the
published JSON Schema, but has not been installed into a non-Claude client from
this repo. And ChatGPT Skills were limited to Business, Enterprise, Healthcare
and Edu workspaces as of July 2026 — not Free, Plus, or Pro. Check the client's
own docs for its install step, which varies (upload vs. repo reference).

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
│   └── marketplace.json          <- Claude Code marketplace (lists plugins)
├── LICENSE                       <- MIT
├── README.md
├── scripts/
│   ├── validate.py               <- checks both formats, and that they agree
│   └── plugin.schema.1.0.0.json  <- vendored Agent Plugins schema
└── plugins/
    └── research-figures/         <- one themed bundle = one Agent Plugin
        ├── plugin.json           <- Agent Plugins 1.0.0 manifest
        ├── .claude-plugin/
        │   └── plugin.json       <- Claude Code manifest
        └── skills/               <- shared by both formats
            └── figure-versioning/
                ├── SKILL.md
                ├── assets/
                └── references/
```

### Two manifests per plugin

Every plugin states its metadata twice, deliberately:

| File | Read by | Why it exists |
| --- | --- | --- |
| `plugin.json` (plugin root) | ChatGPT, Codex, Cursor, Copilot, VS Code, Kiro | The portable Agent Plugins 1.0.0 standard |
| `.claude-plugin/plugin.json` | Claude Code | Claude Code 2.1.227 does **not** read the root manifest — it fails with *"Expected .claude-plugin/marketplace.json or .claude-plugin/plugin.json"* |

This is what the standard's own migration guide prescribes: add the root manifest
without deleting the platform files. Delete `.claude-plugin/` and Claude Code
stops seeing the plugin; delete `plugin.json` and every other client does.

`skills/` is shared — both formats discover skills in the same place, so skill
directories are written once and never duplicated.

Note that `plugin.json` permits exactly ten top-level fields and rejects anything
else (`additionalProperties: false`), so Claude's `category` cannot live there —
it stays in the marketplace entry. `name` must also match the schema's pattern:
lowercase alphanumerics, dots and hyphens, starting and ending alphanumeric.

The cost of two manifests is that `name`, `version` and `description` appear in
three places counting the marketplace entry. That is what `scripts/validate.py`
is for.

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

1. Create `plugins/<name>/plugin.json` — the Agent Plugins manifest. `$schema`
   and `name` are the only required fields; `version`, `description`, `author`,
   `homepage`, `repository`, `license`, `keywords` and `extensions` are the rest
   of the permitted set.
2. Create `plugins/<name>/.claude-plugin/plugin.json` with the **same** `name`,
   `version` and `description`.
3. Add a matching entry to the `plugins` array in
   `.claude-plugin/marketplace.json` — `name`, `description`, `source`
   (`./plugins/<name>`), `category`.
4. Run `python3 scripts/validate.py`, then commit and push.

### This repo is public

Anything committed here is published. Skills often carry real numbers in their
examples — check `references/` and any worked examples for unpublished data
before pushing, and replace it with placeholders that keep the lesson intact.
`figure-versioning`'s worked example is genericized for exactly this reason.

### Validating

One command checks everything, from the repo root:

```bash
python3 scripts/validate.py
```

For every plugin it verifies:

- `plugin.json` against the vendored Agent Plugins 1.0.0 JSON Schema
  (`scripts/plugin.schema.1.0.0.json` — pinned, and the schema's `$schema` value
  is a `const` naming its own version, so the vendored copy cannot silently go
  stale)
- that `name`, `version`, `description` and `license` agree across both
  manifests, and that the description matches the marketplace entry
- that the marketplace `source` points where it claims
- that every skill has a `SKILL.md` whose frontmatter carries `name` and
  `description`, with `name` matching its directory
- `claude plugin validate --strict` on the repo and on each plugin

It needs `jsonschema` (`pip install jsonschema`); without it the schema check is
skipped with a note rather than silently passing.

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

---

## License

[MIT](LICENSE) — © 2026 Jan Luka Cas.

Use, copy, modify and redistribute freely; the only condition is that the
copyright notice travels with it. Both plugin manifests declare `"license":
"MIT"`, so clients that surface licence metadata pick it up without reading the
file.
