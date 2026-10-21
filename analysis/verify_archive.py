from pipeline import ROOT, verify
print(f"{verify()} archive hashes verified")
for name in ("README.md", "CITATION.cff", ".zenodo.json"):
    text = (ROOT/name).read_text(encoding="utf-8")
    assert "<ALLMETA_RELEASE" not in text, "Unfilled release token: "+name
    assert "v1.8.0" in text and "10.5281/zenodo.23515177" in text, "allmeta v1.8.0 tag/DOI missing: "+name
eq = (ROOT/"RELEASE_EQUIVALENCE.md").read_text(encoding="utf-8")
assert "1cb3f8409c7af75ed41f7e1811f9c502f900fc79" in eq and "byte-identical" in eq and "22,428/22,428" in eq, "Release equivalence record missing"
print("allmeta v1.8.0 release identifiers filled; release equivalence record present")
