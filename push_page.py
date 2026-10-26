"""Re-push one page (text, access, files) to the portal: python push_page.py <key>
Uses the saved portal session (spbuild.login) and build-ids.json; links become internal://sitepage-ID/."""
import json, re, sys, unicodedata as ud
import spbuild as sb, site_pages as sp

key = sys.argv[1]
ids = json.load(open("build-ids.json"))["pages"]
files = json.load(open("files.json"))
pages = {p["key"]: p for p in sp.finalize()}
slug2id = {p["slug"]: ids[k] for k, p in pages.items() if k in ids}
p = pages[key]
html = re.sub(r'href="(?:sidor/)?([a-z0-9-]+)"', lambda m: f'href="internal://sitepage-{slug2id[m.group(1)]}/"' if m.group(1) in slug2id else m.group(0), p["html"])
sb.login()
pid = ids[key]
t = sb.soup(f"/portal/sites/page/edit.php?id={pid}")
f, d = sb.form_fields(t, r"page/edit")
tx = next(k for k in d if re.fullmatch(r"module_1_\d+_text", k))
d.update({"title": p["title"], "slug": p["slug"], "state": "2", "access_type": str(p["access"]), "access_password": "", tx: html})
if p["docs"]:
    fl = next(k for k in d if re.fullmatch(r"module_5_\d+_file", k))
    d[fl] = ",".join("1401-%d" % files[ud.normalize("NFC", n)]["id"] for n in p["docs"])
btn = next(b for b in f.find_all("button") if "Spara" in b.get_text())
if btn.get("name"):
    d[btn["name"]] = "1"
r = sb.s.post(sb.B + f"/portal/sites/page/edit.php?id={pid}", data=d)
sb.log(f"{r.status_code} PUSH page {key} ({pid})")
print(key, pid, r.status_code)
