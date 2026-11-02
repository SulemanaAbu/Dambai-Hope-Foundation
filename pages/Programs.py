import streamlit as st
from utils import theme

theme.setup("PROGRAMS")
theme.page_title("Our programs", "Four connected steps that take a young person from risk to opportunity")

for p in theme.PILLARS:
    theme.pillar_card(p, detail=True)
    st.write("")

theme.footer()
