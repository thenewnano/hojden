"""Tested operations against the Styrelseproffset portal for the Brf Höjden site.

All functions use spbuild's saved session (login() reuses .sp_session; it logs in only if that is stale).
Every write is appended to build-actions.log. Page ids: build-ids.json (pages + news).
"""
import json
import re

import spbuild as sb

IDS_FILE = "build-ids.json"


def ids():
    return json.load(open(IDS_FILE))


def save_ids(d):
    json.dump(d, open(IDS_FILE, "w"), indent=1)


def _submit_btn(f):
    return next(b for b in f.find_all("button") if "Spara" in b.get_text())


# ------------------------------------------------------------------ pages
def create_page(title, modules=(1,)):
    """Create an empty page (draft). modules: 1 text, 5 files, 4 contact form, 2 headline, 6 image, 9 calendar.
    Returns the new page id."""
    sb.login()
    t = sb.soup("/portal/sites/page/create.php")
    f, d = sb.form_fields(t, r"page/create")
    d["title"] = title
    d["modules[]"] = [str(m) for m in modules]
    r = sb.s.post(sb.B + "/portal/sites/page/create.php", data=d)
    m = re.search(r"id=(\d+)", r.url)
    assert m, f"create failed {r.status_code} {r.url}"
    sb.log(f"{r.status_code} CREATE page '{title}' -> {m.group(1)}")
    return int(m.group(1))


def delete_page(pid):
    """Moves the page to the portal trash (recoverable)."""
    sb.login()
    t = sb.soup(f"/portal/sites/page/delete.php?id={pid}")
    f = next(x for x in t.find_all("form") if "delete" in (x.get("action") or ""))
    _, d = sb.form_fields(t, r"delete")
    btn = [b for b in f.find_all("button") if b.get("name")]
    if btn:
        d[btn[-1]["name"]] = "1"
    r = sb.s.post(sb.B + f.get("action"), data=d)
    sb.log(f"{r.status_code} DELETE page {pid}")
    return r.status_code


# ------------------------------------------------------------------ news
def news_form(pid):
    sb.login()
    t = sb.soup(f"/portal/sites/update/edit.php?id={pid}" if pid else "/portal/sites/update/edit.php")
    f, d = sb.form_fields(t, r"update/edit")
    return f, d


def save_news(f, d, pid=None):
    btn = _submit_btn(f)
    if btn.get("name"):
        d[btn["name"]] = "1"
    url = sb.B + "/portal/sites/update/edit.php" + (f"?id={pid}" if pid else "")
    r = sb.s.post(url, data=d)
    m = re.search(r"id=(\d+)", r.url)
    return r, (int(m.group(1)) if m else pid)


def create_news(title, html, date, time="09:00", publish=True):
    """New news post. author 'Styrelsen' (0), notifications SUPPRESSED (always). Returns portal id.
    NB: news default to *Publicerad*; publish=False makes a draft. date 'YYYY-MM-DD'."""
    f, d = news_form(None)
    d.update({"title": title, "body": html, "author_id": "0", "published_from_date": date, "published_from_time": time,
              "state": "2" if publish else "1", "suppress_notification": "1"})
    r, nid = save_news(f, d)
    sb.log(f"{r.status_code} CREATE news '{title}' -> {nid}")
    return nid


def edit_news_body(pid, fn):
    """Apply fn(old_html)->new_html to a news post body. Keeps all other fields (incl. suppress_notification)."""
    f, d = news_form(pid)
    new = fn(d["body"])
    if new == d["body"]:
        return "unchanged"
    d["body"] = new
    d["suppress_notification"] = "1"
    r, _ = save_news(f, d, pid)
    sb.log(f"{r.status_code} EDIT news {pid}")
    return r.status_code


