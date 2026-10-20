# E-value reproducibility archive — paper 22

**Incomplete validation archive; not ready for publication.** This directory is local only and is not a git repository. No release, DOI, browser evidence or fresh installed-EValue agreement is claimed.

The original allmeta page and its local dependencies are preserved byte for byte in `app-original/`; full checkout identity and each snapshot hash are in `provenance.json`. The checkout is newer than the bundled build-info stamp. Tag v1.8.0 is not locally available. Host fetch/tag reconciliation and a complete rerun are required before a release claim.

## Evidence available

- `PREREG.md` and `PREREG_ADDENDUM.md`: prespecified inputs, tolerances, safeguards and scope.
- `data/`: original installed-package datasets, 48 derived real-data configurations and 73 synthetic configurations, 121 total.
- `evidence/local/inherited-summary.json`: 78/78 checks (13 acceptance states and 65 quantities/nulls) against a pre-existing synthetic repository fixture.
- `evidence/local/refusals-summary.json`: 26/26 checks on 13 invalid-input probes.
- `evidence/local/comparator-safeguards.json`: numerical perturbation, dropped configuration, duplicate ID and nonfinite value all rejected.
- `evidence/local/corpus-execution.json`: all 121 configurations execute; this is NOT an R parity count.

The fixture reports EValue source-function execution at a pinned upstream commit, not an installed package. Its supplied source generator is retained as `.R.txt` provenance, not executed here. Do not present inherited reference checks as fresh R validation.

## One-command full validator

From this directory, with R 4.6.0, EValue 4.1.4, metadat 1.6.0 and metafor 5.2.1 installed:

```text
Rscript --vanilla validate.R < NUL
```

Python 3 and Node are also required (local versions recorded in `evidence/environment.json`). `RSCRIPT`, `PYTHON` and `R_LIBS_USER` may select executables/library locations; they cannot bypass exact R package pins. No command installs packages or uses the network.

The validator refuses missing/wrong versions, checks the complete SHA-256 source inventory, generates fresh corpus and references, executes all page scripts in document order, compares fixed expected IDs/quantity keys/nulls and prints passed/expected, and runs numerical/drop/duplicate/nonfinite safeguards. Existing `.validate-work` is refused; preserve it elsewhere before retry. New outputs go only in `.validate-work`.

The EValue reference adapter is **prepared but unexecuted**. Host review of installed function signatures and the expected two-row/three-column result layout is required. SMD point and each endpoint are transformed independently with evalues.MD(sd=1); this does not claim equivalence to its se-based interval constructor.

Local-only replay: `python -B analysis/pipeline.py local`. Integrity: `python -B analysis/pipeline.py verify`. These do not complete the fresh R gate. Regenerating evidence intentionally invalidates `SOURCE_SHA256.json`; review changes before regenerating the inventory.

## Scope and limits

The page supports RR, OR, HR and SMD. It does not offer OLS, RD, confounded_meta or sens_plot. The broad brief's corresponding requirement remains unmet. No feature expansion was authorized by an explicit specification; unsupported functions are not counted as passing tests.

Real-data values are individual study effect estimates derived using metafor, not pooled effects or meta-analytic E-values. Binary zero-cell correction is 0.5 for affected tables only. The source dataset yielded a warning about large SMDs; none were removed after seeing results. These are numerical probes, not clinical analyses.

Node uses a minimal simulated DOM. It checks computation and refusal cleanup, but does not establish real browser input parsing, accessibility, rendering, screenshots or offline operation in a browser. Real-page Edge captures and TIFF verification are outstanding host work. The original snapshot has not been changed; there is no fixed version or original-versus-fixed improvement claim.

See the workspace `HOST_STEPS.md`, `STATUS.md`, `JOURNAL.md` and manuscript trace for remaining gates. A filesystem replay is not a committed `git archive` replay.

## Licensing and citation

The allmeta snapshot includes its original MIT license. Dataset sources remain metadat datasets with their package/source attribution; study provenance is retained in the exported rows. Cite the EValue package and method paper after live bibliographic verification. Metadata contains `<ALLMETA_RELEASE>` and `<ALLMETA_RELEASE_DOI>` intentionally; no DOI has been minted.
