"""Create a NEW page from its spec and publish it:  python new_page.py <key> ["Menu group"]
1) add page("<key>", ...) to site_pages.py and "<key>" to SLUGS;  2) put new documents in the archive with
portal_ops.upload_file(...) and list them in docs=[...];  3) run this.  Group = top-level menu text, e.g. "Bo i huset"."""
import subprocess
import sys

import portal_ops as po
import site_pages as sp

key = sys.argv[1]
group = sys.argv[2] if len(sys.argv) > 2 else None
p = {x["key"]: x for x in sp.finalize()}[key]
d = po.ids()
if key in d["pages"]:
    print("page already exists:", d["pages"][key])
else:
    mods = [1] + ([5] if p["docs"] else []) + ([4] if key == "kontakt" else [])
    d["pages"][key] = po.create_page(p["title"], mods)
    po.save_ids(d)
subprocess.run([sys.executable, "push_page.py", key], check=True)
if group:
    print("menu:", po.menu_add_page(d["pages"][key], group))
print("done:", key, d["pages"][key])
