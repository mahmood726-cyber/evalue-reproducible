# Changelog

## 1.0.0

Initial reproducibility archive for the paper 22 validation of the allmeta E-value page against EValue 4.1.4 (22,428/22,428 checks on 3,738 configurations, 26/26 refusals, no app defect). The allmeta release identifiers are filled: v1.8.0 (tag commit 1cb3f84, DOI 10.5281/zenodo.23515177). The archive version in CITATION.cff and .zenodo.json is 1.0.0; it previously carried the allmeta release token. RELEASE_EQUIVALENCE.md records that `app-v1.8.0/` is byte-identical to the v1.8.0 blobs, and that replaying the corpus on those bytes reproduces the archived rows exactly. The verifier now requires the filled values and the equivalence record. Machine paths in five archive-authored files are replaced by `<WORKSPACE>`, and an internal status file in `publication/` is removed. README.md, CITATION.cff and .zenodo.json now use LF line endings. SOURCE_SHA256.json is re-pinned.
