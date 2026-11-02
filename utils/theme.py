"""Shared look, content and helpers for every page of the DHF website."""
import base64
import csv
import smtplib
import ssl
from email.message import EmailMessage
from datetime import datetime
from io import BytesIO
from pathlib import Path

import numpy as np
import streamlit as st
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
LOGO = ROOT / "assets" / "logo.jpeg"
DATA_FILE = ROOT / "data" / "submissions.csv"

# ------------------------------------------------------------------
# EDIT ME: contact details (placeholders until your brother confirms)
# ------------------------------------------------------------------
CONTACT = {
    "email": "dambaihopefoundation12@gmail.com",
    "phone": "+233 53 636 1384",           # president's line, shown in the footer
    "location": "Dambai, Oti Region, Ghana",
    "donate": "Call or message our founder, Issah Tairu, on +233 53 636 1384 to give or to ask how to support our work.",  # TODO swap for the foundation's own line / MoMo details when the new SIM is ready
}

# Public contact people (President, Vice President, Executive Secretary)
LEADERS = [
    dict(role="President and Founder", name="Issah Tairu", phone="+233 53 636 1384", tel="+233536361384"),
    dict(role="Vice President", name="Bikeko Isaac", phone="+233 59 806 1627", tel="+233598061627"),
    dict(role="Executive Secretary", name="Musfira Abass", phone="+233 59 785 1488", tel="+233597851488"),
]

# Full executive team (from the DHF proposal document)
TEAM = [
    ("President / Founder", "Issah Tairu"),
    ("Vice President", "Bikeko Isaac"),
    ("Executive Secretary", "Musfira Abass"),
    ("Programmes Coordinator", "Abdul Manaf Mustapha Abass"),
    ("Schools Outreach Officer", "Zulkiphil Umar-Farouk"),
    ("Counselling and Recovery Officer", "Gabriel Boafo"),
    ("Re-integration and Skills Officer", "Gbati Prince"),
    ("Health and Reproductive Education Officer", "Fuseini Hekima"),
    ("Finance Officer / Treasurer", "Naeim Osumanu"),
    ("Public Relations and Media Officer", "Abdulai Iddrisu Ukashar"),
    ("Deputy Public Relations Officer", "Mienuye Bright"),
    ("Partnerships and Fundraising Officer", "Gidisu Raymond Peter"),
    ("Monitoring, Evaluation and Learning Officer", "Cudjoe Mansah Harriet"),
    ("Volunteer Coordinator", "Sulemana Abdul Latif"),
    ("Logistics and Welfare Officer", "Mohammed Yakubu Shamsudeen"),
    ("Legal and Compliance Adviser", "Fuseini Warana"),
    ("Organizer", "Fuseini Alhassan"),
]

ASSETS_DIR = ROOT / "assets"

# Brand palette (sampled from the logo)
GREEN, DEEP = "#2E7D55", "#1E5A3C"                       # logo greens
TINT, MINT, PAGE_BG = "#DDF0E4", "#E8F7EE", "#F4FAF6"      # soft boxes / light text on dark / page background
BLUE, ORANGE, LEAF, INK = "#1F6FDB", "#F28A1E", "#5FB52B", "#1D2B24"

TAGLINE = "No child left behind, no life written off."

# The four pillars from the mission document, used on Home and Programs
PILLARS = [
    dict(name="Prevent", color=BLUE,
         short="Educating youth, parents and schools before problems take root.",
         items=["School visits, workshops and outreach campaigns",
                "Education for parents, teachers and the community",
                "Teenage pregnancy prevention and health education, with the Ghana Health Service"]),
    dict(name="Recover", color=ORANGE,
         short="Counseling and mentorship to help youth reclaim health and dignity.",
         items=["Counseling and mentorship for youth affected by substance abuse",
                "Referral to trained professionals where needed",
                "Support that protects each young person's dignity"]),
    dict(name="Re-integrate", color=LEAF,
         short="Pathways back to school or vocational training.",
         items=["Helping dropouts return to school",
                "Vocational and apprenticeship training",
                "Follow-up so no one slips back out"]),
    dict(name="Empower", color=GREEN,
         short="Life skills and enterprise opportunities as alternatives to drugs and idleness.",
         items=["Life-skills and leadership sessions",
                "Enterprise opportunities for young people",
                "Volunteers and campus ambassadors who give youth purpose"]),
]


