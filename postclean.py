"""Strip CMS leftovers from a crawl: usage python postclean.py export_private"""
import glob
import os
import re
import sys

out = sys.argv[1]
ICONS = "dokument_ikon|kuvert|lock|refresh|portable4|white-dropbox-24"
for p in glob.glob(f"{out}/pages/*.md"):
    t = open(p).read()
    t = re.sub(r"^\[\]\(assets/index\.php\)\n", "", t, flags=re.M)
    t = re.sub(rf"!\[[^\]]*\]\(assets/({ICONS})\.(png|gif)\)", "", t)
    t = re.sub(r"^\* \[(Ändra|Skriv ut|Empty)\]\([^)]*\)\n", "", t, flags=re.M)
    t = re.sub(r"\n{3,}", "\n\n", t)
    t = re.sub(r"^(# .+)\n\n\1\n", r"\1\n", t, flags=re.M)
    open(p, "w").write(t)
for f in ["index.php"] + [f"{i}.{e}" for i in ICONS.split("|") for e in ("png", "gif")]:
    path = f"{out}/assets/{f}"
    if os.path.exists(path):
        os.remove(path)
