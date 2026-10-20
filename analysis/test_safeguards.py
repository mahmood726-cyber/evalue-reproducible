"""Independent fail-closed hash/inventory and pinned-R negative controls."""
import hashlib
import subprocess
import uuid
from pathlib import Path
from pipeline import ROOT, verify, write, rscript

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
    result=subprocess.run([rscript(),"--vanilla","analysis/version_safeguard.R"],cwd=ROOT,
                          stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,
                          text=True,encoding="utf-8",errors="replace")
    if result.returncode: raise RuntimeError(result.stdout)
    outcomes.append("wrong-R-version")
    print(f"{len(outcomes)}/{len(outcomes)} archive/version safeguards pass: "+", ".join(outcomes))

if __name__=="__main__": main()