def delete_news(pid):
    sb.login()
    t = sb.soup(f"/portal/sites/update/delete.php?id={pid}")
    f = next(x for x in t.find_all("form") if "delete" in (x.get("action") or ""))
    _, d = sb.form_fields(t, r"delete")
    btn = [b for b in f.find_all("button") if b.get("name")]
    if btn:
        d[btn[-1]["name"]] = "1"
    r = sb.s.post(sb.B + f.get("action"), data=d)
    sb.log(f"{r.status_code} DELETE news {pid}")
    return r.status_code


# ------------------------------------------------------------------ menu
def _menu_form():
    t = sb.soup("/portal/sites/menu/structure.php")
    return next(x for x in t.find_all("form") if "menu/structure" in (x.get("action") or ""))


def menu_rows():
    """Existing menu rows (template rows with empty ids are skipped)."""
    f = _menu_form()

    def col(n):
        out = []
        for i in f.find_all(["input", "select"], attrs={"name": n}):
            out.append(i.get("value", "") if i.name != "select" else ((i.find("option", selected=True) or i.find("option")).get("value", "")))
        return out
    keys = ["ids", "parents", "ordering", "itemtypes", "pageids", "texts", "links"]
    cols = {k: col(f"menuitem_{k}[]") for k in keys}
    return [{k: cols[k][i] for k in keys} for i in range(len(cols["ids"])) if cols["ids"][i]]


def _menu_post(rows, delete_ids=()):
    f = _menu_form()
    data = []
    for k in ["ids", "parents", "ordering", "itemtypes", "pageids", "texts", "links"]:
        data += [(f"menuitem_{k}[]", r[k]) for r in rows]
    data += [("menuitem_delete[]", i) for i in delete_ids] + [("save", "1")]
    r = sb.s.post(sb.B + f.get("action"), data=data)
    sb.log(f"{r.status_code} POST menu (delete {list(delete_ids)})")
    return r.status_code


def menu_add_page(page_id, group_text, position=None):
    """Add a page under the top-level group item with that text (item type 3). position = 1-based, default last."""
    sb.login()
    rows = menu_rows()
    grp = next(r for r in rows if r["texts"] == group_text and r["itemtypes"] == "3")
    sibs = sorted([r for r in rows if r["parents"] == grp["ids"]], key=lambda r: int(r["ordering"]))
    pos = position or len(sibs) + 1
    new = {"ids": "", "parents": grp["ids"], "ordering": str(pos), "itemtypes": "1", "pageids": str(page_id), "texts": "", "links": ""}
    for r in sibs:
        if int(r["ordering"]) >= pos:
            r["ordering"] = str(int(r["ordering"]) + 1)
    return _menu_post(rows + [new])


def menu_remove_page(page_id):
    sb.login()
    rows = menu_rows()
    gone = next(r for r in rows if r["pageids"] == str(page_id))
    rows = [r for r in rows if r is not gone]
    sib = sorted([r for r in rows if r["parents"] == gone["parents"]], key=lambda r: int(r["ordering"]))
    for n, r in enumerate(sib, 1):
        r["ordering"] = str(n)
    return _menu_post(rows, [gone["ids"]])


