# <study or model name> figure versions

Every graph produced from <the thing> lives here, in a numbered version folder.
Nothing is written loose into a results directory.

**A version is one set of graphs generated under one configuration.** Version
numbers are chronological and mean nothing beyond creation order — `v5` is not
"better" than `v3`, it is only later. When you generate graphs under a
configuration that differs from the newest version, create the next `vN` rather
than overwriting.

The convention, including what counts as a configuration change, is in the
`figure-versioning` skill.

| Version | Date | Scope | <config axis 1> | <config axis 2> | Figures | Status |
|---|---|---|---|---|---:|---|
| [v1](v1/) | <YYYY-MM-DD> | <what it covers> | <value> | <value> | <count> | <status> |
| [v2](v2/) | <YYYY-MM-DD> | <what it covers> | <value> | <value> | <count> | <status> |

## What changed between versions

- **v1 → v2** <what actually changed, and its numerical effect where there is one:
  `RMSE 0.3140 → 0.1472`. Say plainly when two adjacent versions are unrelated
  runs rather than a progression.>

## Reading a version

Each folder carries a `MANIFEST.md` giving the configuration that produced it,
the command that generated it, the git commit, and a link back to the data that
accompanies those figures. Data files stay with their study directories; only
graphs are versioned here.
