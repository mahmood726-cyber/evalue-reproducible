# Addendum 5: release snapshot v1.9.0 (2026-10-31; written before any release-page result)

allmeta v1.9.0 was tagged at commit d38d3fd70656f3fedfa03916573fe0bf904f5e9c ("release: allmeta v1.9.0", 2026-10-31 09:41:38 +0000; annotated tag object 7c846614080ad3167f8890de46460818d837e645), DOI 10.5281/zenodo.23833871 (the Zenodo record reports version v1.9.0). Its only parent is 6ce55eb, the commit replayed in run 3 (`app-main-6ce55eb/`, PREREG_ADDENDUM_4.md). Source inspection only: `git diff 6ce55eb d38d3fd` changes `CHANGELOG.md`, `CITATION.cff` and `shared/build-info.js`. Of these, only `shared/build-info.js` is among the seven files the page loads; its version stamp moves from v1.8.0/42a94da to v1.9.0/6ce55eb.

## Plan (locked now)

- Add `app-v1.9.0/` with the same seven paths, written from the tag commit's git blob bytes (`git cat-file blob d38d3fd:<path>`), with `provenance-release-v1.9.0.json` giving each blob id and SHA-256 and whether each file is byte-identical to `app-main-6ce55eb/` and to `app-v1.8.0/`. Expected: only `shared/build-info.js` differs from `app-main-6ce55eb/`, and only `evalue/index.html` and `shared/build-info.js` differ from `app-v1.8.0/`. The earlier snapshots are kept unchanged.
- `validate.R` (via `pipeline.py full`) additionally replays the full corpus and the refusal probes through `app-v1.9.0/evalue/index.html` against the same fresh EValue reference, after the 6ce55eb replay. Quantities, tolerance, fixed denominators and probes are unchanged. The run output is kept in `evidence/fresh/run-4-release-v1.9.0/`.
- Expected outcome: **22,428/22,428** checks on 3,738 configurations, **26/26** refusals, and output **exactly equal** to the original page's. Planted defects are still rejected and the archive safeguards still pass 9/9.
- The figures are not re-captured. The page displays no version stamp, and the rendering files are byte-identical to `app-main-6ce55eb/`, from which `figures/main-6ce55eb/` was captured.
- The archive then names v1.9.0 (tag, commit d38d3fd, DOI 10.5281/zenodo.23833871) as the validated release in README.md, CITATION.cff, .zenodo.json and RELEASE_EQUIVALENCE.md, keeping the v1.8.0 record. `analysis/verify_archive.py` requires these identifiers. After re-pinning, the one-command validation is run end to end, and one defect is planted afterwards and must be refused.

## What counts as failure

Any of: a snapshot file whose `git hash-object` differs from its d38d3fd blob; a file other than `shared/build-info.js` differing from `app-main-6ce55eb/`; fewer than 22,428/22,428 checks or 26/26 refusals for the v1.9.0 page; any output row not exactly equal to the original page's; a planted defect or safeguard not rejected; the full validation not exiting 0; the post-hoc planted defect not refused. A failure is reported as found and not repaired inside this addendum.
