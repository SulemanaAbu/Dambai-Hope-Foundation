"""Hero banner: photo background with the headline typed out, replaying every 15 seconds.

Pure CSS animation (no JavaScript), so it works inside Streamlit. Every letter fades in one
after another, a cursor blinks, the subtitle fades in, and after REPLAY_EVERY seconds the text
clears and types itself out again. People who have "reduce motion" switched on in their
system settings see the finished text straight away.
"""
import base64
import html as _html
from pathlib import Path

import streamlit as st

ASSETS = Path(__file__).resolve().parent.parent / "assets"

# ---- Tweak the animation here ----------------------------------------------
START_DELAY = 0.5     # seconds before typing starts
LETTER_GAP = 0.06     # seconds between letters (smaller = faster typing)
REPLAY_EVERY = 15     # the whole animation restarts every this many seconds
FADE_AT = 96          # % of the cycle at which the text fades out before replaying
# ----------------------------------------------------------------------------

CSS = """
<style>
.hero-photo { position: relative; min-height: clamp(480px, 76vh, 720px); display: flex; align-items: flex-end;
  border-radius: 28px 28px 28px 120px; overflow: hidden; margin: 1rem 0 2.5rem;
  background-size: cover; background-position: center top; background-color: #2E7D55; }
/* dark green fade from the lower part only, so faces stay bright and the text stays readable */
.hero-photo::before { content: ""; position: absolute; inset: 0;
  background: linear-gradient(180deg, rgba(18,60,40,0) 40%, rgba(18,60,40,.85) 72%, rgba(18,60,40,.95) 100%); }
.hero-photo .inner { position: relative; padding: 2rem 3rem 2.6rem; }
.hero-photo h1 { color: #E8F7EE; font-size: clamp(2rem, 4.6vw, 3.6rem); font-weight: 800;
  line-height: 1.08; margin: 0 0 .8rem; }
.hero-photo .wd { display: inline-block; white-space: nowrap; }
.hero-photo .ch, .hero-photo .cur, .hero-photo .sub {
  opacity: 0; animation-duration: __T__s; animation-iteration-count: infinite; animation-timing-function: linear; }
.hero-photo .cur { display: inline-block; }
.hero-photo .blink { display: inline-block; width: .07em; height: .9em; margin-left: .08em;
  background: #E8F7EE; vertical-align: -.05em; animation: dhf-blink 1s steps(1) infinite; }
@keyframes dhf-blink { 0%, 49% { opacity: 1; } 50%, 100% { opacity: 0; } }
.hero-photo .sub { color: #fff; font-size: 1.15rem; max-width: 52ch; margin: 0; animation-name: dhf-sub; }
@media (max-width: 640px) { .hero-photo { min-height: 460px; } .hero-photo .inner { padding: 1.5rem 1.4rem 1.8rem; } }
@media (prefers-reduced-motion: reduce) {
  .hero-photo .ch, .hero-photo .sub { animation: none !important; opacity: 1 !important; }
  .hero-photo .cur { display: none; }
}
</style>
""".replace("__T__", str(REPLAY_EVERY))


@st.cache_data
def _data_uri(name: str) -> str:
    """Read an image from assets/ and return it as an inline data URI."""
    raw = (ASSETS / name).read_bytes()
    return "data:image/jpeg;base64," + base64.b64encode(raw).decode()


def _pct(seconds: float) -> float:
    """Seconds into the cycle -> percentage of the cycle."""
    return seconds / REPLAY_EVERY * 100


def _show_at(name: str, seconds: float, ramp: float = 0.01) -> str:
    """A keyframe set: hidden, then visible from `seconds`, then faded out at the end of the cycle."""
    p = _pct(seconds)
    return (f"@keyframes {name}{{0%,{p:.3f}%{{opacity:0}}"
            f"{p + ramp:.3f}%,{FADE_AT}%{{opacity:1}}100%{{opacity:0}}}}")


def _typed_html(text: str):
    """Wrap every letter in a span with its own keyframes. Returns (html, keyframes_css, finish_time)."""
    words, frames, n = [], [], 0
    for word in text.split(" "):
        letters = []
        for ch in word:
            frames.append(_show_at(f"dhf-l{n}", START_DELAY + n * LETTER_GAP))
            letters.append(f'<span class="ch" style="animation-name:dhf-l{n}">{_html.escape(ch)}</span>')
            n += 1
        words.append(f'<span class="wd">{"".join(letters)}</span>')
        n += 1                                   # the space between words takes one beat too
    return " ".join(words), "".join(frames), START_DELAY + n * LETTER_GAP


def typed_hero(headline: str, subtext: str, image: str, alt: str = ""):
    """Show the photo hero with the headline typing itself out, replaying every REPLAY_EVERY seconds."""
    typed, frames, end = _typed_html(headline)
    frames += _show_at("dhf-cur", end)
    frames += _show_at("dhf-sub", end + 0.3, ramp=3.0)
    page = (
        f'<style>{frames}</style>'
        f'<div class="hero-photo" role="img" aria-label="{_html.escape(alt)}" '
        f'style="background-image:url({_data_uri(image)})">'
        f'<div class="inner">'
        f'<h1 aria-label="{_html.escape(headline)}"><span aria-hidden="true">{typed}'
        f'<span class="cur" style="animation-name:dhf-cur"><span class="blink"></span></span></span></h1>'
        f'<p class="sub">{_html.escape(subtext)}</p>'
        f'</div></div>')
    st.markdown(CSS + page, unsafe_allow_html=True)