"""Upload site documents/images to the portal file archive through the API (Bearer key).
Writes files.json: NFC file name -> {id, folder}. Re-runnable: skips names already present."""
import json, os, unicodedata as ud, requests

env = dict(l.rstrip("\n").split("=", 1) for l in open(".env") if "=" in l)
H = {"Authorization": "Bearer " + env["SP_API_KEY"]}
B = "https://www.styrelseproffset.se"
ASSETS = "export_private/assets/"
nfc = lambda s: ud.normalize("NFC", s)
disk = {nfc(f): f for f in os.listdir(ASSETS)}

CATS = {
    "Föreningen": ["broschyr_hojden.pdf", "Stadgar.pdf", "EkonomiskPlan.pdf", "Årsredovisning inkl revisionsberättelse 2022 (sign).pdf",
                   "Årsredovisning inkl revisionsberättelse 2023.pdf", "Protokoll ordinarie föreningsstämma 230615 (sign).pdf",
                   "Protokoll ordinarie föreningsstämma 240617 (sign).pdf", "Ekebäckshöjd kv Öst - Hus C_MB2021-0007_20211207.pdf"],
    "Boende": ["ansokan_andrahand.pdf", "Instruktion-andrahandsuthyrning-bostadsrättshavare-hyresgäst.pdf", "avtalupplatelseandrahan_BRF.pdf",
               "BILPOOLSINFO Ekebäckshöjd.pdf", "garantibevis_BRF Höjden .pdf", "garantibevis vitvaror höjden.pdf", "Skötsel tvätt.pdf",
               "Goda råd om att förebygga brand i hemmet.pdf", "Manual_brandvarnare_99x105_SE-nordic_19-06_web.pdf"],
    "Nyhetsbilagor": ["Offert Brf Höjden 2.1-komprimerad.pdf", "BR Visning Brf Höjden BF.pdf"],
    "Bilder": ["ekebackshojd-takpark-beskuren.jpg", "raformat_stena_brf-hojden_balkong_1.jpg", "raformat_stena_brf-hojden_gard_1.jpg",
               "raformat_stena_brf-hojden_gatan_1.jpg", "karta.png", "DCL_uttagen.jpeg"] + [f"IMG_{n}.jpg" for n in (1413, 1414, 1416, 1417, 1419, 1420, 1421, 1424)],
}
pages = json.load(open("site.json"))
used = {nfc(d) for p in pages for d in p["docs"]}
placed = {nfc(f) for fs in CATS.values() for f in fs}
CATS["Skötsel"] = sorted(used - placed)            # every remaining manual/care guide

def listing(fid):
    return requests.get(B + f"/api/files/folder-json/{fid}", headers=H, timeout=60).json().get("entries", [])

def upload(name, folder_id, new_name=None):
    with open(ASSETS + disk[name], "rb") as fh:
        data = {"owner_type": 1, "owner_id": folder_id}
        if new_name:
            data.update(folder_new="true", folder_new_name=new_name)
        r = requests.post(B + "/api/files/upload", headers=H, data=data, files={"file": (name, fh)}, timeout=300)
    print(r.status_code, name, r.text[:100].replace("\n", " "))
    return r

root = next(e["id"] for e in listing(0) if e["name"] == "Hemsidan")
out = json.load(open("files.json")) if os.path.exists("files.json") else {}
for cat, names in CATS.items():
    sub = next((e["id"] for e in listing(root) if e["is_folder"] and e["name"] == cat), None)
    for n in names:
        if n in out:
            continue
        assert n in disk, n
        if sub is None:
            upload(n, root, new_name=cat)
            sub = next(e["id"] for e in listing(root) if e["is_folder"] and e["name"] == cat)
        else:
            upload(n, sub)
        f = next((e for e in listing(sub) if not e["is_folder"] and nfc(e["name"]) == n), None)
        if f:
            out[n] = {"id": f["id"], "folder": cat}
        json.dump(out, open("files.json", "w"), ensure_ascii=False, indent=1)
print(len(out), "files recorded;", sum(len(v) for v in CATS.values()), "planned")
