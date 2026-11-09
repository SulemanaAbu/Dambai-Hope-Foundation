"""Prepare photos for the website carousel.

1. Put your original photos in a folder called  new_photos  (next to app.py).
2. Run:  python resize_photos.py
3. Shrunken copies are saved in assets/gallery/ and appear on the Home page automatically.
"""
import re
import sys
from pathlib import Path

from PIL import Image, ImageOps

SRC, DEST = Path("new_photos"), Path("assets") / "gallery"
WIDTH = 900                                     # photos are shrunk to this width (smaller files = faster site)

if not SRC.exists():
    SRC.mkdir()
    sys.exit("I created a folder called 'new_photos'. Put your photos in it, then run this again.")

files = [p for p in sorted(SRC.iterdir()) if p.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}]
if not files:
    sys.exit("No photos found in 'new_photos'. Add .jpg or .png files and run this again.")

DEST.mkdir(parents=True, exist_ok=True)
for p in files:
    img = ImageOps.exif_transpose(Image.open(p)).convert("RGB")      # fixes photos that were taken sideways
    if img.width > WIDTH:
        img = img.resize((WIDTH, round(img.height * WIDTH / img.width)), Image.LANCZOS)
    name = re.sub(r"[^a-z0-9]+", "_", p.stem.lower()).strip("_") or "photo"
    out = DEST / f"{name}.jpg"
    if out.exists():                                                  # already done on an earlier run
        print(f"Skipped {p.name}  (assets/gallery/{out.name} already exists)")
        continue
    img.save(out, "JPEG", quality=80, optimize=True)
    note = "   <- portrait photo: the card will crop it, a landscape photo looks better" if img.height > img.width * 1.1 else ""
    print(f"Saved {out}  ({img.width}x{img.height}, {out.stat().st_size // 1024} KB){note}")

total = len(list(DEST.glob("*.jpg")))
print(f"\nDone. assets/gallery now holds {total} photo(s). They appear on the Home page automatically.")
if total > 15:
    print("Tip: more than 10 photos makes the page slower to load, especially on phones.")