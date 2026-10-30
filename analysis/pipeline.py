"""Offline archive validation. All child CLIs have closed stdin."""
from __future__ import annotations
import copy
import csv
import hashlib
import json
import math
import os
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
FIELDS = ("point", "ci", "rr_point", "rr_lo", "rr_hi")
TOL = 1e-9


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + "\n", encoding="utf-8")


def run(args, cwd=ROOT, log=None, expected=0):
    p = subprocess.run([str(x) for x in args], cwd=cwd, stdin=subprocess.DEVNULL,
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
                       encoding="utf-8", errors="replace")
    if log:
        Path(log).write_text(p.stdout, encoding="utf-8")
    if p.returncode != expected:
        raise RuntimeError(f"{args[0]} exited {p.returncode}:\n{p.stdout}")
    return p.stdout


def rscript():
    candidates = [os.environ.get("RSCRIPT"), shutil.which("Rscript"),
                  r"C:\Program Files\R\R-4.6.0\bin\Rscript.exe"]
    for p in candidates:
        if p and Path(p).is_file():
            return p
    raise RuntimeError("Rscript missing; set RSCRIPT to pinned R 4.6.0")


def real_cases(path):
    with Path(path).open(encoding="utf-8", newline="") as f:
        return [{**r, **{k: float(r[k]) for k in ("point", "lo", "hi")},
                 "rare": r["rare"] == "TRUE"} for r in csv.DictReader(f)]


def synthetic():
    rows = []
    for measure in ("RR", "OR", "HR", "SMD"):
        points = (-2, -.5, 0, .5, 2) if measure == "SMD" else (.2, .6, 1, 1.6, 2, 10)
        for p in points:
            for rare in ((False, True) if measure in ("OR", "HR") else (False,)):
                for ci in (True, False):
                    lo, hi = (p-.2, p+.2) if measure == "SMD" else (p/1.5, p*1.5)
                    rows.append(dict(id=f"grid-{measure}-{p}-{rare}-{ci}", measure=measure,
                                     point=p, lo=lo if ci else None, hi=hi if ci else None, rare=rare))
    for name, measure, p, lo, hi in (
        ("cross-rr","RR",1,.5,2), ("cross-smd","SMD",0,-1,1), ("degenerate","RR",2,2,2)):
        rows.append(dict(id=name, measure=measure, point=p, lo=lo, hi=hi, rare=False))
    # Dense grid, PREREG_ADDENDUM_2.md.
    for measure in ("RR", "OR", "HR", "SMD"):
        n = 121 if measure == "SMD" else 101
        for i in range(n):
            p = -3 + 6*i/(n-1) if measure == "SMD" else math.exp(math.log(.02) + math.log(50/.02)*i/(n-1))
            for rare in ((False, True) if measure in ("OR", "HR") else (False,)):
                for ci in (True, False):
                    lo, hi = (p-.25, p+.25) if measure == "SMD" else (p/1.5, p*1.5)
                    rows.append(dict(id=f"dense-{measure}-{i:03d}-{rare}-{ci}", measure=measure,
                                     point=p, lo=lo if ci else None, hi=hi if ci else None, rare=rare))
    return rows


def probes():
    base = dict(measure="RR", point=2, lo=1.5, hi=2.7, rare=False)
    changes = {
        "missing-point":{"point":None}, "zero-ratio":{"point":0,"lo":None,"hi":None},
        "negative-ratio":{"point":-1,"lo":None,"hi":None},
        "text-point":{"point":"oops"}, "malformed-point":{"point":"","badInput":["point"]},
        "malformed-ci":{"lo":"","hi":"","badInput":["lo"]},
        "partial-ci":{"lo":None}, "reversed-ci":{"lo":3,"hi":1},
        "noncontaining-ci":{"lo":2.5,"hi":3}, "zero-limit":{"lo":0},
        "nonfinite":{"point":"Infinity"}, "overflow-smd":{"measure":"SMD","point":1000,"lo":None,"hi":None},
        "unsupported":{"measure":"OLS"}
    }
    return [dict(base, **{"id":"refuse-"+name}) | change for name,change in changes.items()]


