import json, re, requests
from bs4 import BeautifulSoup
B = "https://www.brftorget.se/brfhojdenigoteborg/sidor/"
pages = json.load(open("build.json"))["pages"]
bad = 0
for p in pages:
    r = requests.get(B + p["slug"], timeout=30)
    t = BeautifulSoup(r.text, "lxml"); m = t.select_one("main") or t.body
    txt = re.sub(r"\s+", " ", m.get_text(" ", strip=True))
    protected = "Denna sida är skyddad" in txt
    files = [a for a in m.find_all("a", href=True) if "download.php" in a["href"]]
    internal = "internal://" in r.text
    probe = re.sub(r"<[^>]+>", " ", p["html"]); probe = re.sub(r"\s+", " ", probe).strip()[:40]
    ok = (protected if p["access"] == 3 else (probe[:25] in txt and not protected)) and len(files) == len(p["docs"]) * (0 if p["access"] == 3 else 1) and not internal and r.status_code == 200
    if p["access"] == 3: ok = ok and protected
    if not ok: bad += 1
    print(("OK  " if ok else "FAIL"), r.status_code, p["slug"].ljust(34), "members" if p["access"] == 3 else "public ", f"files {len(files)}/{len(p['docs'])}", "PROTECTED" if protected else "", "INTERNAL-LEFT" if internal else "")
print("problems:", bad)
