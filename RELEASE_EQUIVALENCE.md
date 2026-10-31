# Equivalence of the archived release pages with allmeta v1.9.0 and v1.8.0

## allmeta v1.9.0 (validated release)

allmeta v1.9.0: tag `v1.9.0` (tag object `7c846614080ad3167f8890de46460818d837e645`), commit
`d38d3fd70656f3fedfa03916573fe0bf904f5e9c`, DOI 10.5281/zenodo.23833871 (the Zenodo record reports version v1.9.0). Its parent
is `6ce55eb9232b17b6fb0948ec8217d653acf28b57` (allmeta PR #236, the 1/RR marker label), validated in run 3
(`app-main-6ce55eb/`, PREREG_ADDENDUM_4.md). The release commit changes `CHANGELOG.md`, `CITATION.cff` and
`shared/build-info.js`; only the last is among the page's files.

All 7 files in `app-v1.9.0/` are byte-identical to the v1.9.0 blobs (`git hash-object` equals the blob id of
`d38d3fd:<path>`; `provenance-release-v1.9.0.json`). Compared with `app-main-6ce55eb/`, only `shared/build-info.js` differs
(build stamp v1.9.0/6ce55eb; not displayed in the validated output). Compared with `app-v1.8.0/`, `evalue/index.html` (the
1/RR label) and `shared/build-info.js` differ; the engine `shared/evalue.js` is identical.

Replay on the v1.9.0 bytes (run 4, PREREG_ADDENDUM_5.md, `evidence/fresh/run-4-release-v1.9.0/`, 31 Oct 2026, Node v24.13.0,
R 4.6.0, EValue 4.1.4): **22,428/22,428** checks on 3,738 configurations (largest normalized difference 4.86e-15), refusals
26/26, and the output equals the original page's exactly (`release-v1.9.0-vs-original.json`). Figures 1 and 2 with the
1/RR label (`figures/main-6ce55eb/`) were captured from `app-main-6ce55eb/`, whose rendering files are byte-identical to
v1.9.0. All of the archive's comparison results therefore apply unchanged to allmeta v1.9.0.

## allmeta v1.8.0

allmeta v1.8.0: tag `v1.8.0`, commit `1cb3f8409c7af75ed41f7e1811f9c502f900fc79`, DOI 10.5281/zenodo.23515177.
The page was first validated at commit `74ff0a7d2263ca8e0c07419888152ea156036abd` (run 1, `app-original/`), which is an
ancestor of v1.8.0. It was then validated directly on the v1.8.0 tag bytes (run 2, `app-v1.8.0/`, PREREG_ADDENDUM_3.md).

All 7 files in `app-v1.8.0/` are byte-identical to the v1.8.0 blobs (`git hash-object` equals the blob id of
`1cb3f84:<path>`). Nothing was replaced.

`app-original/` is kept unchanged as the run-1 record. Its files differ from v1.8.0 as follows:

| File | Difference from v1.8.0 | Effect on results |
|---|---|---|
| `evalue/index.html` | CRLF line endings from a `core.autocrlf` working tree; LF content equals the v1.8.0 blob `ab17be6378827a743689d125452870b7e10c8908` | none (line endings only) |
| `hub/app-style.css` | CRLF line endings; LF content equals the v1.8.0 blob `24574bf090eaa4ec0ab3c24aa965069f1ca7d4ea` | none (CSS) |
| `shared/forced-colors.css` | CRLF line endings; LF content equals the v1.8.0 blob `abbfcf01b6b7c4fd2e2f550d8b034a0b97c71466` | none (CSS) |
| `shared/build-info.js` | 74ff0a7 build stamp (v1.7.0, 7899ce5); v1.8.0 has v1.8.0, 42a94da | none (build stamp; not displayed in the validated output) |

`shared/evalue.js` (the engine), `hub/shared/a11y-landmarks.js` and `LICENSE` are byte-identical to v1.8.0 in both
snapshots. The planted-defect copies under `evidence/fresh/*/mutant-app/` are deliberately modified (`shared/evalue.js`
HR constant) and are not release snapshots.

Check by execution (21 Oct 2026, Node v24.13.0, Windows): `analysis/replay.cjs` was re-run, with the archived
`data/corpus.json` and the archive's refusal probes, on the 7 page files read with `git cat-file blob 1cb3f84:<path>`, and
on `app-original/`. The results were compared with the archived EValue reference
`evidence/fresh/run-2-release-v1.8.0/reference.csv` using `compare()` in `analysis/pipeline.py`. The R reference was not
re-run.

- v1.8.0 bytes: **22,428/22,428** checks pass on 3,738 configurations (largest normalized difference 4.86e-15); refusals
  26/26. The `rows` are identical to `evidence/fresh/run-2-release-v1.8.0/release-app.json` and the refusal rows to
  `release-refusals-app.json`. SHA-256 of the canonical JSON of `rows`:
  `bba55cc0716e22526ffad7f14f0c5467bd30b2195308cfa7669b2a038e033958` (new and archived). The only other difference in
  the file is the `runtime` field (Node v24.13.0 here, v24.22.0 archived).
- `app-original/`: 22,428/22,428, refusals 26/26, `rows` identical to `full-app.json` (same SHA-256 as above).
- The release output equals the original output exactly.

All of the archive's comparison results therefore apply unchanged to allmeta v1.8.0.
