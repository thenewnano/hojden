import json
b = json.load(open("build.json"))
ids = {"start":21525,"om":21526,"styrelse":21527,"stamma":21528,"stadgar":21529,"ekonomi":21530,"grontbolan":21531,"bostadsratt":21532,"nyinflyttad":21533,"regler":21534,"parkering":21535,"tvatt":21536,"pool":21537,"cykel":21538,"balkong":21539,"las":21540,"bredband":21541,"andra":21542,"sopor":21543,"skotsel":21544,"badrum":21545,"kok":21546,"fonster":21547,"golv":21548,"vaggar":21549,"elektricitet":21550,"ventilation":21551,"brandskydd":21552,"felanmalan":21553,"kontakt":21554,"avgift":21555,"maklare":21556,"medlemskontakter":21557,"bilagor":21558}
nids = {504:8999,505:9000,506:9001,507:9002,508:9003,509:9004,510:9005,511:9006,512:9007,513:9008,514:9009,515:9010,516:9011,517:9012,518:9013,519:9014,520:9015,521:9016,522:9017,523:9018,524:9019,525:9020,526:9021,527:9022,528:9023,529:9024,530:9025,531:9026,532:9027,533:9028,535:9029,536:9030,537:9031,538:9032,539:9033,540:9034}
json.dump({"pages": ids, "news": nids}, open("build-ids.json", "w"), indent=1)

L = ["# Page and news tracking: Brf Höjden on Styrelseproffset", "",
     "Site: https://www.brftorget.se/brfhojdenigoteborg/ (portal slug `brfhojdenigoteborg`). Built 2026-10-25. Site is **noindex** while under review.", "",
     "Regenerate with `make_docs.py`; content source of truth is `site_pages.py` (pages) and `make_build.py` (menu, news).", "",
     "## Pages (34)", "", "| Menu section | Page | Portal id | URL slug | Access | Attached files | Notes |", "|---|---|---|---|---|---|---|"]
for p in b["pages"]:
    L.append(f"| {p['section'] or 'Front page'} | {p['title']} | {ids[p['key']]} | `{p['slug']}` | {'**members**' if p['access']==3 else 'public'} | {len(p['docs'])} | {p['note']} |")
L += ["", "## News archive (36 posts, all members-only through the site-wide news lock)", "",
      "`approx` = the old site never showed a date for this post; the date is an **estimate** from the post's content and its position in the sequence. Real dates (RSS/homepage) are marked exact.", "",
      "| Old post | Portal id | Title | Date | Date quality |", "|---|---|---|---|---|"]
for n in b["news"]:
    L.append(f"| {n['nid']} | {nids[n['nid']]} | {n['title']} | {n['date']} {n['time']} | {'approx' if n['approx'] else 'exact'} |")
