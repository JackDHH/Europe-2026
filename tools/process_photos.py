"""Copy public journal photos into friends/photos/<id>.jpg, re-encoded with ALL metadata (GPS, camera, times) removed.
Usage: python3 -I process_photos.py <dir containing downloaded assets named <id>.*>"""
import sys, os, json, glob, re
from PIL import Image, ImageOps
BASE = os.path.dirname(os.path.abspath(__file__)); src = sys.argv[1]
want = set()
for f in glob.glob(os.path.join(BASE, "journal_dump/journal/*.json")):
    if os.path.basename(f).startswith("."): continue
    x = json.load(open(f)); x = x.get("data", x)
    if x.get("public") is False: continue
    for ph in x.get("photos") or []:
        if re.match(r"^[a-f0-9]{32}$", ph.get("id", ""), re.I): want.add(ph["id"])
os.makedirs(os.path.join(BASE, "friends/photos"), exist_ok=True)
done = 0
for pid in want:
    out = os.path.join(BASE, "friends/photos", pid + ".jpg")
    if os.path.exists(out): continue
    cand = [p for p in glob.glob(os.path.join(src, pid + "*")) if not os.path.basename(p).startswith(".")]
    if not cand: print("missing", pid); continue
    im = ImageOps.exif_transpose(Image.open(cand[0])).convert("RGB")
    im.thumbnail((1600, 1600))
    clean = Image.new("RGB", im.size); clean.paste(im)   # fresh image: no EXIF/XMP/ICC carried over
    clean.save(out, "JPEG", quality=82, optimize=True, progressive=True)
    done += 1
# remove photos no longer public
for f in glob.glob(os.path.join(BASE, "friends/photos/*.jpg")):
    if os.path.basename(f)[:-4] not in want: os.remove(f); print("removed", f)
print("processed", done, "of", len(want))
