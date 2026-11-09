"""Links to your Google Form and Google Drive photos. Paste them between the quotation marks."""
import re

# 1) Google Form for volunteers. Open the form > Send > link icon > copy the link.
VOLUNTEER_FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLScOuaHC_LuJBkN_zYYaxgJx5uj-kV4F3BoW4N_oI7OYeZRzoA/viewform?usp=publish-editor"

# 2) Google Drive folder with the outreach photos. Right-click the folder > Share > set "Anyone with the link"
#    > Copy link.
PHOTOS_DRIVE_URL = "https://drive.google.com/drive/folders/1ydMh-H5VZ1ER1-3-WfCNZEr4846t-dCG"

# Show the photo album directly on the Home page (needs the folder shared as "Anyone with the link").
EMBED_ALBUM = True

# Show the volunteer form directly on the page instead of only a button.
# Needs the long form link (not forms.gle). If unsure, leave False.
EMBED_VOLUNTEER_FORM = False


def volunteer_embed_url() -> str:
    """The form link with Google's embed option switched on."""
    url = VOLUNTEER_FORM_URL
    if not url or "embedded=true" in url:
        return url
    return url + ("&" if "?" in url else "?") + "embedded=true"


def album_embed_url() -> str:
    """Turn a Drive folder link into the address Google uses for an embedded photo grid."""
    m = re.search(r"/folders/([\w-]+)", PHOTOS_DRIVE_URL) or re.search(r"[?&]id=([\w-]+)", PHOTOS_DRIVE_URL)
    return f"https://drive.google.com/embeddedfolderview?id={m.group(1)}#grid" if m else ""