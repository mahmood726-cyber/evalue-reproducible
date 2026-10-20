# Preregistered validation plan — 2026-10-20

Written before numerical results. No results are implied by this plan.

## Scope and locked inputs

Execute the actual `evalue/index.html` classic scripts in document order, including local external dependencies, in Node with a minimal DOM. Invoke the page's `run()` and read its `__almLastEValue` accessor; do not substitute a reimplementation. Browser rendering is a separate host gate.

Inventory installed R packages before choosing exact versions. Lock the chosen R version and EValue, metadat, metafor and jsonlite versions in `versions.json` before generating references. Every R entry point must source the fail-closed version assertion. Missing versions stop validation; no fallback or automatic install.

Real-data corpus: every row of `metadat::dat.bcg` (binary counts tpos/tneg/cpos/cneg), transformed by `metafor::escalc` to RR and OR with normal 95% limits; run RR with rare=false and OR with rare=false/true. Every row of `metadat::dat.normand1999` (m1i/sd1i/n1i/m2i/sd2i/n2i), transformed to SMD with normal 95% limits; run SMD. Dataset structures are checked, not guessed or silently substituted. No clinical inference is intended from these computational examples.

Synthetic numerical grid: RR/OR/HR point values 0.2, 0.6, 1, 1.6, 2, 10; intervals [point/1.5, point*1.5] and no interval; both rare settings for OR/HR, rare=false for RR. SMD values -2, -0.5, 0, 0.5, 2; intervals [point-0.2, point+0.2] and no interval. Add explicit null-crossing RR [0.5,2] with point 1 and SMD [-1,1] with point 0, and degenerate RR [2,2].

Refusal probes: missing point, zero/negative ratio, nonnumeric/malformed point, partial/reversed/noncontaining CI, zero ratio limit, nonfinite input, overflowing SMD and unsupported measure. Also verify intentional blank CIs return null CI rather than 1. Assertions are exact for refusal, nulls and IDs.

## Oracle and comparisons

Use EValue::evalues.RR/OR/HR for ratio measures; use EValue::evalues.MD with sd=1 for standardized mean differences. Inspect installed help/source to determine its uncertainty convention before implementing the adapter. If the R MD API cannot represent arbitrary asymmetric limits, compare points with evalues.MD and CI endpoints with evalues.MD separately; disclose this convention and do not claim equivalence to its se-based interval. Compare point E-value, CI E-value and transformed RR point/lower/upper where available in the package output.

For each finite numerical quantity require |app-R|/max(1,|R|) <= 1e-9. No iterative exceptions are planned. Require identical configuration IDs, lengths, quantity keys, null patterns and acceptance states; reject duplicate IDs, missing/extra records and nonfinite values. Print passed/expected, never reduce the denominator after failure.

Run original and fixed snapshots separately; preserve any failing evidence before app changes. If no fix is justified, report original only and explicitly state that no fixed snapshot exists.

## Required safeguards

After a successful baseline, perturb one app point result by 1e-8*max(1,abs(R)); comparison must fail. Independently remove one configuration; comparison must fail. Also test hash tampering, duplicate IDs, nonfinite values and version mismatch fail closed. Keep mutant outputs separate from baseline.

## Explicit scope gap

The page exposes no OLS, RD, confounded_meta or sens_plot controls/engines. Their availability in EValue does not establish app support. Record installed API availability, but do not count unsupported functionality as validated. Completion of the brief's broader full R validation requirement remains blocked unless the coordinator accepts the narrower scope or those features are separately implemented, preregistered and tested.

## Archive and manuscript gates

Hash exact source bytes, corpus, scripts, pinned versions and references. `Rscript validate.R` must check integrity and versions, regenerate independent references, replay the page and run safeguards. Fresh git-archive replay, official journal criteria/DOI title verification and real Edge figures remain host tasks. Main text <=1000 words; abstract <=300. Preserve exact paper 22 author/CRediT assignments. No invented counts, browser captures, clinical claims or completed author contributions.