# ------------------------------------------------------------------ site settings (Hemsida > Inställningar)
def set_site_setting(probe_field, **overrides):
    """Change fields in the settings form that contains `probe_field` (each tab is its own form), e.g.
    set_site_setting('description', description='...'); set_site_setting('has_login', has_login='1').
    A checkbox is switched OFF by passing None. Returns {field: (before, after)} read back from the server."""
    sb.login()
    t = sb.soup("/portal/sites/site/edit.php")
    f = next(x for x in t.find_all("form") if x.find(["input", "select", "textarea"], attrs={"name": probe_field}))
    d = {}
    for i in f.find_all(["input", "select", "textarea"]):
        n = i.get("name")
        if not n or i.get("type") in ("submit", "button", "file", "image"):
            continue
        if i.get("type") in ("checkbox", "radio"):
            if i.has_attr("checked"):
                d[n] = i.get("value", "on")
        elif i.name == "textarea":
            d[n] = i.text
        elif i.name == "select":
            o = i.find("option", selected=True) or i.find("option")
            d[n] = o.get("value", "") if o else ""
        else:
            d[n] = i.get("value", "")
    before = {k: d.get(k) for k in overrides}
    for k, v in overrides.items():
        if v is None:
            d.pop(k, None)
        else:
            d[k] = v
    r = sb.s.post(sb.B + "/portal/sites/site/edit.php", data=d)
    sb.log(f"{r.status_code} SETTING {overrides}")
    t2 = sb.soup("/portal/sites/site/edit.php")
    after = {}
    for k in overrides:
        e = t2.find(["input", "select", "textarea"], attrs={"name": k})
        after[k] = (("on" if e.has_attr("checked") else None) if e is not None and e.get("type") in ("checkbox", "radio") else (e.get("value") or e.text if e is not None else None))
    return {k: (before[k], after[k]) for k in overrides}


def set_header_image(jpg_path, filename="header.jpg"):
    """Upload the site header image (Sidhuvud). Prepare first: JPEG, max 1150 px wide, ideally < 300 kB."""
    sb.login()
    t = sb.soup("/portal/sites/site/edit.php")
    f = next(x for x in t.find_all("form") if x.find("input", {"name": "photo_upload"}))
    d = {}
    for i in f.find_all(["input", "select", "textarea"]):
        n = i.get("name")
        if not n or i.get("type") in ("submit", "button", "file", "image"):
            continue
        if i.get("type") in ("checkbox", "radio"):
            if i.has_attr("checked"):
                d[n] = i.get("value", "on")
        elif i.name == "textarea":
            d[n] = i.text
        else:
            d[n] = i.get("value", "")
    with open(jpg_path, "rb") as fh:
        r = sb.s.post(sb.B + "/portal/sites/site/edit.php", data=d, files={"photo_upload": (filename, fh, "image/jpeg")})
    sb.log(f"{r.status_code} HEADER image {filename}")
    return r.status_code


# ------------------------------------------------------------------ files (API key, no login needed)
def _api():
    import requests
    env = dict(l.rstrip("\n").split("=", 1) for l in open(".env") if "=" in l)
    return requests, {"Authorization": "Bearer " + env["SP_API_KEY"]}, "https://www.styrelseproffset.se"


def upload_file(path, category="Föreningen", name=None):
    """Upload a document/image to archive folder Hemsidan/<category> (Föreningen, Boende, Skötsel, Nyhetsbilagor, Bilder)
    via the API and record it in files.json (key = NFC file name). Returns the file id.
    Attach it to a page by adding the name to that page's docs=[...] in site_pages.py, then push_page.py <key>."""
    import os
    import unicodedata as ud
    requests, H, B = _api()
    name = name or os.path.basename(path)
    root = next(e["id"] for e in requests.get(B + "/api/files/folder-json/0", headers=H).json()["entries"] if e["name"] == "Hemsidan")
    sub = next(e["id"] for e in requests.get(B + f"/api/files/folder-json/{root}", headers=H).json()["entries"] if e["is_folder"] and e["name"] == category)
    with open(path, "rb") as fh:
        r = requests.post(B + "/api/files/upload", headers=H, data={"owner_type": 1, "owner_id": sub}, files={"file": (name, fh)}, timeout=600)
    fid = r.json()["data"]["file_id"]
    files = json.load(open("files.json"))
    files[ud.normalize("NFC", name)] = {"id": fid, "folder": category}
    json.dump(files, open("files.json", "w"), ensure_ascii=False, indent=1)
    sb.log(f"{r.status_code} UPLOAD {name} -> {category} id {fid}")
    return fid


def delete_file(fid):
    requests, H, B = _api()
    r = requests.delete(B + f"/api/files/file/{fid}", headers=H)
    sb.log(f"{r.status_code} DELETE file {fid}")
    return r.status_code
