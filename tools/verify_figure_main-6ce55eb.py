"""PREREG_ADDENDUM_4.md: verify_figure.py with the figure directory set to figures/main-6ce55eb/.
HOST: convert the real captured PNGs to RGB/LZW/300-dpi TIFF; never create a substitute image."""
from pathlib import Path
import hashlib
import json
import sys
from PIL import Image, __version__ as PIL_VERSION
root=Path(__file__).resolve().parents[1]/"figures/main-6ce55eb"
capture=json.loads((root/"capture.json").read_text(encoding="utf-8"))
expected={"figure1":"bcg-001-RR-FALSE","figure2":"normand1999-001-SMD"}
assert {c["figure"]:c["input"]["id"] for c in capture["captures"]}==expected
def check(tiff):
    with Image.open(tiff) as im:
        ok=im.mode=="RGB" and im.tag_v2.get(259)==5 and all(float(v)>=300 for v in im.info.get("dpi",(0,0)))
        return ok,{"mode":im.mode,"size":list(im.size),"dpi":[float(v) for v in im.info.get("dpi",(0,0))],
                   "compression_tag":im.tag_v2.get(259)}
info={"pillow":PIL_VERSION}
for name in expected:
    png,tiff=root/(name+".png"),root/(name+".tiff")
    if "--check-only" not in sys.argv:
        with Image.open(png) as im:
            im.convert("RGB").save(tiff,compression="tiff_lzw",dpi=(300,300))
    ok,meta=check(tiff)
    assert ok,(name,meta)
    with Image.open(png) as a, Image.open(tiff) as b:
        assert a.convert("RGB").tobytes()==b.tobytes(), name+": TIFF pixels differ from capture"
    info[name]=meta|{"png_sha256":hashlib.sha256(png.read_bytes()).hexdigest(),
                     "tiff_sha256":hashlib.sha256(tiff.read_bytes()).hexdigest(),"pixels_equal_capture":True}
(root/"verification.json").write_text(json.dumps(info,indent=2)+"\n",encoding="utf-8")
print(f"{len(expected)}/{len(expected)} real-capture TIFFs verified: RGB, LZW, >=300 dpi, pixels identical to PNG")