def flatten_fixture(cases):
    return [{"id": c["id"], "accepted": True, "values":{
        "point": c["expected"]["point"], "ci":c["expected"]["ci"],
        **{"rr_"+k:v for k,v in c["expected"]["rr"].items()}}} for c in cases]


def compare(expected, actual):
    if not expected:
        raise ValueError("Empty expected corpus")
    def indexed(rows):
        result = {}
        for r in rows:
            if set(r) != {"id","accepted","values"} or r["id"] in result:
                raise ValueError("Schema mismatch or duplicate ID")
            if type(r["accepted"]) is not bool:
                raise ValueError("Acceptance must be boolean")
            result[r["id"]] = r
        return result
    a, b = indexed(expected), indexed(actual)
    if a.keys() != b.keys():
        raise ValueError(f"Configuration mismatch: missing={sorted(a.keys()-b.keys())}, extra={sorted(b.keys()-a.keys())}")
    checks = passed = 0
    failures = []
    maximum = 0.
    for key, ref in a.items():
        got = b[key]
        checks += 1
        if ref["accepted"] == got["accepted"]:
            passed += 1
        else:
            failures.append(key+": acceptance")
        if not ref["accepted"]:
            checks += 1
            if ref["values"] is None and got["values"] is None:
                passed += 1
            else:
                failures.append(key+": refusal payload")
            continue
        if not isinstance(ref["values"], dict) or set(ref["values"]) != set(FIELDS):
            raise ValueError("Reference quantity keys mismatch")
        if not isinstance(got["values"], dict) or set(got["values"]) != set(FIELDS):
            # Fixed denominator: acceptance + five quantities for every accepted reference.
            checks += len(FIELDS)
            failures.append(key+": quantity keys mismatch")
            continue
        for field in FIELDS:
            checks += 1
            x, y = ref["values"][field], got["values"][field]
            if x is None or y is None:
                ok = x is None and y is None
            elif type(x) not in (int,float) or type(y) not in (int,float) or not all(map(math.isfinite,(x,y))):
                ok = False
            else:
                diff = abs(x-y)/max(1,abs(x))
                maximum = max(maximum,diff)
                ok = diff <= TOL
            if ok:
                passed += 1
            else:
                failures.append(key+":"+field)
    return dict(passed=passed, expected=checks, configurations=len(expected),
                max_normalized_difference=maximum, tolerance=TOL, failures=failures,
                final_line=f"{passed}/{checks} checks pass")


def safeguards(expected, actual):
    baseline = compare(expected,actual)
    if baseline["failures"]:
        raise ValueError("Safeguards require passing baseline")
    mutants = {}
    changed = copy.deepcopy(actual)
    target = next(i for i,r in enumerate(expected) if r["accepted"])
    v = expected[target]["values"]["point"]
    changed[target]["values"]["point"] += 1e-8 * max(1,abs(v))
    mutants["relative-1e-8"] = changed
    mutants["dropped-configuration"] = copy.deepcopy(actual[:-1])
    mutants["duplicate-id"] = copy.deepcopy(actual + actual[:1])
    changed = copy.deepcopy(actual)
    changed[target]["values"]["point"] = math.nan
    mutants["nonfinite"] = changed
    outcomes = {}
    for name, rows in mutants.items():
        try:
            s = compare(expected,rows)
            rejected = bool(s["failures"])
            reason = s
        except ValueError as e:
            rejected, reason = True, str(e)
        if not rejected:
            raise AssertionError("Mutant escaped: "+name)
        outcomes[name] = {"rejected":rejected,"reason":reason}
    return outcomes


