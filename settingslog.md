# Settings log: Brf Höjden on Styrelseproffset

All times 2026-10-25. Portal: Hemsida > Inställningar unless noted. "Who" = changes made by Claude on the chairman's instruction.

| # | Setting | Before | After | Why |
|---|---|---|---|---|
| 1 | Medlemmar ska kunna logga in på hemsidan (`has_login`) | off | **on** | Required for members-only pages and news |
| 2 | Be sökmotorer att inte indexera hemsidan (`is_noindex`) | off | **on** | Keep the half-built site out of Google until launch; **switch off at launch** |
| 3 | Lås nyheter (`has_locked_siteupdates`) | off | **on** | Chairman's decision: all news private |
| 4 | Startsida (`index_type` / `index_page`) | news feed (`updates` / none) | **page** / Välkommen (id 21525) | News is locked, so a news front page would be empty for visitors |
| 5 | Beskrivning (`description`) | empty | "Brf Höjden i Göteborg: information för medlemmar och boende i Ekebäckshöjd." | Search/preview text |
| 6 | Hemsidans meny (Menyer) | 5 starter items | 6 top-level items + 33 children (see build-tracking.md); 'Bilagor till nyheter' removed from the menu later the same day | New structure |
| 7 | Starter pages 21511-21515 | published | **draft** | Replaced by new pages; kept, not deleted |
| 8 | Fil-uppladdningar | 0 files | 50 files in folder *Hemsidan* (via API, then deleted my temporary `build.json`) | Page attachments |
| 9 | Sidhuvudsbild (Sidhuvud, `photo_upload`) | platform default illustration | Stena Fastigheter press photo of the Sjupundsgatan bus stop with the Höjden building (`brf-hojden-sjupundsgatan.jpg`, from the chairman's Downloads) | Chairman chose this photo during review. Source file is a Stena Fastigheter press image: check its usage terms/credit |
| 10 | Sidhuvudsbild (Sidhuvud, `photo_upload`), second change | bus-stop press photo (#9) | `ekebackshojd-hus-d.png` from the chairman's Downloads, converted to a 1150×384 JPEG (2.6 MB 16-bit PNG -> 137 KB) | Chairman's choice. It is a rendering (3D visualisation with people); check who owns it / usage terms, like #9 |

## Not changed (deliberately)
- BankID login (costs money), cookie consent popup, "Deaktivera hemsida" (turns the whole site off), own domain, footer text, bookings/agreements options, member register, subscribers (0), e-mail settings.
- **News notifications:** every news post was created with "suppress notification" ticked; the site has 0 subscribers.

## Test artifacts (removed)
- Test pages 21522, 21523, 21524 and test news 8998 were created while testing and moved to the portal trash.
- Stray test files in the archive root from failed upload attempts were deleted.

## Access
- An API key (`SP_API_KEY` in `.env`) was created by the chairman and used **only** for file upload/listing/deletion of my own test files. Revoke it when the build is finished (Inställningar > API-nycklar).
- Portal login is rate-limited: repeated scripted logins locked it for a while. Page/news/menu work was done through the chairman's already-logged-in Chrome session.
