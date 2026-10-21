"""Independent fail-closed hash/inventory and pinned-R negative controls."""
import hashlib
import os
import subprocess
import uuid
from pathlib import Path
from pipeline import ROOT, verify, write, rscript, prereg_order

def main():
    outcomes=[]
    scratch=ROOT.parent/".p22-checks"
    scratch.mkdir(exist_ok=True)
    temp=scratch/("safeguards-"+uuid.uuid4().hex)
    temp.mkdir()
    # Retain the small negative-control inputs; no recursive deletion.
    def inventory_controls():
        root=Path(temp)
        p=root/"input.txt"
        p.write_bytes(b"original")
        write(root/"SOURCE_SHA256.json",{"input.txt":hashlib.sha256(p.read_bytes()).hexdigest()})
        assert verify(root)==1
        for name in ("changed","missing","extra"):
            p.write_bytes(b"original")
            if name=="changed": p.write_bytes(b"changed")
            elif name=="missing": p.unlink()
            else: (root/"extra.txt").write_bytes(b"extra")
            try: verify(root)
            except ValueError: outcomes.append(name)
            else: raise AssertionError("Inventory mutant escaped: "+name)
    inventory_controls()
    def prereg_controls():
        # Small git histories: a correct one passes; squashed, results-first, shallow, edited-plan and record-mismatch fail.
        plan,res={"PREREG.md":b"plan\n"},{"evidence/fresh/r.json":b"{}\n"}
        def build(name,steps):
            root=temp/name
            subprocess.run(["git","init","-q",str(root)],check=True)
            hashes=[]
            for t,files in steps:
                for f,data in files.items():
                    (root/f).parent.mkdir(parents=True,exist_ok=True); (root/f).write_bytes(data)
                env=dict(os.environ,GIT_AUTHOR_DATE=f"@{t} +0000",GIT_COMMITTER_DATE=f"@{t} +0000")
                g=lambda *a: subprocess.run(["git","-C",str(root),"-c","user.name=test","-c","user.email=test","-c","core.autocrlf=false",*a],
                                            env=env,capture_output=True,text=True,check=True).stdout.strip()
                g("add","-A"); g("commit","-q","-m",str(t)); hashes.append(g("rev-parse","HEAD"))
            return root,hashes
        def record(root,pc,pt,rc,rt):
            write(root/"PREREG_RECORD.json",{"stages":[{"plan":["PREREG.md"],"plan_commit":pc,"plan_committed_unix":pt,
                "plan_blobs":{"PREREG.md":hashlib.sha1(b"blob 5\0plan\n").hexdigest()},"results":"evidence/fresh",
                "first_results_commit":rc,"first_results_committed_unix":rt}]})
        good,h=build("good",[(1700000000,plan),(1700000100,res)]); record(good,h[0],1700000000,h[1],1700000100)
        assert len(prereg_order(good))==1
        cases=[]
        record(good,h[0],1699999999,h[1],1700000100); cases.append(("prereg-record-mismatch",good))
        root,h2=build("squashed",[(1700000000,plan|res)]); record(root,h2[0],1700000000,"0"*40,1700000100); cases.append(("prereg-squashed",root))
        root,h2=build("results-first",[(1700000000,res),(1700000100,plan)]); record(root,h2[1],1700000000,h2[0],1700000100); cases.append(("prereg-results-first",root))
        root,h2=build("edited",[(1700000000,plan),(1700000100,res),(1700000200,{"PREREG.md":b"plan\n"+b"edited\n"})])
        (root/"PREREG.md").write_bytes(b"plan\n"); record(root,h2[0],1700000000,h2[1],1700000100); cases.append(("prereg-edited",root))
        shallow=temp/"shallow"
        subprocess.run(["git","-c","core.autocrlf=false","clone","-q","--depth","1",good.as_uri(),str(shallow)],check=True,capture_output=True)
        record(shallow,h[0],1700000000,h[1],1700000100); cases.append(("prereg-shallow",shallow))
        for name,root in cases:
            try: prereg_order(root)
            except ValueError: outcomes.append(name)
            else: raise AssertionError("Preregistration mutant escaped: "+name)
    prereg_controls()
    result=subprocess.run([rscript(),"--vanilla","analysis/version_safeguard.R"],cwd=ROOT,
                          stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,
                          text=True,encoding="utf-8",errors="replace")
    if result.returncode: raise RuntimeError(result.stdout)
    outcomes.append("wrong-R-version")
    print(f"{len(outcomes)}/{len(outcomes)} archive/version safeguards pass: "+", ".join(outcomes))

if __name__=="__main__": main()
