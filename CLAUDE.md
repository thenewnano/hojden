# Brf Höjden: website migration (Joomla -> Styrelseproffset)

You are working for the chairman of **Bostadsrättsföreningen Höjden i Göteborg** (84 apartments, Ekebäckshöjd, Göteborg; org.nr 769639-3391). Swedish content, English chat. The chairman is the admin and decides content; take initiative but follow the rules in "Safety rules".

## Status (2026-10-25)
The new site is **built, live and under review**: https://www.brftorget.se/brfhojdenigoteborg/ (portal slug `brfhojdenigoteborg`).
- 34 pages (3 members-only), 36 news posts (all members-only), 6-item menu, 52 documents/images in the file archive.
- Site is **noindex** (hidden from search engines) until launch. Domain `brfhojdengbg.se` still points to the OLD Joomla site; nothing about the domain has been changed.
- The chairman created a member login and confirmed news is private. The member register is otherwise empty (no members imported yet).
- Everything is documented in: `build-tracking.md` (every page/news id, notes, decisions, open items), `settingslog.md` (every portal setting changed), `build-actions.log` (machine log of writes, gitignored).
- **Keep those two .md files up to date after every change** (regenerate tracking with `python3 make_docs.py`, which reads `build.json` + `make_docs.py` text; edit the text inside `make_docs.py` for decisions/open items; add rows to `settingslog.md` by hand).

### Open items
- Stämma protocol of 26 June 2025: chairman will provide the file; upload it and add to page `ekonomi` (members-only).
- Header image is a rendering (`ekebackshojd-hus-d`), previously a Stena Fastigheter press photo: usage terms not verified.
- Member register import + data-processing agreement (personuppgiftsbiträdesavtal) with Styrelseproffset; then test the members-only pages/news as a real member.
- Domain/go-live: not started. Chairman chose to keep reviewing first. Checklist idea: find who controls the domain/DNS/e-mail, ask Styrelseproffset support to attach `brfhojdengbg.se` (see `styrelseproffset-plan.md`), note old DNS/MX, switch noindex OFF, keep Joomla live 2-4 weeks. Decide cookie consent (currently off) before launch.
- 28 of 36 news dates are **estimates** (old site showed no dates). Flagged in `build-tracking.md`.
- Revoke the API key (`SP_API_KEY`) when the build work is finished (portal: Inställningar > API-nycklar). Delete `.env` when done.
- Starter pages 21511-21515 (Om föreningen, Styrelse, Stadgar och årsmöten, Information A-Ö, Kontakta oss) are drafts, not deleted; delete from the portal if no longer wanted.
- 2023 storage-hours rule and similar old newsletter rules were deliberately NOT put on pages (no longer valid per chairman).

## How to access the site (read this first)
Credentials live in `.env` (gitignored; never print, copy or commit values): `BRF_USER`/`BRF_PASS` (old Joomla admin), `SP_USER`/`SP_PASS` (Styrelseproffset portal login), `SP_API_KEY` (portal API key). Parse it with `dict(l.rstrip("\n").split("=",1) ...)`, NOT `source` (values may contain spaces/special characters).

- **Portal** = https://www.styrelseproffset.se/portal (admin). Public site = brftorget.se/brfhojdenigoteborg.
- **Login is rate-limited** ("För många inloggningsförsök. Vänta en stund"; locked for ~1 hour after ~10 scripted logins). `spbuild.login()` saves the session cookie in `.sp_session` and reuses it, so scripts log in at most once. Always call `sb.login()` at the start of a script; never log in in a loop.
- If the session is stale AND logins are locked: use the chairman's logged-in Chrome (`mcp__claude-in-chrome__*` tools; load via ToolSearch; call `tabs_context_mcp` first; open a NEW tab) and run form posts in the page with `fetch` (see `runner.js`). The browser session cookie is HttpOnly, so it cannot be reused from scripts.
- **API key** (Bearer): `https://www.styrelseproffset.se/api/...`, docs at /api/dokumentation (needs login). It covers files, notes, meetings, messages etc., but **has no endpoints for website pages, news, menu or site settings** (only `GET /api/site/page/list`). We use it only for file upload/list/delete. `GET /api/files/folder-json/{id}` lists folders (0 = root).
- Python env: `.venv/bin/python` (requests, bs4, lxml, markdown, markdownify). Recreate if missing: `python3 -m venv .venv && .venv/bin/pip install requests beautifulsoup4 markdownify lxml markdown`. System `python3` has Pillow (for image resizing).