def html(block: str):
    """Render HTML safely (strips indentation so Markdown never treats it as code)."""
    st.markdown("\n".join(l.strip() for l in block.splitlines() if l.strip()),
                unsafe_allow_html=True)


CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@500;700;800&family=Source+Sans+3:wght@400;600;700&display=swap');
html, body, [class*="css"], .stMarkdown, p, li {{ font-family: 'Source Sans 3', sans-serif; color: {INK}; }}
h1, h2, h3, h4 {{ font-family: 'Bricolage Grotesque', sans-serif !important; color: {DEEP}; letter-spacing: -0.01em; }}
#MainMenu, footer, header[data-testid="stHeader"], [data-testid="stSidebar"],
[data-testid="stSidebarNav"], [data-testid="collapsedControl"] {{ display: none !important; }}
.block-container, [data-testid="stMainBlockContainer"] {{ max-width: 1440px !important; padding: 1rem 3rem 0 !important; }}
@media (max-width: 640px) {{ .block-container, [data-testid="stMainBlockContainer"] {{ padding: 1rem 1rem 0 !important; }} }}
/* green page background */
.stApp {{ background-color: {PAGE_BG} !important; }}
/* the logo stands alone; the menu is a pill that stretches across the page, with the faded logo at its right end */
.st-key-navbar {{ position: relative; overflow: hidden; background: linear-gradient(100deg, {TINT} 0%, #C9E7D5 100%);
  border: 1px solid rgba(46,125,85,.20); border-radius: 999px; padding: .5rem .8rem; }}
.st-key-navbar::before {{ content: ""; position: absolute; inset: 0; pointer-events: none; opacity: .20;
  background: var(--logo) no-repeat right -2% center / auto 420%; }}
.st-key-navbar > * {{ position: relative; }}
.st-key-navbar [data-testid="stPageLink"] a {{ border-radius: 999px; width: 100%; justify-content: center; padding: .55rem 1rem; }}
.st-key-navbar [data-testid="stPageLink"] a:hover {{ background: rgba(255,255,255,.75) !important; }}
.st-key-navbar [data-testid="stPageLink"] a[aria-current="page"] {{ background: #fff !important; }}
.st-key-navbar [data-testid="stPageLink"] p, .st-key-navbar [data-testid="stPageLink"] span {{
  font-size: 1rem !important; font-weight: 700 !important; color: {DEEP} !important;
  text-transform: uppercase; letter-spacing: .08em; }}
/* phones: keep the four tabs in ONE row inside a compact rounded bar, and shrink the logo */
@media (max-width: 640px) {{
  .st-key-logo [data-testid="stImage"] {{ width: 76px !important; }}
  .st-key-logo img {{ max-width: 76px !important; }}
  .st-key-navbar {{ border-radius: 18px; padding: .25rem .35rem; }}
  .st-key-navbar::before {{ background-size: auto 260%; background-position: right -14% center; opacity: .14; }}
  .st-key-navbar [data-testid="stHorizontalBlock"] {{ flex-direction: row !important; flex-wrap: nowrap !important; gap: .1rem !important; }}
  .st-key-navbar [data-testid="stColumn"], .st-key-navbar [data-testid="column"] {{
    min-width: 0 !important; width: auto !important; flex: 1 1 0 !important; }}
  .st-key-navbar [data-testid="stPageLink"] a {{ padding: .5rem .15rem; }}
  .st-key-navbar [data-testid="stPageLink"] p, .st-key-navbar [data-testid="stPageLink"] span {{
    font-size: .68rem !important; letter-spacing: .02em !important; white-space: normal !important;
    text-align: center; line-height: 1.15; }}
}}
/* keep the faded logo behind everything */
[data-testid="stAppViewContainer"] {{ position: relative; z-index: 1; }}
[data-testid="stAppViewContainer"], [data-testid="stMain"] {{ background: transparent !important; }}
p, li {{ font-size: 1.08rem; line-height: 1.65; max-width: 70ch; }}

/* hero */
.hero {{ background: {GREEN}; border-radius: 28px 28px 28px 120px; padding: 3.5rem 3rem; margin: 1rem 0 2.5rem; }}
.hero h1 {{ color: {MINT}; font-size: clamp(2.2rem, 5vw, 3.8rem); font-weight: 800; line-height: 1.05; margin: 0 0 1rem; }}
.hero p {{ color: #fff; font-size: 1.2rem; max-width: 52ch; }}
.page-title {{ background: {TINT}; border-left: 10px solid {GREEN}; padding: 1.6rem 2rem; border-radius: 8px; margin: 1rem 0 2rem; }}
.page-title h1 {{ margin: 0; font-size: 2.4rem; }}
.page-title p {{ margin: .4rem 0 0; }}

/* pillar blocks: the colour bar echoes the leaves in the logo */
.pillar {{ border-top: 8px solid var(--c); background: #fff; padding: 1.1rem 1.2rem 1.4rem;
          box-shadow: 0 2px 14px rgba(30,90,60,.10); border-radius: 0 0 14px 14px; height: 100%; }}
.pillar h3 {{ margin: 0 0 .4rem; color: var(--c); }}
.pillar p {{ font-size: 1rem; margin: 0; }}

.statement {{ background: {TINT}; padding: 1.6rem 1.8rem; border-radius: 14px; height: 100%; }}
.statement h3 {{ margin-top: 0; }}
.cta {{ background: {DEEP}; color: #fff; padding: 2.4rem 2rem; border-radius: 20px; text-align: center; margin: 2.5rem 0 1rem; }}
.cta h2 {{ color: {MINT}; margin: 0 0 .5rem; }}
.cta p {{ margin: 0 auto; color: #fff; }}
.footer {{ border-top: 6px solid {GREEN}; margin-top: 3rem; padding: 1.5rem 0 2rem; text-align: center; font-size: .95rem; }}
.footer b {{ color: {DEEP}; }}
a:focus-visible, button:focus-visible {{ outline: 3px solid {ORANGE}; outline-offset: 2px; }}
</style>
"""


@st.cache_data
def _logo_png() -> bytes:
    """Logo with the empty margin cropped off AND the white background made transparent."""
    img = Image.open(LOGO).convert("RGB")
    arr = np.asarray(img)
    ys, xs = np.where(arr.min(axis=2) < 235)          # every pixel that is not white
    pad = 6
    img = img.crop((max(xs.min() - pad, 0), max(ys.min() - pad, 0),
                    min(xs.max() + pad, img.width), min(ys.max() + pad, img.height)))
    rgb = np.asarray(img).astype(float)
    # pure white -> fully transparent; anything darker (including the cream lettering) stays solid
    alpha = np.clip((252 - rgb.min(axis=2)) / 14, 0, 1) * 255
    out = Image.fromarray(np.dstack([rgb, alpha]).astype(np.uint8), "RGBA")
    out.thumbnail((640, 640))
    buf = BytesIO()
    out.save(buf, "PNG")
    return buf.getvalue()


# How visible the faded logo behind every page is: 0 = invisible, 1 = full strength
WATERMARK_OPACITY = 0.14


def _watermark_css() -> str:
    b64 = base64.b64encode(_logo_png()).decode()
    return f"""<style>
:root {{ --logo: url("data:image/png;base64,{b64}"); }}
.stApp::before {{ content: ""; position: fixed; inset: 0; z-index: 0; pointer-events: none;
  background: var(--logo) no-repeat center / min(72vmin, 760px); opacity: {WATERMARK_OPACITY}; }}
</style>"""


def setup(title: str):
    """Call first on every page: config, styling, faded background logo, and top navigation."""
    st.set_page_config(page_title=f"{title} | Dambai Hope Foundation",
                       page_icon=Image.open(LOGO), layout="wide",
                       initial_sidebar_state="collapsed")
    st.markdown(CSS + _watermark_css(), unsafe_allow_html=True)
    # Row: logo alone at the left, then a menu pill that stretches to the right edge of the page
    logo_col, menu_col = st.columns([1, 9], vertical_alignment="center")
    with logo_col:
        with st.container(key="logo"):
            st.image(_logo_png(), width=100)
    with menu_col:
        with st.container(key="navbar"):
            cols = st.columns(4)                            # four equal columns = tabs spread out evenly
            cols[0].page_link("app.py", label="Home")
            cols[1].page_link("pages/About.py", label="About")
            cols[2].page_link("pages/Programs.py", label="Programs")
            cols[3].page_link("pages/Get_Involved.py", label="Get involved")


def page_title(title: str, subtitle: str):
    html(f'<div class="page-title"><h1>{title}</h1><p>{subtitle}</p></div>')


def pillar_card(p: dict, detail: bool = False):
    extra = "<ul>" + "".join(f"<li>{i}</li>" for i in p["items"]) + "</ul>" if detail else ""
    html(f'<div class="pillar" style="--c:{p["color"]}"><h3>{p["name"]}</h3><p>{p["short"]}</p>{extra}</div>')


def footer():
    html(f"""
    <div class="footer"><b>Dambai Hope Foundation (DHF)</b><br>
    Restoring Hope · Redirecting Futures · Rebuilding Lives<br>
    {CONTACT['email']} · {CONTACT['phone']} · {CONTACT['location']}<br>
    © {datetime.now().year} Dambai Hope Foundation</div>""")


def save_submission(kind: str, **fields):
    """Append a form submission to data/submissions.csv."""
    DATA_FILE.parent.mkdir(exist_ok=True)
    new = not DATA_FILE.exists()
    row = {"time": datetime.now().isoformat(timespec="seconds"), "type": kind, **fields}
    with open(DATA_FILE, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["time", "type", "name", "email", "phone", "message"])
        if new:
            w.writeheader()
        w.writerow({k: row.get(k, "") for k in w.fieldnames})


def photo(name: str, caption: str):
    """Show one of the photos stored in assets/."""
    st.image(str(ASSETS_DIR / name), caption=caption, use_container_width=True)


def leader_card(l: dict):
    html(f'''<div class="statement"><h3 style="margin:0">{l["name"]}</h3>
    <p style="margin:.2rem 0 .6rem"><b>{l["role"]}</b></p>
    <p style="margin:0"><a href="tel:{l["tel"]}">{l["phone"]}</a></p></div>''')


def send_email(kind: str, name: str, email: str, phone: str, message: str) -> bool:
    """Email a form entry to the foundation's Gmail. Returns True if it was sent.

    Needs [email] sender / app_password / recipient in Streamlit secrets
    (see .streamlit/secrets.toml.example). Returns False if not set up or if sending fails.
    """
    try:
        cfg = st.secrets["email"]
        msg = EmailMessage()
        msg["Subject"] = f"[DHF website] {kind} from {name.strip()}"
        msg["From"] = cfg["sender"]
        msg["To"] = cfg["recipient"]
        msg["Reply-To"] = email.strip()          # so you can just hit Reply
        msg.set_content(
            f"New message from the DHF website\n\n"
            f"Type:    {kind}\nName:    {name}\nEmail:   {email}\n"
            f"Phone:   {phone or '-'}\n\nMessage:\n{message}\n")
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ssl.create_default_context(),
                              timeout=15, local_hostname="localhost") as server:
            server.login(cfg["sender"], str(cfg["app_password"]).replace(" ", ""))   # Gmail codes work without spaces
            server.send_message(msg)
        return True
    except Exception:
        return False