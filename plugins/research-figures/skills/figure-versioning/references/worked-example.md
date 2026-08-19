# Worked example: a column-validation figure directory

A six-version directory, at `results/breakthrough/column_validation/`. It is
worth reading because it shows the two things the templates cannot: how much
detail a configuration table needs to be useful a month later, and what a version
history looks like when it is *not* a clean progression.

> The numbers, case names, and commit hashes below are illustrative placeholders
> chosen to be internally consistent (a monovalent sorbate, MW 23 g/mol). They
> are not measurements. What is worth copying is the *shape* of the index and the
> manifests, not the values in them.

The directory holds validation of a sorption column model against four published
breakthrough experiments, each run at two feed conditions — eight cases in all.
Its layout:

```text
results/breakthrough/column_validation/
  figures/
    INDEX.md
    v1/ MANIFEST.md + 1 png
    v2/ MANIFEST.md + 5 png
    v3/ MANIFEST.md + 3 png
    v4/ MANIFEST.md + 8 png
    v5/ MANIFEST.md + 8 png
    v6/ MANIFEST.md + 1 png
  validation_metrics.csv        <- data, not versioned
  validation_results.json
  floor_5mg_g/                  <- one run's data outputs
  mole_balance/
  case_a_floor/
```

## The index

Its discriminating columns are `Floor` and `Case C feed C0` — the two settings
that actually moved across versions in this study. Nothing else earned a column.

```markdown
| Version | Date | Scope | Floor | Case C feed C0 | Figures | Status |
|---|---|---|---|---|---:|---|
| [v1](v1/) | 2026-03-04 | Case A only | 5 mg/g | n/a | 1 | historical |
| [v2](v2/) | 2026-03-05 | Case C only | 0 | 300 mg/L assumed | 5 | **superseded** |
| [v3](v3/) | 2026-03-05 | Case B sensitivities | 5 mg/g | n/a | 3 | current for that study |
| [v4](v4/) | 2026-03-17 | All eight cases | 0 | 182.6 mg/L from pH | 8 | **current, zero floor** |
| [v5](v5/) | 2026-03-17 | All eight cases | 5 mg/g | 182.6 mg/L from pH | 8 | **current, 5 mg/g floor** |
| [v6](v6/) | 2026-03-17 | Mole balance | derived | 182.6 mg/L from pH | 1 | **current** |
```

Three things to notice:

- **Four versions are simultaneously "current."** v3 is current for the Case B
  sensitivity study; v4 and v5 are both current because they are the two arms of
  a deliberate floor comparison a reader may want side by side; v6 is current
  post-processing. Only v2 is superseded. Forcing a single "latest" would have
  destroyed real information.
- **`n/a` appears only twice.** Had it appeared in five of six rows, that column
  belonged in the manifests instead.
- **Status carries the qualifier**, not just the word — `current, 5 mg/g floor`
  tells a reader which of two current versions they want.

Its prose section does the work the table cannot:

```markdown
- **v1 → v2 → v3** are three separate single-study runs from early March, not a
  progression of the same figures. Each covers different cases.
- **v2 → v4** is the substantive correction: Case C's feed concentration moved
  from an assumed 300 mg/L to 182.6 mg/L, derived from the paper's own reported
  pH 11.9 via `[M+] = [OH-]`. Case C RMSE improved `0.3140 → 0.1472` and R2
  `0.31 → 0.79`. The v2 breakthrough panels are superseded; its Figure 6
  equilibrium diagnostics are not affected.
- **v4 → v5** changes only the equilibrium floor, `0 → 5 mg/g`. Its effect is
  small: the largest metric change is Case A high-pH, RMSE `0.1204 → 0.1038`.
- **v6** is post-processing over v4 and v5, not a new solve.
```

The v2 entry is the model for a supersession note: it says what was wrong, what
replaced it, how much it mattered in metric terms, and — crucially — that
*part* of v2 survives. A blanket "superseded" would have implied the Figure 6
diagnostics were also invalid.

## A manifest of a fresh run

`v5/MANIFEST.md`:

````markdown
# v5 — Full eight-case suite, 5 mg/g floor, corrected Case C feed

Generated: 2026-03-17  
Git commit: `a1b2c3d4e`  
Data and metrics: [`../../floor_5mg_g/`](../../floor_5mg_g/)

## Configuration

| Setting | Value |
|---|---|
| Cases | all eight |
| Equilibrium floor | 5 mg/g = 0.2174 mol/kg |
| Chemistry closure | measured titration for Case A; ideal water elsewhere |
| Case C feed C0 | 7.94 mol/m3 = 182.6 mg/L, derived from reported pH 11.9 |

## Produced by

```bash
validate_columns.py --equilibrium-floor-mg-g 5.0 --output-dir results/breakthrough/column_validation/floor_5mg_g
```

## Figures

- `case_a_validation.png`
- ... (eight in total)

## Note

Differs from v4 only in the equilibrium floor. Direct comparison is in floor_5mg_g/README.md.
````

Four rows, and each one earns its place. Two give values in both the flag's units
and the model's internal units, so a reader checking the code against the table
does not have to convert. One records where a derived number came from. One
states a closure that applies to some cases and not others — exactly the kind of
thing that is obvious while running and unrecoverable later.

The note is one sentence because one sentence is all the version needs: it names
the single axis of difference from v4 and points at the comparison.

## A manifest of derived figures

`v6/MANIFEST.md` covers a figure that came from post-processing, not a solve:

```markdown
| Setting | Value |
|---|---|
| Cases | all eight |
| Derived from | the v4 and v5 curve data; no new solve |
| Plotted run | the 5 mg/g floor set (v5) |
| Case C feed C0 | 7.94 mol/m3 = 182.6 mg/L |
```

with the note: *"Post-processing of v4/v5 outputs, not an independent simulation.
Regenerate whenever v4 or v5 is regenerated."*

That last sentence is the whole reason to flag derived versions. Nothing in the
directory structure records that v6 depends on v4 and v5, so regenerating them
would silently leave v6 stale. The manifest is the only place that dependency can
live.

## Where the honesty shows

`v6` records `Git commit: unknown`. The figures were made from uncommitted work
and the exact commit was not recoverable. Writing a nearby plausible SHA would
have been worse than useless — it would have sent a future reader to code that
did not produce the figure. `unknown` is a real answer.
