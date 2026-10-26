# Migration plan: brfhojdengbg.se (Joomla/Simply BRF) -> Styrelseproffset

Research date: 2026-10-25. Only public pages were read; no login, no forms, no changes. Items marked UNVERIFIED are not confirmed by an official page.

## 1. What Styrelseproffset offers (homepage / "Foreningshemsida")

| Area | Finding | Source |
|---|---|---|
| Product | Board portal + association homepage + member app (Foreningsproffset). All functions included in every plan. | https://www.styrelseproffset.se |
| Pricing (BRF, excl. VAT/month) | <25 apartments 250 kr; 25-75: 500 kr; >75: 750 kr. First 12 months free, no card, no binding. Usage charges per 1,000: SMS 600 kr, BankID logins on the site 300 kr. What happens after the free year: not stated. | https://www.styrelseproffset.se/priser |
| Editor | Page = ordered list of modules (heading, metadata, image, gallery, text, text+image, Q&A, divider) with a rich-text (WYSIWYG) editor with fact box, important box, button, step-by-step, rule excerpt. Not Markdown. HTML module exists ("Avancerat innehall"), but scripts/iframes only run on your own domain. | https://www.styrelseproffset.se/hjalp/sidor-pa-hemsidan |
| Pages | Title + unique slug, publish from/to dates, draft with preview link, per-page header image, page width types, "show for members" (listed in member app/portal). Each page gets its own folder in the file archive; files are shown only if a "files" module is placed. | same |
| Menu | Pages placed in menu at creation; items can be a page, a label with submenu, or an external URL. Menu structure managed on a separate screen. | same |
| News | Title + body, optional image (cropped 2:1, max 800x400), from/to date (empty = save time), slug unique per year, author, draft/published, push+e-mail notification to subscribers (can be blocked), optional likes/comments. Article does not describe archive or categories; the hemsida page does list "Automatiskt arkiv" (archive exists, details UNVERIFIED). Whether the "from" date can be set to the past (needed for old news): implied but UNVERIFIED. | https://www.styrelseproffset.se/hjalp/nyheter-pa-hemsidan , /hemsida |
| Member-only | Page protection: none / shared password / member login. "Lås nyheter" setting restricts ALL news to logged-in users (site-wide, not per item). Login must be enabled in site settings. | /hjalp/sidor-pa-hemsidan , /hjalp/skapa-foreningshemsida |
| Member auth | Member's e-mail must be in the member register; member self-registers via /loggain, gets a one-time link and password by e-mail (no invitation mechanism described). BankID optional (needs personal number in register; costs credits). Access ends automatically when membership ends. Same account works in the app. | https://www.styrelseproffset.se/hjalp/skapa-inloggning-pa-foreningens-hemsida |
| Files | 100 GB, any file type, multi-upload, PDF/DOC/XLS preview, folders; Dropbox integration. File module can show a folder on a page. | /funktioner , /vanliga-fragor |
| Images | Image module, gallery, frames, in-text images. | /hjalp/sidor-pa-hemsidan |
| Design | Colors/logos via "Grafisk profil", header image (max 1150 px), custom CSS (limited support, Google Fonts via @import). "Many ready page templates" is claimed on /hemsida; exact theme set UNVERIFIED. | /hjalp/skapa-foreningshemsida |
| Domain | Own domain supported and included. Support registers and points it (you do not edit DNS yourself); certificate by support; permanent redirect from brftorget.se/<sub> option. www/apex and e-mail (MX) handling not documented: ask support. Existing hosting may be kept for personal mailboxes. | https://www.styrelseproffset.se/hjalp/egen-hemsidesdoman , /vanliga-fragor |
| Redirects | "Ompekningar" in site settings: short path -> target page, added one by one. Whether old-URL structures like /nyheter/NNN-... are supported: UNVERIFIED. | https://www.styrelseproffset.se/hjalp/ompekningar |
| Forms | Contact form module (creates e-mail ticket in board portal), form module, auto-reply. | /hemsida , /hjalp/sidor-pa-hemsidan |
| SEO/GDPR/cookies | Meta description, noindex toggle (use during build), sitemap + RSS links, optional Google Analytics with consent checkbox, cookie info link in footer. Hosting: DB in Sweden, files on AWS EU/EEA. DPA included; processor Webb Trepunktnoll AB. | /hjalp/skapa-foreningshemsida , /gdpr , /vanliga-fragor |
| Import / API | NOT found. No import, bulk upload for pages/news, API, or webhooks mentioned in FAQ, features, help index or GDPR page. Only Excel/OpenOffice import for member register. Multi-file upload to the file archive exists. An AI assistant can "create a news post on the website, ready for review" from a plain-Swedish instruction (approval required); no external API/MCP mentioned. | /vanliga-fragor , /funktioner , /ai-assistent |
| Demo / examples | https://www.brftrepunktnoll.se ; gallery https://www.styrelseproffset.se/hemsidesgalleri (~70 sites) | /hemsida |