def replay(cases, work, name, page="app-original/evalue/index.html"):
    write(work/(name+"-inputs.json"),cases)
    text = run(["node","analysis/replay.cjs",page,
                work/(name+"-inputs.json"),work/(name+"-app.json")])
    (work/(name+"-replay.log")).write_text(text,encoding="utf-8")
    return read(work/(name+"-app.json"))["rows"]


def planted_source_defect(cases,expected,work):
    """Replay a copy of the page whose HR conversion constant is perturbed; it must fail."""
    app=work/"mutant-app"
    shutil.copytree(ROOT/"app-original",app)
    js=app/"shared/evalue.js"
    old="Math.pow(0.5, Math.sqrt(est))"
    text=js.read_text(encoding="utf-8")
    if text.count(old)!=1:
        raise RuntimeError("Planted-defect target not found exactly once")
    js.write_text(text.replace(old,"Math.pow(0.5000001, Math.sqrt(est))"),encoding="utf-8")
    summary=compare(expected,replay(cases,work,"mutant",app/"evalue/index.html"))
    if not summary["failures"]:
        raise AssertionError("Planted app-source defect escaped")
    summary["failures"]=summary["failures"][:20]+(["..."] if len(summary["failures"])>20 else [])
    write(work/"mutant-summary.json",summary)
    return summary


def smd_convention(cases,actual,reference):
    """Descriptive only: app pointwise SMD limits vs EValue's se-based exp(0.91 d +/- 1.78 se)."""
    with Path(reference).open(encoding="utf-8",newline="") as f:
        ref={r["id"]:r for r in csv.DictReader(f)}
    got={r["id"]:r for r in actual}
    out={}
    for group in ("real","synthetic"):
        diffs=[]
        for c in cases:
            if c["measure"]!="SMD" or c["lo"] is None or ("dataset" in c)!=(group=="real"):
                continue
            r=ref[c["id"]]
            for k in ("lo","hi"):
                x=float(r["se_rr_"+k]); y=got[c["id"]]["values"]["rr_"+k]
                diffs.append(abs(x-y)/abs(x))
        out[group]=dict(configurations=len(diffs)//2,max_relative_difference=max(diffs),
                        counted_in_validation=False)
    return out


def write_csv(cases,path):
    with Path(path).open("w",encoding="utf-8",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=["id","measure","point","lo","hi","rare"],extrasaction="ignore")
        writer.writeheader()
        for case in cases:
            writer.writerow(case | {"rare":"TRUE" if case["rare"] else "FALSE"})


def verify(root=ROOT):
    pins=read(root/"SOURCE_SHA256.json")
    excluded={".git",".validate-work","__pycache__"}
    files={p.relative_to(root).as_posix():p for p in root.rglob("*")
           if p.is_file() and not (set(p.relative_to(root).parts)&excluded)
           and p.name!="SOURCE_SHA256.json"}
    if set(files)!=set(pins):
        raise ValueError("Archive inventory mismatch")
    for name,p in files.items():
        if hashlib.sha256(p.read_bytes()).hexdigest()!=pins[name]:
            raise ValueError("Hash mismatch: "+name)
    return len(pins)


