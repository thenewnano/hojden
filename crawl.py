"""Crawl brfhojdengbg.se (Joomla) into Markdown + images + attachments."""
import hashlib
import json
import os
import re
import sys
import time
from urllib.parse import urljoin, urlparse, unquote

import requests
from bs4 import BeautifulSoup
from markdownify import markdownify

BASE = "https://www.brfhojdengbg.se"
OUT = "export"
SKIP = re.compile(r"/(logga-ut|loggain|skapakonto|administrator|component/users)|format=|print=|tmpl=|view=(reset|remind|registration)")
FILE_EXT = re.compile(r"\.(pdf|docx?|xlsx?|pptx?|zip|jpe?g|png|gif|webp|svg|txt|csv)$", re.I)

FEED_DATES = {}
s = requests.Session()
s.headers["User-Agent"] = "brf-migration-export/1.0"


def login(user, pw):
    r = s.get(f"{BASE}/loggain")
    soup = BeautifulSoup(r.text, "lxml")
    form = next((f for f in soup.find_all("form") if f.find("input", {"name": "password"})), None)
    if not form:
        sys.exit("login form not found")
    data = {i["name"]: i.get("value", "") for i in form.find_all("input") if i.get("name")}
    data.update(username=user, password=pw)
    r = s.post(urljoin(r.url, form.get("action") or r.url), data=data)
    if "logout" not in r.text.lower() and "logga ut" not in r.text.lower():
        sys.exit("login failed")
    print("logged in")


def norm(url):
    u = urlparse(urljoin(BASE + "/", url))
    if u.netloc not in ("www.brfhojdengbg.se", "brfhojdengbg.se"):
        return None
    path = re.sub(r"^/index\.php", "", u.path).rstrip("/") or "/"
    q = f"?{u.query}" if re.fullmatch(r"(start|limit)=\d+(&(start|limit)=\d+)*", u.query) else ""
    return BASE + path + q


def slug(url):
    p = urlparse(url)
    name = (p.path.strip("/") or "index").replace("/", "__")
    return name + (f"__{p.query.replace('=', '')}" if p.query else "")


def save_asset(url, assets_dir):
    full = urljoin(BASE + "/", url)
    name = os.path.basename(unquote(urlparse(full).path)) or "file"
    dest = os.path.join(assets_dir, name)
    if os.path.exists(dest):
        return name
    r = s.get(full)
    if r.status_code != 200:
        print("  asset failed", r.status_code, full)
        return None
    with open(dest, "wb") as f:
        f.write(r.content)
    return name


def uncloak_emails(html, body):
    """Email Protector splits each address over nested spans. The attribute-name
    prefixes are random per request and named in the page's inline script:
    local-part pieces concatenate in document order, domain pieces are prepended."""
    prefixes = re.findall(r'indexOf\("data-ep-(\w+)"\)', html)
    if len(prefixes) < 2:
        return
    p_local, p_domain = prefixes[0], prefixes[1]
    for span in body.select("span.cloaked_email"):
        local, domain = "", ""
        for sp in span.find_all("span"):
            for k, v in sp.attrs.items():
                if k.lower().startswith("data-ep-" + p_local):
                    local += v
                elif k.lower().startswith("data-ep-" + p_domain):
                    domain = v + domain
        if domain:
            target = span.parent if span.parent and span.parent.name == "a" else span
            if target.parent is not None:  # anchor may already be replaced by an earlier span
                target.replace_with(local + domain)


def process(url, assets_dir, pages_dir, seen_links):
    r = s.get(url)
    if r.status_code != 200:
        print("skip", r.status_code, url)
        return None
    soup = BeautifulSoup(r.text, "lxml")
    for a in soup.find_all("a", href=True):
        n = norm(a["href"])
        if n and not SKIP.search(n) and not FILE_EXT.search(n):
            seen_links.add(n)
    body = soup.select_one("#t3-content") or soup.select_one(".item-page") or soup.body
    uncloak_emails(r.text, body)
    for t in body.select("script,style,.pager,.article-info,.print-icon,.icons,.pagination"):
        t.decompose()
    title = (body.find(["h1", "h2"]) or soup.title).get_text(" ", strip=True)
    date = FEED_DATES.get(url)
    for a in body.find_all("a", href="#"):
        a.decompose()
    for img in body.find_all("img", src=True):
        if re.search(r"/(templates|media)/", img["src"]):  # template UI icons, not content
            img.decompose()
            continue
        name = save_asset(img["src"], assets_dir)
        if name:
            img["src"] = f"assets/{name}"
    for a in body.find_all("a", href=True):
        h = a["href"]
        if FILE_EXT.search(urlparse(h).path) and norm(h):
            name = save_asset(h, assets_dir)
            if name:
                a["href"] = f"assets/{name}"
    md = markdownify(str(body), heading_style="ATX")
    md = re.sub(r"\n{3,}", "\n\n", md).strip()
    front = f"---\ntitle: {json.dumps(title, ensure_ascii=False)}\nsource: {url}\n" + (f"date: {date}\n" if date else "") + "---\n\n"
    with open(os.path.join(pages_dir, slug(url) + ".md"), "w") as f:
        f.write(front + md + "\n")
    return title


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "public"
    out = OUT if mode == "public" else OUT + "_private"
    pages_dir, assets_dir = f"{out}/pages", f"{out}/assets"
    os.makedirs(pages_dir, exist_ok=True)
    os.makedirs(assets_dir, exist_ok=True)
    if mode == "private":
        env = dict(l.rstrip("\n").split("=", 1) for l in open(".env") if "=" in l)
        login(env["BRF_USER"], env["BRF_PASS"])
    feed = s.get(BASE + "/nyheter?format=feed&type=rss").text
    FEED_DATES.update({norm(l): d for l, d in re.findall(r"<link>([^<]+/nyheter/[^<]+)</link>.*?<pubDate>([^<]+)", feed, re.S)})
    queue = [BASE + "/", BASE + "/nyheter"]
    sm = requests.get(BASE + "/sitemap.xml").text
    queue += [m for m in re.findall(r"<loc>([^<]+)", sm) if (n := norm(m.replace("&amp;", "&")))]
    done, index = set(), []
    while queue:
        url = norm(queue.pop(0))
        if not url or url in done or SKIP.search(url) or FILE_EXT.search(url):
            continue
        done.add(url)
        links = set()
        title = process(url, assets_dir, pages_dir, links)
        if title:
            print("ok", url)
            index.append({"url": url, "title": title, "file": slug(url) + ".md"})
        queue += sorted(links - done)
        time.sleep(0.3)
    with open(f"{out}/index.json", "w") as f:
        json.dump(index, f, ensure_ascii=False, indent=1)
    print(len(index), "pages")


main()
