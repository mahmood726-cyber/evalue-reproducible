# Equivalence of the archived release page with allmeta v1.8.0

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
