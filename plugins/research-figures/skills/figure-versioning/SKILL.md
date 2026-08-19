---
name: figure-versioning
description: Convention for filing generated figures into numbered version folders (figures/vN/) with a MANIFEST.md and a rolled-up INDEX.md, inside any results directory. Use this whenever you generate, regenerate, or reorganize plots that a report or paper will cite — after running a validation/sensitivity/sweep script, when a model parameter or input changed and the figures need to be redone, when a results directory has loose PNG/SVG files that need to be brought under version control, when someone asks "which run produced this figure?", or when a report link needs to point at the right figure version. Also use it when asked to set up figure versioning, bump a figure version, write a figure manifest, or check whether a change warrants a new version.
---

# Figure versioning

Figures get regenerated constantly, and a figure that no longer matches the
numbers in the report it illustrates is worse than no figure at all. This
convention makes every graph traceable to the configuration that produced it, so
a reader can always answer "what settings gave me this curve?" without guessing.

This is a convention, not a code feature. No script enforces it. Scripts write
their figures wherever their `--output-dir` points; whoever runs them then files
those figures under the next version. See "Why this isn't automated" at the end —
that reasoning matters, because a request to "just make the script do it" will
come up and the answer is deliberate.

## The rule

> **A version is one set of graphs generated under one configuration.**
> When you generate graphs under a configuration that differs from the newest
> version, create the next `vN` folder. Never overwrite an existing version.

Version numbers are chronological only. `v5` is not better than `v3`, it is later.
Different `vN` folders are frequently different *studies*, not successive drafts
of the same figure.

## Layout

Applies inside any results directory — a study folder, a paper's figure set, a
sweep's output directory. Substitute `<results-dir>` for whichever one you are
working in.

```text
<results-dir>/
  figures/
    INDEX.md          <- table of every version, newest last
    v1/
      MANIFEST.md     <- config, command, commit, file list, note
      <figures>.png
    v2/
    ...
  <data outputs>.csv          <- data stays with its study directory
  <data outputs>.json
  <per-run subdirectories>/
```

Only graphs are versioned. CSV, JSON, NPZ, and other data outputs stay in the
study directory that produced them, and each `MANIFEST.md` links back to them.
Version folders stay small and browsable, and the data does not get duplicated
once per version.

## What counts as a configuration change

Bump the version for any of these:

- a model parameter changed (a rate constant, a capacity, a floor, a fitted coefficient)
- an input changed (feed composition, operating condition, geometry, boundary condition)
- an assumption or closure changed (which sub-model, which correlation, which activity treatment)
- the code changed in a way that moves the curves
- the case list changed (different experiments or scenarios included)
- the plotted quantity or the figure layout changed

Do **not** bump for: re-running an identical configuration, editing a caption or
axis label without regenerating, or fixing a typo in a manifest. Overwrite in
place instead.

If you are unsure whether something counts, bump. Version folders are cheap; a
silently overwritten figure that no longer matches its report is not.

## Procedure

1. Run whatever script generates the figures.
2. Find the current highest version and the commit you are on:

   ```bash
   ls -d <results-dir>/figures/v*/ 2>/dev/null | sort -V | tail -1; git rev-parse --short HEAD
   ```

3. Create `<results-dir>/figures/vN/` where `N` is one past that highest.
4. Move the generated graphs in. Leave CSV/JSON/NPZ in the study directory.
5. Write `figures/vN/MANIFEST.md` from `assets/MANIFEST_TEMPLATE.md`.
6. Add a row to `figures/INDEX.md` and describe the change in its
   "What changed between versions" section. If `INDEX.md` does not exist yet,
   start it from `assets/INDEX_TEMPLATE.md`.
7. If a version is superseded, mark it in `INDEX.md` and in its own `MANIFEST.md`.
   Do not delete it — a superseded figure is still the evidence for whatever
   report cited it at the time.
8. Update any report that embeds the figure to point at the new path.

## Writing the manifest

`assets/MANIFEST_TEMPLATE.md` has the skeleton. The part that takes judgement is
the configuration table, because its rows are domain-specific. Include:

- **every setting that differs from the previous version** — this is what makes
  a diff between two manifests readable, and it is the whole point of the table
- **the settings a reader needs to interpret the figures at all**, even if
  unchanged (which cases are plotted, which closure is in force)
- **the provenance of any non-obvious number** — if a value was derived rather
  than taken from a source, say from what. A row reading
  `Feed C0 | 182.6 mg/L, derived from the paper's reported pH 11.9 via [M+]=[OH-]`
  is worth far more later than one reading `Feed C0 | 182.6 mg/L`.

Leave out settings that are constant across every version and irrelevant to
reading the plot. A table of thirty rows nobody reads defeats the purpose.

Record the command verbatim — the actual invocation with its real flags, not a
cleaned-up idealization — so the run can be reproduced. If the figures came from
post-processing earlier versions rather than a fresh solve, say so in the note
and name the versions it derives from; that dependency is invisible otherwise and
means the derived version goes stale when its sources are regenerated.

If the git commit is not knowable (uncommitted work, unclear provenance), write
`unknown` rather than a plausible guess.

## Writing the index

`assets/INDEX_TEMPLATE.md` has the skeleton. The table columns are:

`Version | Date | Scope | <discriminating config columns> | Figures | Status`

Choose the discriminating columns to be the one to three settings that actually
vary across versions in this directory — the axes along which the study moved.
For a floor-value study that is the floor; for a mesh study it is the mesh; for a
multi-study directory it may be nothing beyond Scope. Do not carry a column that
reads `n/a` for most rows; that is a signal it belongs in the individual
manifests instead.

`Status` is free text, not a fixed vocabulary: `current`, `superseded`,
`historical`, `current for that study`. A directory can legitimately hold several
"current" versions at once when they cover different studies or different
parameter choices a reader may want to compare.

The "What changed between versions" prose section carries what the table cannot:
which transitions are real corrections versus unrelated runs that merely sit next
to each other, and what the numerical effect of a change was. When a bump
measurably moved a metric, quote the before and after — `RMSE 0.3140 → 0.1472` —
because that is what tells a future reader whether the change mattered.

## Referring to figures from reports

Reports link into a specific version, never to a floating "latest":

```markdown
![Validation](figures/v4/case_a_validation.png)
```

A report that cites metrics from a given run should link the figure version from
that same run, so the numbers and the picture cannot drift apart. When a report
is updated to a newer run, update both together.

## Adopting the convention in a directory that has none

When a results directory has loose figures written straight into it:

1. Ask whether those existing figures came from one configuration or several.
   Do not merge distinct runs into a single `v1` to tidy up — that destroys the
   provenance the convention exists to preserve.
2. Create a version folder per distinct configuration you can identify, oldest
   first, and move the graphs in. Use file timestamps and git history to date them.
3. Write each `MANIFEST.md`, reconstructing what you can. For anything you cannot
   recover, write `unknown` — an honest gap is usable; a guess that looks
   authoritative is not.
4. Write `INDEX.md`.
5. Leave the data files where they are.
6. Grep the repo for links to the old flat paths and repoint them.

## Why this isn't automated

Auto-incrementing on every execution produces a folder per run, including the
many reruns that change nothing. Deciding that a configuration is meaningfully
different is a judgement about the science, which is why it sits with the person
or agent doing the work rather than in the script.

A worked example — a six-version directory with its index and two of its
manifests — is in `references/worked-example.md`. Read it when you want to see
how much detail a good manifest actually carries.
