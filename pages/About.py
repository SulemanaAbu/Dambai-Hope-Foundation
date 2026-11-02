import pandas as pd
import streamlit as st
from utils import theme

theme.setup("ABOUT")
theme.page_title("About us", "Who we are, what we want to achieve, and what we stand for")

# --- Who we are -------------------------------------------------------------
st.markdown("### Who we are")
st.write("Dambai Hope Foundation (DHF) is a youth-focused non-governmental organisation based in Dambai. "
         "We work with young people whose lives are being held back by drug abuse or by leaving school too early.")
st.write("Our team of volunteers visits schools, runs workshops, offers counseling and mentorship, and helps "
         "young people find their way back to the classroom or into a trade. Our motto says it all: "
         "no child left behind, no life written off.")

# --- The problem ------------------------------------------------------------
st.markdown("### Why we exist")
st.write("In Dambai, drug abuse and school dropout feed each other. A young person who leaves school has fewer "
         "options, and one caught up in drugs often cannot stay in class. Without early education, support and "
         "a clear path forward, talent and potential are lost. DHF steps in at every stage: before problems "
         "begin, during recovery, and on the road back to learning and work.")

theme.photo("outreach_session.jpg", "An outreach session with students")

# --- Goals ------------------------------------------------------------------
st.markdown("### Our goals")
goals = [
    ("Prevent drug abuse", "Reach youth, parents and schools with education before problems take root.", theme.BLUE),
    ("Support recovery", "Offer counseling and mentorship so young people can reclaim their health and dignity.", theme.ORANGE),
    ("Bring young people back to learning", "Open pathways into school, vocational training and apprenticeships.", theme.LEAF),
    ("Build independence", "Teach life skills and create enterprise opportunities as alternatives to drugs and idleness.", theme.GREEN),
]
cols = st.columns(2, gap="medium")
for i, (t, d, c) in enumerate(goals):
    with cols[i % 2]:
        theme.html(f'<div class="pillar" style="--c:{c};margin-bottom:1rem"><h3>{t}</h3><p>{d}</p></div>')

# --- Values -----------------------------------------------------------------
st.markdown("### What we stand for")
for t, d in [
    ("Hope.", "Every young person can heal, learn and thrive, whatever their past."),
    ("Dignity.", "We treat every young person with respect and protect their privacy."),
    ("Protection.", "Child protection and safeguarding guide everything we do."),
    ("Community.", "Lasting change happens when families, schools and leaders work together."),
    ("Opportunity.", "School and skills training open doors that drugs close."),
    ("Accountability.", "We track our results, listen to feedback and report openly to our partners."),
]:
    st.markdown(f"**{t}** {d}")

# --- Team -------------------------------------------------------------------
st.markdown("### Our leadership")
cols = st.columns(3, gap="medium")
for col, l in zip(cols, theme.LEADERS):
    with col:
        theme.leader_card(l)

with st.expander("Meet the full executive team"):
    st.table(pd.DataFrame(theme.TEAM, columns=["Role", "Name"]).set_index("Role"))

theme.photo("team_with_students.jpg", "DHF volunteers with students")

theme.footer()