## Everyday tasks (all verified unless marked)
Source of truth for page text: **`site_pages.py`** (`page(key, title, section, html, access, docs=[...], note)`, plus `SLUGS`). Links between pages are written as `href="slug"` or `href="sidor/slug"`; `push_page.py` rewrites them to `internal://sitepage-<id>/`, which the platform resolves (survives a domain change). Page ids: `build-ids.json` (`pages` and `news`).

| Task | How |
|---|---|
| Change a page | edit its spec in `site_pages.py`, then `.venv/bin/python push_page.py <key>`; check with `python verify_site.py` (anonymous check of all pages; refresh `build.json` first if you changed text: see below) |
| New page | add `page(...)` + slug in `SLUGS`; `.venv/bin/python new_page.py <key> "Menu group"` (creates, publishes, adds to menu; script untested as a whole, its parts in `portal_ops.py` were tested) |
| Upload a document/image | `portal_ops.upload_file(path, "Föreningen"|"Boende"|"Skötsel"|"Nyhetsbilagor"|"Bilder")` (API, records id in `files.json`); then list the file name in the page's `docs=[...]` and `push_page.py <key>` |
| Create news | `portal_ops.create_news(title, html, "YYYY-MM-DD", "HH:MM")` (always author "Styrelsen", **notifications suppressed**, published) |
| Edit news | `portal_ops.edit_news_body(portal_id, fn)` |
| Menu | `portal_ops.menu_add_page(page_id, "Group text", position)`, `menu_remove_page(page_id)`, `menu_rows()` |
| Site setting | `portal_ops.set_site_setting("probe_field", field=value)`; log it in `settingslog.md` |
| Header image | prepare a JPEG (max 1150 px wide, ~150 kB), `portal_ops.set_header_image(path)` |
| Delete (own test items only) | `portal_ops.delete_page / delete_news` (portal trash, recoverable), `delete_file` |
| Logs/docs | `settingslog.md` by hand; `python3 make_docs.py` regenerates `build-tracking.md` from `build.json` |

After editing text in `site_pages.py`, refresh the checker data:
`python3 -c "import json,site_pages as sp;b=json.load(open('build.json'));f={p['key']:p for p in sp.finalize()};[p.update(html=f[p['key']]['html'],docs=f[p['key']]['docs'],note=f[p['key']]['note']) for p in b['pages']];json.dump(b,open('build.json','w'),ensure_ascii=False)"`
(`make_build.py` rebuilds `build.json` from scratch and UPLOADS it to the archive; only rerun it for a full rebuild.)