Conclusion: assume everything is entered by hand in the web UI. A scripted route would be browser automation of that UI, which needs a logged-in session (user decision) and has not been tested.

## 2. Content mapping

Export: 77 pages (52 public, 25 members), 50 assets (36 PDF, 13 images), 3 filarkiv PDFs.

| Page group (files) | Count | Target on Styrelseproffset | Visibility | Effort |
|---|---|---|---|---|
| nyheter__* (news) | 36 (14 public, 22 members) | News module ("Nyheter"), one item each. Only 5 have real dates (536-540). | Public 14 as normal news; 22 member news: PROBLEM, "Las nyheter" is site-wide only. | Manual, ~36 items |
| foreningen.md, foreningen__brf-hojden, att-bo-i-bostadsratt, garantibevis, styrelse*, valberedning*, foreningsstamma | 7 | Normal pages under menu "Foreningen". Styrelse could use the dynamic "board composition" module instead of static text (UNVERIFIED how it is filled). | Public | Manual copy; stamma page is 8.7 kB |
| foreningen__arsredovisningar | 1 | Page with "files" module (folder of PDFs) | Members (page protection: member login) | Manual + upload PDFs |
| mitt-boende__* (21 pages: andrahandsuthyrning, badrum, ..., tvatt, ventilation, stadgar) | 21 | Pages under menu "Mitt boende" (Q&A and step-by-step modules fit). Stadgar: page + PDF. | Public (all 21 flagged public in the export) | Manual; best candidate for HTML/rich-text paste |
| mitt-boende__serviceanmalan + kontakt__serviceanmalan | 2 | One page; consider site contact-form module or the member app "felanmalan" instead | Public | Manual, decide on duplicates |
| kontakt__for-maklare, manadsavgift-avier | 2 | Normal pages under "Kontakt" | Public | Manual |
| kontakt__kontaktperson | 1 | Page, member-login protected (personal_data) | Members | Manual |
| sidor__skickameddelande | 1 | Replace with contact-form module | Public | Rebuild |
| sidor__nyhetsbrev | 1 | Joomla newsletter signup: no direct equivalent; members subscribe to news via e-mail/push in the portal/app. Replace with explanation or drop | Public | Decide |
| sekretesspolicy | 1 | Normal page (11 kB), linked from footer | Public | Manual; review text for platform change (processor now Webb Trepunktnoll AB) |
| index.md | 1 | Front page: either "latest news" or a chosen page | Public | Manual |
| filarkivet.md + filarkivet/ (3 PDFs) | 1+3 | File archive folder; show via files module on a members-protected page. Do NOT upload the Dropbox PDF; others after review. | Members | Manual upload |
| component__tags__tag__{bank,bolan,lan} | 3 | Joomla-only tag listings: no equivalent. Fold into the existing "Gront bolan" page or drop. | Public | Drop/merge |
| assets/ (50) | 50 | Upload to page folders / file archive; images inserted in editor | n/a | Multi-upload possible, linking is manual |
| Old URLs | all | Site redirects (Ompekningar) one by one for important URLs; otherwise a fresh sitemap | n/a | See cutover |

Special cases:
- Undated news (31 of 36): either keep ordering by publishing them with synthetic, clearly arbitrary dates (e.g. descending by the NNN number) or ask the user for approximate months. Do not invent precise dates. Article numbers (515-540) give order only. UNVERIFIED that the platform shows or orders by the date field only.
- Member news (22): options (a) turn them into protected pages under "Arkiv for medlemmar" (list page + one page each or one long page with Q&A modules), (b) enable "Las nyheter" and put ALL news behind login (conflicts with the decision that some news is public), (c) publish only the 14 public as news and the 22 as one protected page. Option (c) is the least effort and closest to the decision.
- Personal data pages (styrelse, valberedning, kontaktperson, several news) flagged personal_data: re-check wording before publishing; the chairman's phone may stay public.
- Joomla-only: tags, send-message component, newsletter component.

## 3. Recommended method

