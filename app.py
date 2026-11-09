"""Home page. Run the site with:  streamlit run app.py"""
import streamlit as st
import streamlit.components.v1 as components
from utils import gallery, hero, links, theme

theme.setup("Home")

# ------------------------------------------------------------------
# EDIT ME: the photos in the sliding strip under "Our work on the ground".
# Save a photo in the assets/ folder, then add a line here: ("file name", "caption").
# ------------------------------------------------------------------
PHOTOS = [
    ("outreach_session.jpg"),
    ("book_presentation.jpg"),
    ("team_with_students.jpg"),
]

# Link buttons: green with white text
st.markdown(f"""
<style>
[data-testid="stLinkButton"] a {{ background: {theme.GREEN} !important; border: none !important; }}
[data-testid="stLinkButton"] a:hover {{ background: {theme.DEEP} !important; }}
[data-testid="stLinkButton"] a, [data-testid="stLinkButton"] a p {{ color: #fff !important; font-weight: 700; }}
</style>
""", unsafe_allow_html=True)

# Hero: team photo with the motto typing itself out when the page opens
hero.typed_hero(
    headline=theme.TAGLINE,
    subtext=("Dambai Hope Foundation helps young people in Dambai break free from "
             "drug abuse and get back into school or skills training."),
    image="team_with_students.jpg",
    alt="DHF volunteers with students after a school outreach session",
)

# Mission and vision
c1, c2 = st.columns(2, gap="large")
with c1:
    theme.html("""<div class="statement"><h3>Our mission</h3>
    <p>To restore hope, redirect futures, and rebuild lives by tackling drug abuse and school dropout
    among the youth of Dambai, so that every young person has the chance to heal, learn, and thrive.</p></div>""")
with c2:
    theme.html("""<div class="statement"><h3>Our vision</h3>
    <p>A Dambai where every young person is free from drug abuse, is in school or skills training,
    and grows up with dignity, purpose, and opportunity, within a community that protects, supports,
    and believes in its youth.</p></div>""")

# Four pillars
st.markdown("## How we work")
cols = st.columns(4, gap="medium")
for col, p in zip(cols, theme.PILLARS):
    with col:
        theme.pillar_card(p)
st.page_link("pages/Programs.py", label="See our programs in detail")

# Photos from the field: cards sliding from left to right
st.markdown("## Our work on the ground")
gallery.photo_marquee(PHOTOS)

# More photos: your Google Drive album (appears once you paste the link in utils/links.py)
if links.PHOTOS_DRIVE_URL:
    st.markdown("### More from our outreach")
    st.write("Browse more photos from our school visits and community outreach.")
    st.link_button("Open the full photo album", links.PHOTOS_DRIVE_URL, type="primary")
    if links.EMBED_ALBUM and links.album_embed_url():
        components.iframe(links.album_embed_url(), height=520, scrolling=True)

# Call to action
theme.html("""<div class="cta"><h2>Every young person deserves a second chance</h2>
<p>Volunteer, partner with us, or support our work.</p></div>""")
st.page_link("pages/Get_Involved.py", label="Get involved today")

theme.footer()