"""Home page. Run the site with:  streamlit run app.py"""
import streamlit as st
from utils import hero, theme

theme.setup("HOME")

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

# Photos from the field
st.markdown("## Our work on the ground")
g1, g2 = st.columns(2, gap="medium")
with g1:
    theme.photo("outreach_session.jpg", "Students listening during an outreach session")
with g2:
    theme.photo("book_presentation.jpg", "A DHF volunteer presents a book to a student")

# Call to action
theme.html("""<div class="cta"><h2>Every young person deserves a second chance</h2>
<p>Volunteer, partner with us, or support our work.</p></div>""")
st.page_link("pages/Get_Involved.py", label="Get involved today")

theme.footer()