import re
import streamlit as st
from utils import theme

theme.setup("Get involved")
theme.page_title("Get involved", "Volunteer, partner with us, donate, or just say hello")

# ------------------------------------------------------------------
# EDIT ME: who people should contact to donate.
# Change these three lines when the foundation gets its own SIM / Mobile Money number.
# ------------------------------------------------------------------
DONATE_WHO = "Issah Tairu, President and Founder"
DONATE_PHONE = "+233 53 636 1384"
DONATE_TEL = "+233536361384"

# Styles for this page only (the donate card, the larger contact cards, the send button)
st.markdown(f"""
<style>
.donate {{ background: linear-gradient(120deg, {theme.DEEP}, {theme.GREEN}); border-radius: 22px;
  padding: 2.2rem 2.4rem; margin-top: 1.5rem; box-shadow: 0 8px 24px rgba(30,90,60,.25); }}
.donate h2 {{ color: {theme.MINT} !important; font-size: 2.3rem; margin: 0 0 .6rem; }}
.donate p {{ color: #fff !important; font-size: 1.2rem; max-width: none; margin: 0 0 1.1rem; }}
.donate a.num {{ display: inline-block; background: #fff; color: {theme.DEEP} !important; font-size: 1.9rem;
  font-weight: 800; padding: .5rem 1.5rem; border-radius: 999px; text-decoration: none; }}
.donate a.num:hover {{ background: {theme.MINT}; }}
.donate .who {{ color: {theme.MINT} !important; font-weight: 700; margin: .9rem 0 0; }}
.contact-card {{ background: {theme.TINT}; border-left: 8px solid {theme.GREEN}; border-radius: 14px;
  padding: 1.2rem 1.6rem; margin-bottom: 1rem; }}
.contact-card .name {{ font-family: 'Bricolage Grotesque', sans-serif; font-size: 1.75rem; font-weight: 800;
  color: {theme.DEEP}; line-height: 1.1; }}
.contact-card .role {{ font-size: 1.15rem; font-weight: 700; margin: .3rem 0 .5rem; }}
.contact-card a {{ font-size: 1.5rem; font-weight: 800; color: {theme.DEEP} !important; text-decoration: none;
  word-break: break-word; }}
.contact-card a:hover {{ text-decoration: underline; }}
.contact-card a.small {{ font-size: 1.2rem; }}
/* Send message button: green with white text */
[data-testid="stFormSubmitButton"] button {{ background: {theme.GREEN} !important; border: none !important; }}
[data-testid="stFormSubmitButton"] button:hover {{ background: {theme.DEEP} !important; }}
[data-testid="stFormSubmitButton"] button, [data-testid="stFormSubmitButton"] button p {{
  color: #fff !important; font-weight: 700; }}
</style>
""", unsafe_allow_html=True)

left, right = st.columns([3, 2], gap="large")

with left:
    st.markdown("### Send us a message")
    with st.form("contact_form", clear_on_submit=True):
        kind = st.selectbox("I would like to", ["Volunteer", "Partner with DHF", "Donate", "Ask a question"])
        name = st.text_input("Full name")
        email = st.text_input("Email")
        phone = st.text_input("Phone (optional)")
        message = st.text_area("Message", height=140)
        sent = st.form_submit_button("Send message", type="primary")
    if sent:
        if not name.strip() or not message.strip():
            st.error("Please enter your name and a message.")
        elif not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
            st.error("Please enter a valid email address.")
        else:
            # Email it to the foundation; also keep a local copy as a backup
            emailed = theme.send_email(kind, name, email, phone, message)
            theme.save_submission(kind, name=name, email=email, phone=phone, message=message)
            if emailed:
                st.success("Thank you. Your message has been sent and we will get back to you soon.")
            else:
                st.warning("We could not send your message just now. "
                           f"Please email us directly at {theme.CONTACT['email']} or call one of the numbers on this page.")

    # Donate card, directly below the form
    theme.html(f"""
    <div class="donate">
    <h2>Support our work</h2>
    <p>Every contribution helps a young person heal, return to school and rebuild their life.
    To give, or to ask how else you can help, call or message:</p>
    <a class="num" href="tel:{DONATE_TEL}">{DONATE_PHONE}</a>
    <p class="who">{DONATE_WHO}</p>
    </div>""")

with right:
    st.markdown("### Reach us directly")
    theme.html(f"""
    <div class="contact-card"><div class="role">Email</div>
    <a class="small" href="mailto:{theme.CONTACT['email']}">{theme.CONTACT['email']}</a></div>""")
    for l in theme.LEADERS:
        theme.html(f"""
        <div class="contact-card"><div class="name">{l['name']}</div>
        <div class="role">{l['role']}</div>
        <a href="tel:{l['tel']}">{l['phone']}</a></div>""")
    st.markdown(f"**Location:** {theme.CONTACT['location']}")

theme.footer()