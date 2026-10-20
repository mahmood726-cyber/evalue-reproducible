# E-value reproducibility archive — paper 22 (allmeta `evalue/`)

Validation archive for the allmeta E-value page (VanderWeele & Ding E-value for RR, OR, HR and standardized mean differences) against the CRAN R package **EValue 4.1.4**. It is local only. There is no release yet: metadata carry `<ALLMETA_RELEASE>` / `<ALLMETA_RELEASE_DOI>` placeholders.

## Result

| | Original page (allmeta 74ff0a7) |
|---|---|
| Configurations | 3,738 (2,413 real-data from 30 metadat datasets + 1,325 synthetic) |
| Checks (acceptance + 5 quantities each) | **22,428 / 22,428** |
| Largest normalized difference | 4.9 × 10⁻¹⁵ (tolerance 1 × 10⁻⁹ relative to max(1, \|R\|)) |
| Refusal probes | 26 / 26 (13 invalid inputs) |
| Planted defects | all rejected: +1e-8 relative perturbation (22,427/22,428), dropped configuration, duplicate ID, nonfinite value, perturbed HR constant in the app source (21,691/22,428) |
| Archive safeguards | 4 / 4 (changed, missing, extra file; wrong R version) |

No app defect was found, so there is no fixed snapshot and no before/after comparison. The quantities checked are the point E-value, the CI E-value (limit nearest the null; 1 if the interval crosses the null) and the approximate RR with its limits. Evidence: `evidence/fresh/run-1-original-page/` (`summary.json`, `reference.csv`, `full-app.json`, `safeguards.json`, `mutant-summary.json`, `refusals-summary.json`, `validate-stdout.log`, and `reference.csv.session.txt` with the R sessionInfo).

## One-command validation

```text
set R_LIBS_USER=<library containing EValue 4.1.4>
Rscript --vanilla validate.R < NUL
```

Requirements: R 4.6.0, EValue 4.1.4, metadat 1.6.0 and metafor 5.2.1. Every R script asserts these exactly and stops on any mismatch. Python 3 and Node.js (v24 used) are also needed. `RSCRIPT` and `PYTHON` may point to the executables. Nothing is installed and no network is used.

The validator then:
1. checks the SHA-256 inventory (`SOURCE_SHA256.json`);
2. regenerates the real-data corpus from metadat and requires byte identity with `data/real-corpus.csv` and `data/corpus.json`;
3. computes fresh EValue references (`analysis/reference.R`);
4. executes the archived page's scripts in document order in Node (`analysis/replay.cjs`, simulated DOM, the page's own click handler and result accessor);
5. compares with fixed denominators and prints N/N;
6. runs the planted defects, refusal probes and archive safeguards.

Output goes to `.validate-work/`. If that directory already exists, the run is refused; move it aside first.

## Contents

- `PREREG.md`, `PREREG_ADDENDUM.md`, `PREREG_ADDENDUM_2.md`: the plan, written and committed (ea69964) before any EValue corpus result. Addendum 2 widened the real-data corpus to 30 datasets and removed a no-op `sd=1` argument from the MD adapter.
- `app-original/`: page, engine (`shared/evalue.js`) and local dependencies, byte-identical to allmeta commit 74ff0a7d2263ca8e0c07419888152ea156036abd (`provenance.json`, `provenance-host.json`). The bundled `build-info.js` still says v1.7.0. v1.8.0 was not tagged on 20 Oct 2026.
- `data/`: `real-corpus.csv`, `corpus.json`, `oracle-input.csv`, and the exported source datasets in `data/sources/`.
- `analysis/`: corpus generator, EValue adapter, Node replay, comparator/safeguards (`pipeline.py`), `verify_archive.py`, `test_safeguards.py`, version gate.
- `figures/`: Figure 1 (dat.bcg trial 1, RR) and Figure 2 (dat.normand1999 study 1, SMD), captured from the archived page in Microsoft Edge 155 (headless, Playwright-core 1.59.1). Included are the raw PNGs, the RGB/LZW/300-dpi TIFFs and `capture.json`. The capture asserts that the browser's values equal the fresh EValue reference within 1e-9. `verification.json` contains the PIL checks. `tools/` holds the capture and conversion scripts as run from the workspace, plus the npm lock.
- `evidence/local/`: earlier offline-session evidence (an inherited 13-case fixture, 78/78, and the 121-input pilot corpus). It is superseded by `evidence/fresh/` and kept for provenance.
- `references/`: the reference ledger, author assignment and wording rules.
- `publication/`: manuscript working files.

## Scope and limits

- **Methods covered:** EValue `evalues.RR`, `evalues.OR` and `evalues.HR` (rare and common outcome), and `evalues.MD` for standardized differences. The page offers no OLS, risk-difference or meta-analytic (`confounded_meta`, `sens_plot`) E-values, so none is validated or claimed.
- **SMD intervals:** the page transforms each user-supplied limit with exp(0.91·d). The counted comparison applies `evalues.MD` to each limit in the same way. EValue's own se-based interval uses exp(0.91·d ± 1.78·se); compared with that, the page's RR limits differ by up to 0.85% on the real-data rows (`smd-se-convention.json`, descriptive only, not counted). The difference comes from the rounded 1.78 versus 0.91 × 1.96 = 1.7836.
- **Real-data inputs:** individual study estimates computed with metafor `escalc` (add 0.5 to zero cells only; SMD bias-corrected with Wald limits). These are numerical test inputs, not clinical or pooled analyses. Rows with missing raw data are excluded by the preregistered rule: 24 binary and 40 SMD row-analyses in 5 datasets, with per-dataset counts in `corpus.log`. HR is tested only on synthetic inputs.
- **Node replay vs browser:** the counted checks run the page script on a simulated document. Real-browser behaviour is shown only for the two figure inputs, in Edge 155 on Windows 10. Other browsers are untested.
- **Oracle provenance:** EValue 4.1.4 is the CRAN Windows binary, built under R 4.6.1 and run under R 4.6.0. R prints a "built under" warning, which is recorded and does not affect validity.

## Licence and citation

Archive tooling is MIT, and the allmeta snapshot keeps its MIT licence. Datasets come from metadat with their original attributions. See `CITATION.cff`. Cite the EValue package and VanderWeele & Ding (2017).