def prereg_order(root=ROOT):
    """Each preregistration stage in PREREG_RECORD.json: its plan files were added in one commit that is older than, and an
    ancestor of, the first commit touching its results, and they are unchanged since. With .git this is proved from the
    history, which must agree with the record; a squashed or shallow history fails. Without .git only the record is checked."""
    rec=read(root/"PREREG_RECORD.json")
    has_git=(root/".git").exists()
    git=lambda *a: subprocess.run(["git","-C",str(root),*a],capture_output=True,text=True)
    log=lambda path: git("log","--reverse","--format=%H %ct","HEAD","--",path).stdout.split()
    if has_git and git("rev-parse","--is-shallow-repository").stdout.split()!=["false"]:
        raise ValueError("Shallow clone: the preregistration order needs the full history")
    lines=[]
    for s in rec["stages"]:
        if s["plan_commit"]==s["first_results_commit"] or s["plan_committed_unix"]>=s["first_results_committed_unix"]:
            raise ValueError("PREREG_RECORD.json: plan not committed before results: "+s["results"])
        for name,blob in s["plan_blobs"].items():
            raw=(root/name).read_bytes()
            if hashlib.sha1(b"blob %d\0"%len(raw)+raw).hexdigest()!=blob:
                raise ValueError("Preregistration file differs from the preregistered blob: "+name)
        if not has_git:
            lines.append(f'{" + ".join(s["plan"])} ({s["plan_commit"][:7]}) before {s["results"]} ({s["first_results_commit"][:7]}): record only, no git history in this copy')
            continue
        res=log(s["results"])
        if not res:
            raise ValueError("No git history for "+s["results"])
        for name,blob in s["plan_blobs"].items():
            pre=log(name)
            if len(pre)!=2:
                raise ValueError("Preregistration file changed after its commit: "+name)
            if pre[0]==res[0] or int(pre[1])>=int(res[1]) or git("merge-base","--is-ancestor",pre[0],res[0]).returncode:
                raise ValueError(f"{name} was not committed before the first commit touching {s['results']}")
            if pre!=[s["plan_commit"],str(s["plan_committed_unix"])] or git("rev-parse",pre[0]+":"+name).stdout.split()!=[blob]:
                raise ValueError("Git history disagrees with PREREG_RECORD.json: "+name)
        if res[:2]!=[s["first_results_commit"],str(s["first_results_committed_unix"])]:
            raise ValueError("Git history disagrees with PREREG_RECORD.json: "+s["results"])
        lines.append(f'{" + ".join(s["plan"])} ({s["plan_commit"][:7]}) precede the first {s["results"]} commit ({res[0][:7]}) in the git history')
    return lines


def full():
    print(f"Archive integrity PASS: {verify()} files",flush=True)
    work=ROOT/".validate-work"
    if work.exists():
        raise RuntimeError("Existing .validate-work refused; preserve it elsewhere before retry")
    work.mkdir()
    run([rscript(),"--vanilla","analysis/generate_corpus.R",work/"real-corpus.csv"],
        log=work/"corpus.log")
    if (work/"real-corpus.csv").read_bytes() != (ROOT/"data/real-corpus.csv").read_bytes():
        raise RuntimeError("Fresh real corpus differs from locked corpus")
    cases=real_cases(work/"real-corpus.csv")+synthetic()
    if cases != read(ROOT/"data/corpus.json"):
        raise RuntimeError("Fresh full corpus differs from locked corpus")
    write_csv(cases,work/"oracle-input.csv")
    run([rscript(),"--vanilla","analysis/reference.R",work/"oracle-input.csv",work/"reference.csv"],
        log=work/"reference.log")
    with (work/"reference.csv").open(encoding="utf-8",newline="") as f:
        expected=[{"id":r["id"],"accepted":True,"values":{
            k:float(r[k]) if r[k] else None for k in FIELDS}} for r in csv.DictReader(f)]
    actual=replay(cases,work,"full")
    summary=compare(expected,actual)
    write(work/"summary.json",summary)
    print(summary["final_line"],flush=True)
    if summary["failures"]:
        raise RuntimeError("Fresh oracle comparison failed")
    write(work/"safeguards.json",safeguards(expected,actual))
    print("Planted comparator defects (1e-8 perturbation, dropped configuration, duplicate ID, nonfinite) all rejected",flush=True)
    planted=planted_source_defect(cases,expected,work)
    print(f"Planted app-source defect rejected: {planted['final_line']}",flush=True)
    write(work/"smd-se-convention.json",smd_convention(cases,actual,work/"reference.csv"))
    refusal_cases=probes()
    refusal=compare([dict(id=c["id"],accepted=False,values=None) for c in refusal_cases],
                    replay(refusal_cases,work,"refusals"))
    write(work/"refusals-summary.json",refusal)
    print(refusal["final_line"]+" (refusals)",flush=True)
    if refusal["failures"]:
        raise RuntimeError("Refusal mismatch")
    release(cases,expected,actual,refusal_cases,work)
    # PREREG_ADDENDUM_4.md: allmeta main 6ce55eb (1/RR label), same reference and checks.
    release(cases,expected,actual,refusal_cases,work,"app-main-6ce55eb/evalue/index.html","main-6ce55eb","main 6ce55eb")
    print(run([sys.executable,"-B","analysis/test_safeguards.py"],
              log=work/"archive-safeguards.log"), end="", flush=True)


