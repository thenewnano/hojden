"""Assemble build.json (pages + menu + news) and upload it to the portal archive for the in-browser runner."""
import json, re, unicodedata as ud, requests, markdown
import site_pages as sp

nfc = lambda s: ud.normalize("NFC", s)
files = json.load(open("files.json"))
pages = sp.finalize()
for p in pages:
    p["fileids"] = [files[nfc(d)]["id"] for d in p["docs"]]
    p["modules"] = [1] + ([5] if p["docs"] else []) + ([4] if p["key"] == "kontakt" else [])

# ---- menu --------------------------------------------------------------------------------
by = {p["key"]: p for p in pages}
tree = [("page", "start")]
tree += [("group", "Föreningen", ["om", "styrelse", "stamma", "stadgar", "bostadsratt", "grontbolan", "ekonomi"])]
tree += [("group", "Bo i huset", ["nyinflyttad", "regler", "parkering", "tvatt", "pool", "cykel", "balkong", "las", "bredband", "sopor", "andra"])]
tree += [("group", "Skötsel och underhåll", ["skotsel", "badrum", "kok", "fonster", "golv", "vaggar", "elektricitet", "ventilation", "brandskydd"])]
tree += [("group", "Felanmälan och kontakt", ["felanmalan", "kontakt", "avgift", "maklare", "medlemskontakter"])]
tree += [("link", "Nyheter", "https://www.brftorget.se/brfhojdenigoteborg/nyheter")]

# ---- news --------------------------------------------------------------------------------
# Exact dates exist only where the old RSS/homepage gave them. The rest are ESTIMATES derived from content
# (e.g. "12 maj", "4 mars") and post order. Flagged approx=True and listed in build-tracking.md.
DATES = {
 504: ("2022-11-20", "09:00", 1), 505: ("2022-11-28", "09:00", 1), 506: ("2022-12-01", "09:00", 1), 507: ("2022-12-08", "09:00", 1),
 508: ("2022-12-14", "09:00", 0), 509: ("2023-03-01", "09:00", 1), 510: ("2023-09-12", "09:00", 1), 511: ("2023-10-02", "09:00", 1),
 512: ("2023-11-01", "09:00", 1), 513: ("2023-12-05", "09:00", 1), 514: ("2024-05-14", "09:00", 1), 515: ("2024-05-20", "09:00", 1),
 516: ("2024-08-15", "09:00", 1), 517: ("2024-08-15", "09:05", 1), 518: ("2024-10-01", "09:00", 1), 519: ("2025-02-20", "09:00", 1),
 520: ("2025-03-05", "09:00", 1), 521: ("2025-03-10", "09:00", 1), 522: ("2025-04-15", "09:00", 1), 523: ("2025-05-05", "09:00", 1),
 524: ("2025-05-05", "09:05", 1), 525: ("2025-05-20", "09:00", 1), 526: ("2025-05-28", "09:00", 1), 527: ("2025-06-10", "09:00", 1),
 528: ("2025-06-26", "09:00", 1), 529: ("2025-06-30", "13:46", 0), 530: ("2025-08-09", "15:10", 1), 531: ("2025-08-09", "15:18", 0),
 532: ("2025-08-29", "09:00", 1), 533: ("2025-09-05", "09:00", 1), 535: ("2025-12-19", "09:00", 1), 536: ("2025-12-19", "09:30", 0),
 537: ("2026-02-01", "16:55", 0), 538: ("2026-03-08", "11:17", 0), 539: ("2026-07-12", "15:14", 0), 540: ("2026-09-14", "14:11", 0),
}
news = []
import glob, os
for nid, (d, tm, approx) in sorted(DATES.items()):
    f = glob.glob(f"export_private/pages/nyheter__{nid}-*.md")[0]
    raw = open(f).read()
    title = re.search(r'^title: "(.*)"$', raw, re.M).group(1)
    body = re.sub(r"\A---\n.*?\n---\n", "", raw, flags=re.S)
    body = re.sub(r"\A\s*# .*\n", "", body)                                   # title is its own field
    body = re.sub(r"^\s*!\[[^\]]*\]\(assets/[^)]*\)\s*$", "", body, flags=re.M)  # inline images: see Bilagor page
    body = re.sub(r"!\[[^\]]*\]\(assets/[^)]*\)", "", body)
    body = re.sub(r"\[([^\]]*)\]\(assets/[^)]*\)", lambda m: m.group(1) + " (se Bilagor till nyheter)", body)
    body = body.replace("\xa0", " ").strip()
    html = markdown.markdown(body, extensions=["extra", "sane_lists", "nl2br"])
    html = re.sub(r'href="/(mitt-boende|foreningen|kontakt)/[^"]*"', 'href="https://www.brftorget.se/brfhojdenigoteborg/"', html)
    news.append(dict(nid=nid, title=title, html=html, date=d, time=tm, approx=bool(approx), slug_hint=f"n{nid}"))

settings = dict(index_page="start", description="Brf Höjden i Göteborg: information för medlemmar och boende i Ekebäckshöjd.")
build = dict(pages=pages, menu=tree, news=news, settings=settings)
json.dump(build, open("build.json", "w"), ensure_ascii=False)
print(len(pages), "pages;", len(news), "news;", sum(1 for n in news if n["approx"]), "estimated dates;", os.path.getsize("build.json") // 1024, "kB")

# upload for the in-browser runner (deleted again after the build)
env = dict(l.rstrip("\n").split("=", 1) for l in open(".env") if "=" in l)
H = {"Authorization": "Bearer " + env["SP_API_KEY"]}
B = "https://www.styrelseproffset.se"
root = next(e["id"] for e in requests.get(B + "/api/files/folder-json/0", headers=H).json()["entries"] if e["name"] == "Hemsidan")
with open("build.json", "rb") as fh:
    r = requests.post(B + "/api/files/upload", headers=H, data={"owner_type": 1, "owner_id": root}, files={"file": ("build.json", fh)})
print(r.status_code, r.text[:140])
