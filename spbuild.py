"""Helpers for building the Brf Höjden site in the Styrelseproffset portal.

Credentials come from .env (SP_USER / SP_PASS). Every write goes through
`submit`, which appends one line to build-actions.log.
"""
import re
import time
from datetime import datetime

import requests
from bs4 import BeautifulSoup

B = "https://www.styrelseproffset.se"
SITE = "https://www.brftorget.se/brfhojdenigoteborg"
LOG = "build-actions.log"

s = requests.Session()
s.headers["User-Agent"] = "brf-migration-build/1.0"


SESSION_FILE = ".sp_session"  # gitignored; keeps the cookie so we log in once, not per run


def _logged_in(html):
    return "/member/logout.php" in html


def login():
    """Reuse the saved session; log in at most once (the portal rate-limits logins)."""
    import os
    import pickle
    if os.path.exists(SESSION_FILE):
        s.cookies.update(pickle.load(open(SESSION_FILE, "rb")))
        if _logged_in(s.get(B + "/portal").text):
            return
    env = dict(l.rstrip("\n").split("=", 1) for l in open(".env") if "=" in l)
    t = BeautifulSoup(s.get(B + "/portal").text, "lxml")
    f = t.find("form", action=re.compile("login"))
    d = {i["name"]: i.get("value", "") for i in f.find_all("input") if i.get("name")}
    d.update(email=env["SP_USER"], password=env["SP_PASS"])
    r = s.post(B + f["action"], data=d)
    if not _logged_in(r.text):
        raise SystemExit("login failed: " + BeautifulSoup(r.text, "lxml").get_text(" ", strip=True)[:200])
    pickle.dump(s.cookies, open(SESSION_FILE, "wb"))


def soup(url):
    return BeautifulSoup(s.get(B + url if url.startswith("/") else url).text, "lxml")


def form_fields(t, action_re):
    """Return (form, dict of successful-control values) for the first matching form.
    Repeated names (module_ids[] etc.) become lists, which requests sends as repeated fields."""
    f = next(f for f in t.find_all("form") if re.search(action_re, f.get("action") or ""))
    d = {}

    def put(n, v):
        if n in d:
            d[n] = (d[n] if isinstance(d[n], list) else [d[n]]) + [v]
        else:
            d[n] = v
    for i in f.find_all(["input", "select", "textarea"]):
        n = i.get("name")
        if not n or i.get("type") in ("submit", "button", "file", "image"):
            continue
        if i.name == "select":
            o = i.find("option", selected=True) or (i.find("option") if not i.get("multiple") else None)
            if o is not None:
                put(n, o.get("value", o.get_text(strip=True)))
        elif i.name == "textarea":
            put(n, i.text.lstrip("\n"))
        elif i.get("type") in ("checkbox", "radio"):
            if i.has_attr("checked"):
                put(n, i.get("value", "on"))
        else:
            put(n, i.get("value", ""))
    return f, d


def log(msg):
    with open(LOG, "a") as fh:
        fh.write(f"{datetime.now().isoformat(timespec='seconds')} {msg}\n")


def submit(url, action_re, overrides, submit_name=None, files=None, label=""):
    t = soup(url)
    f, d = form_fields(t, action_re)
    d.update(overrides)
    if submit_name:
        d[submit_name] = "1"
    r = s.post(B + (f.get("action") or url), data=d, files=files, allow_redirects=True)
    ok = r.status_code < 400
    log(f"{'OK ' if ok else 'ERR'} {r.status_code} POST {url} {label}")
    return r


def create_folder(name, parent=""):
    r = submit(f"/portal/files/folder/edit.php?folder_parentid={parent}", r"folder/edit", {"folder_name": name}, label=f"folder {name}")
    return r


def find_folder_ids():
    t = soup("/portal/files/files.php")
    return {re.sub(r"\s+", " ", tr.select_one(".col-name").get_text(" ", strip=True)): tr.get("data-folder-id") for tr in t.select("tr.folder") if tr.get("data-folder-id")}


def upload(path, folder_id, name=None):
    name = name or path.split("/")[-1]
    with open(path, "rb") as fh:
        r = s.post(B + "/portal/files/upload_simple.php", data={"MAX_FILE_SIZE": "268435456", "folder_id": str(folder_id)}, files={"file": (name, fh)})
    log(f"{'OK ' if r.status_code < 400 else 'ERR'} {r.status_code} UPLOAD {name} -> folder {folder_id}")
    return r
