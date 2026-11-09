"""Photo carousel: cards that slide slowly from left to right, forever, and pause when hovered.

Pure CSS animation (no JavaScript). Each photo is embedded only once; the repeated cards reuse it.
People who have "reduce motion" switched on can scroll the strip by hand instead.

Photos come from two places:
  * the list you pass in (file names inside assets/), and
  * every photo found in the folder assets/<folder>/ , picked up automatically.
"""
import base64
import html as _html
from pathlib import Path

import streamlit as st

ASSETS = Path(__file__).resolve().parent.parent / "assets"

# ---- Tweak the carousel here -------------------------------------------------
SECONDS_PER_CARD = 3      # bigger number = slower sliding
SHOW_CAPTIONS = False     # True = show the text under each photo (only photos that have a caption)
# ------------------------------------------------------------------------------

CSS = """
<style>
.gwrap { overflow: hidden; padding: .6rem 0 1rem; margin: .5rem 0 1rem;
  -webkit-mask-image: linear-gradient(90deg, transparent, #000 5%, #000 95%, transparent);
  mask-image: linear-gradient(90deg, transparent, #000 5%, #000 95%, transparent); }
.gtrack { display: flex; width: max-content; animation: dhf-slide var(--dur) linear infinite; }
.gwrap:hover .gtrack { animation-play-state: paused; }
.ghalf { display: flex; gap: 1.1rem; padding-right: 1.1rem; }
.gcard { position: relative; flex: 0 0 auto; width: clamp(250px, 30vw, 420px); aspect-ratio: 4 / 3;
  border-radius: 20px; overflow: hidden; background-size: cover; background-position: center top;
  background-color: #2E7D55; box-shadow: 0 6px 20px rgba(30,90,60,.22); }
.gcap { position: absolute; left: 0; right: 0; bottom: 0; padding: 2.2rem 1rem .8rem; color: #fff;
  font-weight: 600; font-size: 1rem; line-height: 1.3;
  background: linear-gradient(180deg, rgba(18,60,40,0), rgba(18,60,40,.88)); }
/* the strip moves left to right: it starts shifted left by one half and slides back to 0 */
@keyframes dhf-slide { from { transform: translateX(-50%); } to { transform: translateX(0); } }
@media (prefers-reduced-motion: reduce) {
  .gwrap { overflow-x: auto; -webkit-mask-image: none; mask-image: none; }
  .gtrack { animation: none; }
  .ghalf[aria-hidden="true"] { display: none; }
}
</style>
"""

PHOTO_TYPES = {".jpg", ".jpeg", ".png", ".webp"}


@st.cache_data
def _data_uri(name: str) -> str:
    """Read an image from assets/ and return it as an inline data URI."""
    path = ASSETS / name
    mime = {".png": "image/png", ".webp": "image/webp"}.get(path.suffix.lower(), "image/jpeg")
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode()


def _collect(photos, folder):
    """Combine the list with the photos found in the folder. Returns [(file path inside assets/, caption)]."""
    items = []
    for p in photos or []:
        name, caption = (p, "") if isinstance(p, str) else (p[0], p[1] if len(p) > 1 else "")
        items.append((name, caption))
    if folder and (ASSETS / folder).is_dir():
        for f in sorted((ASSETS / folder).iterdir()):
            if f.suffix.lower() in PHOTO_TYPES:
                items.append((f"{folder}/{f.name}", ""))
    return items


def photo_marquee(photos=(), folder=None):
    """Show a sliding strip of photo cards.

    photos = file names inside assets/ (or (file name, caption) pairs);
    folder = a folder inside assets/ whose photos are all added automatically.
    """
    items = _collect(photos, folder)
    if not items:
        return
    images = "".join(f".g{i}{{background-image:url({_data_uri(f)})}}" for i, (f, _) in enumerate(items))
    cards = "".join(
        f'<div class="gcard g{i}" role="img" aria-label="{_html.escape(c or "Photo from a DHF outreach")}">'
        + (f'<div class="gcap">{_html.escape(c)}</div>' if SHOW_CAPTIONS and c else "") + '</div>'
        for i, (_, c) in enumerate(items))
    copies = max(2, -(-6 // len(items)))                # at least 6 cards per half, so the strip never shows a gap
    half = cards * copies
    duration = len(items) * copies * SECONDS_PER_CARD
    page = (f'<style>{images}</style>'
            f'<div class="gwrap"><div class="gtrack" style="--dur:{duration}s">'
            f'<div class="ghalf">{half}</div><div class="ghalf" aria-hidden="true">{half}</div>'
            f'</div></div>')
    st.markdown(CSS + page, unsafe_allow_html=True)