L += ["", "## Major decisions", "",
 "1. **All news private.** Per the chairman: the site-wide 'Lås nyheter' setting is on, so visitors see no news; only logged-in members do. The 14 posts that were public on the old site are now private too.",
 "2. **Structure redesigned for members** (old Joomla menu replaced): Hem | Föreningen | Bo i huset | Skötsel och underhåll | Felanmälan och kontakt | Nyheter. 34 pages in 4 groups instead of ~45 pages in a flat 'Mitt boende' list.",
 "3. **Merged pages:** Serviceanmälan (2 copies) + Garantibevis + lift rule -> *Felanmälan*; Brandskydd + Brandvarnare -> *Brandskydd och brandvarnare*; Materialval -> *Väggar och tak*; Stadgar page + Stadgar.pdf -> *Stadgar*; uteplats -> *Balkong och uteplats* + *Cykelrum och förråd*; Bil/cykelpool kept as one.",
 "4. **New pages written from existing facts only:** *Ny i huset: checklista*, *Ordningsregler* (quiet/drilling hours, balcony, köksfläkt, renovation law, from news 509/514), *Skötsel och underhåll* (overview), *Medlemskontakter* (members-only directory), *Bilagor till nyheter* (members-only), *Välkommen* (front page).",
 "5. **Standing rules lifted out of news:** visitor-parking rules (news 507) -> Parkering; Stena/ARC split and Otis lift cost rule (news 516/530) -> Felanmälan.",
 "6. **Personal data:** chairman's phone is public (Styrelse, Kontakta styrelsen, front page). Valberedning's Gmail, the ARC manager's direct number and Stena jour numbers are only on the members-only *Medlemskontakter* page. Salesperson contact at Balkongrutan appears only in members-only news.",
 "7. **Dropped:** news 454 and 495 (website-vendor boilerplate); the Dropbox PDF (contained a password); Joomla form/tag pages; empty/placeholder pages (Vanliga frågor, Nyinflyttad, bokahiss-utloggad); other association's link in Brandskydd.",
 "8. **Internal links use `internal://sitepage-ID/`**, which the platform resolves; they survive a domain change. Only the menu item 'Nyheter' and one link in the news body use an absolute URL and must be updated if the domain changes.",
 "9. **Files:** 50 documents/images uploaded via the API to the archive folder *Hemsidan* (subfolders Föreningen, Boende, Skötsel, Nyhetsbilagor, Bilder) and attached to pages with the 'Filer' module. Inline images in old news posts were not carried over; they are on *Bilagor till nyheter*.",
 "10. **Starter pages** (Om föreningen, Styrelse, Stadgar och årsmöten, Information A-Ö, Kontakta oss; ids 21511-21515) were set to *draft* and removed from the menu, not deleted. They contain a map and an automatic board-member module you may want to reuse.",
 "", "## Open items for the review", "",
 "- **Member register is empty**, so nobody can log in yet; the members-only pages and news could not be viewed as a member. Load the register (needs the data processing agreement), then test with a real member account.",
 "- **28 news dates are estimates** (list above). Replace with real dates if you know them.",
 "- **Missing document:** stämmoprotokoll 2025 (chairman has requested it). Årsredovisning 2024 and 2025 are published on Ekonomi (members-only).",
 "- **Hero image** was replaced with the chairman's Stena press photo; check Stena's usage terms.",
 "- **Fact questions resolved in review (2026-10-25):** warranty process rewritten (ARC for common areas/BRF issues, member pays inside the apartment, warranty -> Stena with Skanska); no. 31 bike room permanent and no. 43 = upper-garage room; barnvagnsrum overflow kept; storage hours 08-20 no longer apply (not added); bofaktablad mention removed; cykelpool uses GoRide, address removed.",
 "- **Dead link** `Alla bofaktablad.pdf` (404 on old site) is not migrated; the mention on Cykelrum och förråd was removed in review.",
 "- **Resolved in review (2026-10-25):** parking flow rewritten with the chairman's facts (36 spaces: 27 regular at 1 061 kr/month + 9 charging, all rented; ARC assigns, ePARK activates; 3 months notice; buyer may take over; external ePARK rental incl. VAT). Price of charging spaces is not on the page.",
 "- **Bostadsrätterna brochures:** summarised in own words on *Att bo i bostadsrätt* (and a few facts on *Föreningsstämma*) with credit; the two PDFs (SV Dec 2023, EN Feb 2025) are **linked at the source, not hosted**, because they are copyrighted and we don't know if Brf Höjden is a Bostadsrätterna member. Upload copies only after checking their terms.",
 "- **Domain:** not changed. brfhojdengbg.se still points to the old Joomla site.",
 "- **News bodies** may still hold old links to the Joomla site; checked and rewritten to the new site root.",

 "- **Bilagor till nyheter** is no longer in the menu (chairman, 2026-10-25). It stays as a members-only page, reached from the news posts that need it: 519 and 521 link to it; 537 links to it for the cykelrum photos; 518 and 522 now link to the pages that hold their files (Brandskydd och brandvarnare, Bil- och cykelpool).",
 "- Menu shows members-only pages to visitors (they see the login prompt on click). Hide them from the menu if preferred."]
open("build-tracking.md", "w").write("\n".join(L) + "\n")
print(len(L), "lines")
