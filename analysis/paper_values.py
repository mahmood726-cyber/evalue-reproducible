"""Derive every number quoted in the manuscript from archived evidence -> evidence/fresh/paper_values.json."""
import collections
import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT/"evidence/fresh/run-2-release-v1.8.0"  # PREREG_ADDENDUM_3.md: counts from the release page


def load(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def main():
    s = load(RUN/"release-summary.json")
    original = load(RUN/"summary.json")
    release = load(ROOT/"provenance-release.json")
    same = load(RUN/"release-vs-original.json")
    corpus = load(ROOT/"data/corpus.json")
    real = [c for c in corpus if "dataset" in c]
    by_measure = collections.Counter(c["measure"] for c in corpus)
    real_by_measure = collections.Counter(c["measure"] for c in real)
    safeguards = load(RUN/"safeguards.json")
    mutant = load(RUN/"mutant-summary.json")
    refusal = load(RUN/"release-refusals-summary.json")
    smd = load(RUN/"smd-se-convention.json")
    log = (RUN/"corpus.log").read_text(encoding="utf-8")
    excl = [(m.group(1), m.group(2), int(m.group(3))) for m in
            re.finditer(r"(dat\.\S+) (RR|OR|SMD): (\d+) non-estimable", log)]
    binary_rows = sum(n for _, m, n in excl if m == "RR")
    smd_rows = sum(n for _, m, n in excl if m == "SMD")
    capture = load(ROOT/"figures/capture.json")
    figs = {c["figure"]: {"id": c["input"]["id"], "point": c["input"]["point"], "lo": c["input"]["lo"],
                          "hi": c["input"]["hi"], "e_point": c["result"]["point"], "e_ci": c["result"]["ci"],
                          "rr": c["result"]["rr"]} for c in capture["captures"]}
    out = {
        "checks_passed": s["passed"], "checks_expected": s["expected"],
        "configurations": s["configurations"], "max_normalized_difference": s["max_normalized_difference"],
        "tolerance": s["tolerance"],
        "real_configurations": len(real), "synthetic_configurations": len(corpus) - len(real),
        "real_datasets": len({c["dataset"] for c in real}),
        "configurations_by_measure": dict(by_measure), "real_by_measure": dict(real_by_measure),
        "excluded_binary_rows": binary_rows, "excluded_smd_rows": smd_rows,
        "excluded_datasets": len({d for d, _, n in excl if n}),
        "refusal_passed": refusal["passed"], "refusal_expected": refusal["expected"],
        "refusal_probes": refusal["configurations"],
        "perturbation_result": safeguards["relative-1e-8"]["reason"]["final_line"],
        "dropped_rejected": safeguards["dropped-configuration"]["rejected"],
        "mutant_passed": mutant["passed"], "mutant_expected": mutant["expected"],
        "smd_se_max_rel_diff_real": smd["real"]["max_relative_difference"],
        "smd_se_real_configurations": smd["real"]["configurations"],
        "browser": capture["browser"], "figures": figs,
        "release_tag": release["tag"], "release_commit": release["tag_commit"],
        "release_changed_page_files": release["page_files_changed_74ff0a7_to_v1.8.0"],
        "release_output_identical_to_original": same["identical_output"],
        "original_checks_passed": original["passed"], "original_checks_expected": original["expected"],
    }
    (ROOT/"evidence/fresh/paper_values.json").write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