Manual entry in the web UI from prepared snippets, with optional UI automation later.

- Prepare per page a clean rich-text HTML snippet (convert md -> HTML, simple tags only: h2/h3, p, ul/ol, a, strong; no inline styles) plus a manifest (title, slug, menu parent, visibility, attached files, publish date). The editor is WYSIWYG so pasting rendered HTML from a browser or using the "HTML" module is the fastest path (HTML module is on-domain only for scripts, plain HTML is fine; but prefer text modules so the member app renders them).
- Browser automation (Claude in Chrome / Playwright) of the page and news forms is feasible in principle but: needs the user's logged-in session, forms use drag-and-drop module lists, risk of duplicated or mis-saved items, and it is unverified. Use only after the hand-test shows the form is stable, and only for the 36 news items.
- No API: do not plan on scraping internal endpoints.
- Alternative for news: the AI assistant can create news from instructions; helpful but each needs approval, not a bulk route.

Risks: member news restriction mismatch; no import so ~60 manual items; undated news ordering; push/e-mail notifications firing to subscribers when old news is published (use "Blockera notis" / draft + set dates; check that old items do not send notifications); member register must be loaded and e-mails correct before login works; BankID costs; free year ends after 12 months (price afterwards unknown for the exact tier: 250/500/750 depending on apartments); domain/DNS fully handled by support (dependency and lead time); Joomla hosting at Simply BRF may be tied to the domain/contract.

## 4. Step order

0. Decide open questions below. Create account (user) and start the free trial; keep the site noindex while building.
1. Settings: site address under brftorget.se (choose carefully, do not change later), graphic profile, header, footer, enable member login (without BankID at first), noindex on.
2. Load the member register (Excel import exists) with e-mail addresses; this is a user task and personal-data sensitive.
3. Test pass: create 1 public page (e.g. mitt-boende__tvatt) and 1 public news item; check mobile view, slug, menu, preview link. Create 1 protected page (arsredovisningar with 1 PDF) and test the login with a board member's account in a private window; verify that a non-member sees nothing. Check whether news notifications fire.
4. Fix the conventions found (heading levels, image size, link style) and update the snippets.
5. Bulk build: menu structure -> public pages (foreningen, mitt-boende, kontakt) -> protected pages and files -> news (oldest first so newest ends on top; verify date handling) -> front page.
6. Review: link check (all assets/ links replaced), personal data check, Swedish proofreading, board sign-off. Walk through with 2-3 residents.
7. Order own domain via support (ask: apex+www, certificate, mail forwarding, timing, TTL, ability to switch back). Lower DNS TTL at the current registrar/Simply BRF a few days before.
8. Cutover: support points brfhojdengbg.se; select it as primary address; enable permanent redirect from brftorget.se; remove noindex; add Ompekningar for top old URLs (stamma, styrelse, tvatt, parkering etc.); inform residents (notice board, e-mail, one news item).
9. Rollback: keep Joomla site untouched and paid until the new site has run ~2-4 weeks; rollback = point DNS back to Simply BRF's records (note them down first, including MX/mail records) and turn noindex on again. Do not cancel the old subscription or delete the Joomla site before then. Take a final export/backup of the old site.
10. After: cancel old hosting only if mailboxes do not depend on it; set a calendar reminder for the end of the free period.

## 5. Open questions (most blocking first)

1. May the user create the Styrelseproffset account/free trial (or already has one)? Everything else depends on a logged-in session. Also: should an automation tool ever drive that session, or does the user prefer manual entry with prepared snippets?
2. Where does the domain brfhojdengbg.se live (registrar, who holds it, does Simply BRF control DNS/mail)? Is any e-mail on that domain used? Needed to know if the domain can move at all.
3. Member news (22 items): option (a), (b) or (c) from section 2? Do the member-only news need to stay at all?
4. Is the member register (names, e-mail, apartment) complete and may it be loaded into Styrelseproffset (GDPR/DPA signed by the association)? Without it nobody can log in.
5. Is the exact number of apartments known (price tier 250/500/750 kr/month after the free year) and does the board accept the cost?
6. Undated news: approximate dates available, or accept synthetic ordering (and should old news send notifications - assume no)?
7. Should BankID login be enabled (extra per-login cost) or e-mail/password only?
8. Pages without equivalent (newsletter signup, tag pages, send-message): drop/replace as proposed?
9. Which Joomla URLs matter (e.g. QR codes, printed notices, links in e-mails) and need redirects?
10. Questions for Styrelseproffset support (contact form on /kontakt): any bulk import or API for pages/news; whether the news date can be backdated; whether ordinary pages can be listed in a "news archive" style; www/apex/MX handling on own domain; per-news member restriction; price after the free year.

