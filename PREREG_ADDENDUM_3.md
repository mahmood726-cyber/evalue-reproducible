# Addendum 3: release snapshot v1.8.0 (2026-10-21; written before any release-page result)

allmeta v1.8.0 was tagged after run 1, at commit 1cb3f8409c7af75ed41f7e1811f9c502f900fc79 (origin/main, "release: allmeta v1.8.0"). The validated commit 74ff0a7 is an ancestor of the tag. Of the seven files the page loads (`app-original/`), `git diff 74ff0a7 v1.8.0` changes only `shared/build-info.js`, where the version stamp moves from v1.7.0/7899ce5 to v1.8.0/42a94da. Three archived files (`evalue/index.html`, `hub/app-style.css`, `shared/forced-colors.css`) have CRLF line endings because they were copied from a `core.autocrlf=true` working tree. Their LF-normalised bytes equal the git blobs, and those blobs are the same at both commits.

## Plan (locked now)

- Add `app-v1.8.0/` with the same seven paths, written from the tag's git blob bytes (`git show v1.8.0:<path>`). `app-original/` is kept unchanged.
- `validate.R` (via `pipeline.py full`) also replays the full corpus through `app-v1.8.0/evalue/index.html` against the same fresh EValue reference. The quantities, the 1e-9 tolerance relative to max(1,|R|), the fixed denominators and the refusal probes are unchanged. The expected result is 22,428/22,428 checks on 3,738 configurations and 26/26 refusals. Any failure fails the run.
- The release page's numeric output must also be identical to the original page's (exact equality of every value, which is stronger than the tolerance). This is recorded in `release-vs-original.json`.
- Planted defects are unchanged and still run against the original page, plus one new check: a release-snapshot hash mismatch must fail `verify` (covered by the existing changed-file safeguard over the whole inventory).
- The figures are not recaptured. The page displays no version stamp in the captured region, and the page/engine bytes that render it are unchanged. This is stated in the figure legends.
- The paper reports the release (v1.8.0, commit 1cb3f84) as the cited version, with the validation counts from the release replay. The original-page result is kept in the archive.
