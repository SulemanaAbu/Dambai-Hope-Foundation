"""Email checker. Run it from the project folder with:   python test_email.py

It reads .streamlit/secrets.toml, tries to log in to Gmail, sends one test email,
and tells you in plain words what is wrong if something fails.
"""
import smtplib
import socket
import ssl
import sys
import tomllib
from email.message import EmailMessage
from pathlib import Path

path = Path(".streamlit/secrets.toml")
if not path.exists():
    sys.exit("PROBLEM: .streamlit/secrets.toml was not found. Run this from the project folder, "
             "and check the file name is exactly secrets.toml (no .example, no 'copy').")

try:
    cfg = tomllib.loads(path.read_text(encoding="utf-8"))["email"]
    sender, recipient = cfg["sender"], cfg["recipient"]
    password = str(cfg["app_password"]).replace(" ", "")
except Exception as e:
    sys.exit(f"PROBLEM reading secrets.toml: {e!r}\nCheck it starts with [email] and that every value is in quotation marks.")

print(f"Sender: {sender}")
print(f"Recipient: {recipient}")
print(f"Password length (should be 16): {len(password)}")
print(f"Computer name Python normally sends to Gmail: {socket.getfqdn()!r}")
if len(password) != 16:
    print("  -> The code is not 16 characters. Paste it again from the email, with no extra letters.")

msg = EmailMessage()
msg["Subject"] = "[DHF website] test message"
msg["From"] = sender
msg["To"] = recipient
msg.set_content("If you can read this, the DHF website email setup works.")


def attempt(label, make_server):
    print(f"\nTrying {label} ...")
    try:
        with make_server() as server:
            if label.endswith("587"):
                server.starttls(context=ssl.create_default_context())
            server.login(sender, password)
            server.send_message(msg)
        print(f"SUCCESS via {label}. Test email sent to {recipient} (check Spam too).")
        return True
    except smtplib.SMTPAuthenticationError as e:
        print("Gmail REJECTED the login. The code is wrong, was made for a different Gmail than the sender,\n"
              "or was deleted. Make a new App Password for the sender account.\nDetails:", e)
        return "auth"
    except Exception as e:
        print(f"Could not complete this attempt: {e!r}")
        print("  -> Usually the network (school/office Wi-Fi, firewall or antivirus) blocking the connection.")
        return False


ctx = ssl.create_default_context()
result = attempt("port 465", lambda: smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ctx, timeout=20, local_hostname="localhost"))
if result is False:
    attempt("port 587", lambda: smtplib.SMTP("smtp.gmail.com", 587, timeout=20, local_hostname="localhost"))