## Portal knowledge (hard-won)
- **Forms**: the portal is classic server-rendered forms. Read the form with BeautifulSoup, send *all* fields. **Repeated field names must stay repeated** (`module_ids[]`, `module_types[]`...): `spbuild.form_fields` returns lists for them. An earlier version collapsed them and silently dropped text edits on pages with 2+ modules.
- Page edit: `/portal/sites/page/edit.php?id=N`. Fields: `title`, `slug`, `state` (**1 = Utkast/draft, 2 = Publicerad**), `access_type` (**1 none/public, 2 password, 3 member login**), `access_password`, text module `module_1_<id>_text` (TipTap rich text; server stores the posted HTML), files module `module_5_<id>_file`. Create: `/portal/sites/page/create.php` with `title` + `modules[]` (1 text, 2 headline, 4 contact form, 5 files, 6 image, 9 calendar, 12 meta info; "Överskrift"(2) is pre-ticked: leave it out, the page title already renders as heading).
- **Files on a page**: set `module_5_<id>_file` to a comma list `1401-<fileid>,1401-<fileid>` (1401 = file entity type; 1402 = folder). Setting the *folder* field (`1402-id`) via a plain POST did NOT work; individual files do. File table renders with download links containing an auth hash, so links are stable only through the module.
- **Page text links**: use `internal://sitepage-<id>/` for page links. Plain relative links break (page is served at `/sidor/<slug>` while the front page is at the site root).
- **News**: `/portal/sites/update/edit.php[?id=N]`: `title`, `body`, `author_id` (0 = "Styrelsen"), `published_from_date` + `published_from_time` (backdating works), `state` (default is **Publicerad!**; 1 draft, 2 published), `suppress_notification` (**always tick**; there are 0 subscribers, but never email anyone by accident), `slug` auto. News has no file module; attachments live on page `bilagor-till-nyheter` (not in menu; linked from news 519, 521, 537) and on the page that owns them (518 -> brandskydd, 522 -> bil-och-cykelpool).
- **News lock**: `has_locked_siteupdates` ("Lås nyheter") is ON: visitors see "Hittade inga nyheter". There is no per-post restriction, so *all* news is members-only (chairman's decision).
- **Member-only pages** show "Denna sida är skyddad" + login to anonymous visitors. Members log in with the e-mail in the member register (portal Medlemmar; Excel import exists at `/portal/members/import.php`). BankID login is optional and costs money: left off.
- **Menu** `/portal/sites/menu/structure.php`: parallel arrays `menuitem_ids[] parents[] ordering[] itemtypes[] pageids[] texts[] links[]`. Item types **1 page, 2 link, 3 text (group), 4 headline**. New rows have empty id; children reference the parent's item id (save parents first, then read ids, then add children). Removing an item needs `menuitem_delete[]=<item id>`; merely omitting a row does NOT delete it. Template rows (empty ids) are part of the form HTML: ignore them.
- **Settings** `/portal/sites/site/edit.php`: one `<form>` per tab, each with its own Spara; submitting a form from a hidden tab in the browser does nothing. Key fields: `has_login`, `has_locked_siteupdates`, `is_noindex`, `index_type` (`updates`|`page`) + `index_page`, `description`, `cookie_consent`, header `photo_upload`. **`is_locked` is "Deaktivera hemsida" (turns the whole site off): never tick it.**
- **Selectors**: Tagify item selector `GET /api/itemselector/find?scope=1401&query=<text>` returns `{value:"1401-id", ...}` (param is `query`, not `q`).
- **Uploads**: `/portal/files/upload_simple.php` is flaky (returned 400 but still stored the file: check for stray duplicates). The API upload is reliable; `owner_id` 0 = root; folders get created with `folder_new`/`folder_new_name`.
- **Unicode**: exported file names use decomposed å/ä/ö (NFD). Compare with `unicodedata.normalize("NFC", ...)`; `files.json` keys are NFC.
- Chrome tool quirks: it blocks output that looks like URLs/query strings (strip `=?&`); `window.SP` is already used by the portal; browser window cannot be resized below ~half the screen (use a narrow iframe to emulate a phone); tabs sometimes cannot be closed.
- Slugs of the site: pages at `/sidor/<slug>`, news list `/nyheter`, login `/loggain`. Site-specific CSS/menu are template-driven; the header image is the only theme setting we changed.

## Content rules and decisions (from the chairman)
- **All news private.** Chairman's phone number may stay public (Styrelse, Kontakta styrelsen, front page). Personal data (valberedning's Gmail, ARC property manager's direct number, Stena jour numbers, Balkongrutan salesperson) only on members-only pages (`medlemskontakter`, `ekonomi`, `bilagor`) or in members-only news.
- The Dropbox PDF from the old board archive contained a plaintext password (rotated by the chairman); it is NOT migrated. Do not migrate board-internal files.
- **Facts confirmed by the chairman** (don't revert to old text): ARC Fastighetspartner is the manager (since 1 Sep 2024; Stena only for areas outside the stairwells: courtyards, garage, roof park, lounge; Stena jour 0771-80 50 60). Parking: 36 spaces (27 regular at 1 061 kr/month + 9 charging), all rented; ARC assigns/cancels (3 months notice); ePARK activates the permit (operator since 1 Sep 2025; cancelling in ePARK does not end the BRF contract); buyers may take over a seller's space without queue; renting directly from ePARK = external, plus VAT. Car pool = KINTO Share (since 1 May 2025). Cykelpool: register in the GoRide app, otherwise contact the board (still Stena-run). Laundry: book on the screen in the lounge outside the tvättstuga, log in with the tag. Broadband/TV: common Tele2 contract, 151 kr/month added to the fee (broadband, basic TV, Wi-Fi router); each new member must phone Tele2 to activate. Bike rooms: upper garage (under Sjupundsgatan 43), a bike storage at no. 31 (permanent), the lower-garage room (under no. 13) is closed, unused barnvagnsrum may take bikes. Repairs: ARC handles common areas for the BRF; inside the apartment mostly the owner's cost (ARC can help, billed to the member); warranty issues go to Stena, which handles them with Skanska; BRF issues: ARC, usually with board approval.
- Members-only pages stay visible in the menu (chairman chose that). Estimated news dates stay.
- Text from the Bostadsrätterna brochures is summarised in own words with credit; the PDFs are **linked, not hosted** (copyright). Do not upload them unless the chairman confirms permission.
- Never invent facts about the association. When unsure, ask the chairman (AskUserQuestion works well, one question at a time).

## Files in this folder
- `CLAUDE.md` this file; `build-tracking.md`, `settingslog.md`, `styrelseproffset-plan.md` (platform research, early); `build-actions.log` (gitignored).
- Build code: `site_pages.py` (content), `spbuild.py` (session, form reading, logging), `portal_ops.py` (operations), `push_page.py`, `new_page.py`, `upload_files.py` (initial bulk upload), `make_build.py` (full rebuild, news dates), `make_docs.py` (tracking generator), `verify_site.py`, `runner.js` (Chrome fallback).
- Data: `build.json` (page/news payload; contains members-only text: gitignored), `build-ids.json` (page and news ids), `files.json` (file name -> archive id), `site.json` (older spec, stale).
- Old site extraction: `crawl.py` (`python crawl.py public|private`; private logs in with `BRF_USER/BRF_PASS`; skips `/logga-ut/` pages which log you out), `postclean.py`, `export/` (public), `export_private/` (full, gitignored; pages/*.md, assets/, filarkivet/). **Do not re-run crawl.py into the same folders**: later manual edits there are superseded by `site_pages.py` and would be overwritten. The old site brfhojdengbg.se (Joomla 3, Simply BRF) is still live; its Email-Protector plugin cloaks e-mail addresses with random attribute prefixes (crawl.py decodes them).
- Nothing is committed to git yet. Do not commit unless the chairman asks (`.gitignore` already excludes secrets and private content).

## Safety rules
- Never send notifications/e-mails to members or subscribers; always suppress on news. Never import members or change billing/domain/DNS without explicit approval.
- Never tick "Deaktivera hemsida"; keep noindex ON until the chairman says launch; don't enable BankID/cookie-consent changes without asking.
- Don't publish anything impersonating others; don't copy copyrighted text/PDFs; don't print secrets or paste them in chat (an old password once leaked into the chat transcript: avoid repeating it).
- Only delete items you created yourself (test pages/news go to the portal trash). Ask before deleting anything else.
- Verify as an anonymous visitor after publishing (`verify_site.py`), and log what you changed.