## Decision log (user)
- 2026-10-25: ALL news becomes members-only. Use the platform's site-wide news lock (unverified setting name: "Lås nyheter"); no per-item workaround needed. Public visitors see no news. Standing rules from previously public news (parking, andrahand, bredband) live on the normal pages instead.

## Portal probe (read-only, logged in as admin, 2026-10-25)
Verified in the live portal (GET requests only, nothing saved):
- Site exists, fresh: address slug `brfhojdenigoteborg` on the brftorget.se address; no own domain; 0 news, 0 members, 0 subscribers, 0 files (100 GB quota). Menu has 5 starter entries (Information A-Ö, Kontakta oss, Om föreningen, Stadgar och årsmöten, Styrelse).
- Settings currently: member login OFF (`has_login`), BankID OFF, news lock OFF (`has_locked_siteupdates`, label not shown in HTML; matches the "Lås nyheter" setting, confirm in UI), noindex OFF (`is_noindex`), cookie consent OFF, site lock OFF (`is_locked`).
- News form (/portal/sites/update/edit.php): title, body, author, published-from date+time (backdating possible), published-to, draft/published, slug, `suppress_notification` checkbox, links. Per-post restriction: none.
- Page form (/portal/sites/page/create.php): title + modules: Överskrift, Text (formatting, images, raw HTML), Bild, Filer från filarkivet, Metainformation, Kontaktformulär, Kalender. Per-page protection setting not on the create form (probably in the edit step: unverified).
- A–Ö (glossary-style info items, shown by an "A-Ö-information" module) could hold short resident topics (e.g. Bredband, Nyckelbeställning).
- Members: Excel/CSV import exists (/portal/members/import.php; columns incl. e-mail, phone, member type, objektsnummer, ownership share; template download; column mapping step). Residence register + bulk link tool also exist.
- Export centre exists (news, pages, members, files …) -> usable as backup of the new site; no import for news/pages found.
- Files: upload + browse + Dropbox sync option; "Filer från filarkivet" module for downloads on pages.

## Hands-on test (2026-10-25, via user's logged-in Chrome) — RESULTS
Settings changed and verified server-side: member login ON, noindex ON, news lock ("Lås nyheter", has_locked_siteupdates) ON. Left OFF: BankID, cookie consent, "Deaktivera hemsida" (is_locked = deactivate the whole site, NOT a news setting; never tick it).
Test content created (all titled "TEST ... (kan raderas)"; delete before launch via page/news "Alternativ" menu -> trash):
- Page id 21522 /sidor/test-publik-sida-kan-raderas — published, access "Inget": anonymous sees heading, paragraph, list, working mailto link; page carries robots noindex.
- Page id 21523 /sidor/test-skyddad-sida-kan-raderas — published, access_type=3 (Medlemsinloggning): anonymous sees "Denna sida är skyddad" + login form, no text leaked.
- News id 8998 — backdated 2025-06-30 13:46, suppress_notification ticked: shown as "30 jun 2025" on home/news list; after news lock anonymous sees "Hittade inga nyheter." (homepage news block also hidden).
Technique that works (rich text = TipTap/ProseMirror, hidden textarea syncs): in the page, `document.querySelector('.ProseMirror').editor.commands.setContent(html, true)`; plain inputs by assigning value + dispatching input/change. form_input fails on the editor div. Page form fields: title, slug, published_from_date/time, state (1=Utkast, 2=Publicerad), access_type (1 Inget, 2 Lösenord, 3 Medlemsinloggning), access_password, menu_add (select incl. Huvudmenyn + submenus). Create page = /portal/sites/page/create.php (title + module ticks; "Överskrift" and "Text" pre-ticked), then edit.php?id=N. News form: title, body (editor), author_id (0 = "Styrelsen"; default picked Shwan, set 0), published_from_*, state (default = Publicerad! careful), slug (auto), suppress_notification, links.
Gotchas: site settings page is tabbed on wide windows — the Spara of a hidden tab does nothing; open the tab first. Page default state is Utkast; news default is Publicerad. Output containing URL/query-like strings can be blocked by the browser tool: return short status strings.
Open: per-page access works; menu placement and A-Ö not yet tested; file archive upload + "Filer från filarkivet" module not yet tested; member import not tested (needs real data + DPA).
