from pipeline import ROOT, verify, prereg_order
print(f"{verify()} archive hashes verified")
for name in ("README.md", "CITATION.cff", ".zenodo.json"):
    text = (ROOT/name).read_text(encoding="utf-8")
    assert "<ALLMETA_RELEASE" not in text, "Unfilled release token: "+name
    assert "v1.8.0" in text and "10.5281/zenodo.23515177" in text, "allmeta v1.8.0 tag/DOI missing: "+name
    assert "v1.9.0" in text and "10.5281/zenodo.23833871" in text and "d38d3fd" in text, "allmeta v1.9.0 tag/commit/DOI missing: "+name
eq = (ROOT/"RELEASE_EQUIVALENCE.md").read_text(encoding="utf-8")
assert "1cb3f8409c7af75ed41f7e1811f9c502f900fc79" in eq and "byte-identical" in eq and "22,428/22,428" in eq, "Release equivalence record missing"
assert "d38d3fd70656f3fedfa03916573fe0bf904f5e9c" in eq and "10.5281/zenodo.23833871" in eq, "v1.9.0 release equivalence record missing"
print("allmeta v1.9.0 and v1.8.0 release identifiers filled; release equivalence records present")
for line in prereg_order():
    print("Preregistration: "+line)
print("Preregistration files equal their preregistered blobs")