def release(cases,expected,original,refusal_cases,work,page="app-v1.8.0/evalue/index.html",
            prefix="release",label="release v1.8.0"):
    """PREREG_ADDENDUM_3.md (v1.8.0) and PREREG_ADDENDUM_4.md (main 6ce55eb): replay a snapshot against the same reference."""
    actual=replay(cases,work,prefix,page)
    summary=compare(expected,actual)
    write(work/(prefix+"-summary.json"),summary)
    print(summary["final_line"]+f" ({label})",flush=True)
    if summary["failures"]:
        raise RuntimeError(f"{label}: oracle comparison failed")
    refusal=compare([dict(id=c["id"],accepted=False,values=None) for c in refusal_cases],
                    replay(refusal_cases,work,prefix+"-refusals",page))
    write(work/(prefix+"-refusals-summary.json"),refusal)
    print(refusal["final_line"]+f" ({label} refusals)",flush=True)
    if refusal["failures"]:
        raise RuntimeError(f"{label}: refusal mismatch")
    identical=actual==original
    write(work/(prefix+"-vs-original.json"),dict(configurations=len(actual),
          identical_output=identical,comparison="exact equality of every row"))
    if not identical:
        raise RuntimeError(f"{label}: output differs from original page")
    print(f"{label[0].upper()+label[1:]} output identical to original page (exact)",flush=True)


def local():
    work=ROOT/"evidence/local"
    work.mkdir(parents=True,exist_ok=True)
    fixture=read(ROOT/"references/inherited-evalue-input-oracle.json")
    cases=fixture["cases"]
    expected=flatten_fixture(cases)
    actual=replay(cases,work,"inherited")
    summary=compare(expected,actual)
    summary["provenance"]="Inherited repository fixture; no fresh EValue execution"
    write(work/"inherited-summary.json",summary)
    print(summary["final_line"]+" (inherited fixture only)")
    if summary["failures"]:
        raise RuntimeError("Inherited fixture mismatch")
    write(work/"comparator-safeguards.json",safeguards(expected,actual))
    refusal=compare([dict(id=c["id"],accepted=False,values=None) for c in probes()],
                    replay(probes(),work,"refusals"))
    write(work/"refusals-summary.json",refusal)
    print(refusal["final_line"]+" (refusals)")
    if refusal["failures"]:
        raise RuntimeError("Refusal mismatch")
    corpus=real_cases(ROOT/"data/real-corpus.csv")+synthetic()
    write(ROOT/"data/corpus.json",corpus)
    write_csv(corpus,ROOT/"data/oracle-input.csv")
    rows=replay(corpus,work,"corpus")
    if not all(r["accepted"] for r in rows):
        raise RuntimeError("Valid corpus refused")
    write(work/"corpus-execution.json",dict(configurations=len(rows),
          accepted=sum(r["accepted"] for r in rows),oracle_comparison="NOT RUN: EValue missing",
          real_configurations=len(real_cases(ROOT/"data/real-corpus.csv")),
          synthetic_configurations=len(synthetic())))
    print(f"{len(rows)} corpus inputs executed; numerical R parity NOT assessed")


if __name__=="__main__":
    try:
        {"local":local,"full":full,"verify":lambda:print(f"{verify()} hashes verified")}[sys.argv[1]]()
    except Exception as e:
        print(f"FAIL: {e}",file=sys.stderr)
        sys.exit(1)
