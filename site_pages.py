"""Site specification for Brf Höjden on Styrelseproffset.

PAGES is the single source of truth for what gets built: key, title, menu
section, access (1 = public, 3 = member login), HTML body, attached documents.
Text comes from export_private/pages (converted) or is composed here from facts
that already exist in the export. Nothing here is invented.
"""
import re
import markdown

SRC = "export_private/pages/"
PUBLIC, MEMBERS = 1, 3


def md(name, cut_from=None, drop_h1=True, drop_re=()):
    """Convert an exported page to clean HTML (front matter, doc tables, asset links removed)."""
    t = open(f"{SRC}{name}.md").read()
    t = re.sub(r"\A---\n.*?\n---\n", "", t, flags=re.S)
    if drop_h1:
        t = re.sub(r"\A\s*# .*\n", "", t)
    if cut_from:  # drop everything from this heading on (the old 'Dokument' tables)
        t = re.split(cut_from, t, maxsplit=1)[0]
    t = re.sub(r"^\s*#{1,4} *Dokument *\n.*\Z", "", t, flags=re.S | re.M)
    t = re.sub(r"\[([^\]]*)\]\(assets/[^)]*\)", lambda m: m.group(1), t)       # doc links -> plain text
    t = re.sub(r"^\|.*\|\s*$\n?", "", t, flags=re.M)                              # leftover tables
    t = re.sub(r"\xa0", " ", t)
    for pat in drop_re:
        t = re.sub(pat, "", t, flags=re.M)
    t = re.sub(r"\n{3,}", "\n\n", t).strip()
    html = markdown.markdown(t, extensions=["extra", "sane_lists", "nl2br"])
    return re.sub(r"<h1>", "<h2>", html).replace("</h1>", "</h2>")


def a(href, text):
    return f'<a href="{href}">{text}</a>'


EMAIL = a("mailto:styrelsen@brfhojdengbg.se", "styrelsen@brfhojdengbg.se")
ARC_MAIL = a("mailto:bostadsratt@arcfast.se", "bostadsratt@arcfast.se")
ELON_MAIL = a("mailto:felanmalan@elcomfortgruppen.se", "felanmalan@elcomfortgruppen.se")
ARC = a("https://arcfast.se/", "arcfast.se")

# --- section order for the menu -------------------------------------------------
SECTIONS = ["Föreningen", "Bo i huset", "Skötsel och underhåll", "Felanmälan och kontakt"]

PAGES = []


def page(key, title, section, html, access=PUBLIC, docs=(), note="", reuse=None):
    PAGES.append(dict(key=key, title=title, section=section, html=html, access=access, docs=list(docs), note=note, reuse=reuse))


# ================= FÖRENINGEN =====================================================
page("om", "Om Brf Höjden", "Föreningen", md("foreningen__brf-hojden", cut_from=r"#{1,4} *Dokument"),
     docs=["broschyr_hojden.pdf"], note="Text from foreningen/brf-eken; brochure attached")

page("styrelse", "Styrelse och valberedning", "Föreningen",
     f"""<h2>Så når du styrelsen</h2>
<p>E-post för alla ärenden som inte är akuta: <strong>{EMAIL}</strong></p>
<p>Vid akuta fall, ring ordföranden på <strong>072-970 71 42</strong>.</p>
<p>Fel i huset anmäler du till förvaltaren, se {a("/felanmalan", "Felanmälan")}.</p>
<h2>Styrelsen</h2>
<ul><li>Ordförande: Shwan Ciyako</li><li>Ledamot: Joakim Nordström</li><li>Ledamot: Rikard Bergqvist</li><li>Ledamot: Jarne Postma</li><li>Ledamot: Johan Skoog</li></ul>
<h2>Valberedningen</h2>
<p>Valberedningen presenterar på föreningsstämman de personer som är intresserade av att sitta i styrelsen. Den är oberoende av styrelsen: styrelsen får inte påverka valberedningens val och presentation av kandidater. Genom en aktiv dialog med styrelsen och medlemmarna vill valberedningen bidra till ökad gemenskap och engagemang i föreningen.</p>
<p>Valberedningen består av Petter Thomée. Medlemmar hittar kontaktuppgifter under {a("/medlemskontakter", "Medlemskontakter")} (kräver inloggning).</p>
<h2>Vad gör styrelsen?</h2>
<p>Styrelsen företräder bostadsrättsföreningens medlemmar och arbetar för medlemmarnas och föreningens bästa. Föreningsstämman utser styrelsen, som får i uppdrag att leda föreningens arbete och ansvara för förvaltningen. Förvaltningen omfattar både små och stora arbetsuppgifter som administration och teknisk förvaltning, som ofta läggs ut på entreprenad.</p>
<h2>Vad går månadsavgiften till?</h2>
<p>I en bostadsrättsförening ansvarar man gemensamt för fastigheternas drift och skötsel. Styrelsen bestämmer hur hög månadsavgiften ska vara. Avgiften ska täcka föreningens kostnader och avsättning till yttre underhåll, och blir aldrig högre än vad som långsiktigt behövs. Läs mer under {a("/manadsavgift-och-avier", "Månadsavgift och avier")}.</p>""", note="Board names, public chairman phone, valberedning (no personal email: see Medlemskontakter)")

page("stamma", "Föreningsstämma", "Föreningen", md("foreningen__foreningsstamma") + """<h2>Bra att veta</h2>
<ul>
<li>Protokollet från stämman ska vara justerat och tillgängligt för medlemmarna senast tre veckor efter stämman.</li>
<li>Stämmoprotokollet är det enda protokoll som medlemmarna har rätt att ta del av. Revisorerna granskar styrelsens protokoll åt medlemmarna.</li>
<li>Medlemmar som inte kan komma får lämna fullmakt, men inte till någon helt utomstående. Kontrollera i stadgarna vem som får vara ombud.</li>
<li>Ansvarsfrihet för styrelsen beviljas med enkel majoritet.</li>
</ul>
<p>Källa: Bostadsrätternas broschyr Att bo i bostadsrätt.</p>""",
     note="Generic explainer text from old site, kept as is")

page("stadgar", "Stadgar", "Föreningen",
     """<p>Stadgarna är föreningens gemensamma regler. Som medlem har du genom ett juridiskt kontrakt förbundit dig att följa dem, så det är viktigt att läsa igenom dem noggrant när du flyttar in. Bryter man mot stadgarna kan man i värsta fall förlora sin lägenhet, bli skadeståndsskyldig eller åtalad.</p>
<h2>Ändring av stadgar</h2>
<p>Stadgar kan bara ändras genom att medlemmarna röstar på föreningsstämma. Det krävs två stämmor för att få igenom en ändring. Medlemmar kan via motion föreslå ändringar, men bör sakligt kunna argumentera för förändringen. Svensk lag står över stadgarna, så ändringar måste vara förenliga med lagen. Kontakta gärna styrelsen om du har ett förslag.</p>""",
     docs=["Stadgar.pdf"], note="Stadgar.pdf attached")

page("ekonomi", "Ekonomi och årsredovisningar", "Föreningen",
     """<p>I årsredovisningen kan du läsa mer om föreningens ekonomi, till exempel intäkter, utgifter och belåning. Den inledande förvaltningsberättelsen beskriver de åtgärder som gjorts eller som planeras framöver.</p>
<p>Den ekonomiska planen är godkänd av Boverket godkända intygsgivare och registrerad hos Bolagsverket. Den är en budget och prognos för föreningens första verksamhetsår.</p>
<p>Här finns också protokollen från de ordinarie föreningsstämmorna.</p>
<h2>Underhållsplan</h2>
<p>Styrelsen planerar föreningens underhåll långsiktigt. För nyproducerade föreningar som Brf Höjden är en underhållsplan som sträcker sig över 50 år obligatorisk. Planen är styrelsens verktyg för att veta vilka reparationer och vilket underhåll fastigheten behöver framöver och hur det ska finansieras, och den är inte automatiskt tillgänglig för alla medlemmar. Frågor om underhållet besvaras av styrelsen.</p>""",
     access=MEMBERS, docs=["EkonomiskPlan.pdf", "Årsredovisning inkl revisionsberättelse 2022 (sign).pdf", "Årsredovisning inkl revisionsberättelse 2023.pdf",
                           "Årsredovisning inkl revisionsberättelse 2024 (sign).pdf", "Årsredovisning inkl revisionsberättelse 2025 (sign).pdf",
                           "Protokoll ordinarie föreningsstämma 230615 (sign).pdf", "Protokoll ordinarie föreningsstämma 240617 (sign).pdf"],
     note="Members only as on old site. 2024 and 2025 reports added 2026-10-25 (2025 file is an image-only PDF incl. the e-signature log with board members' private e-mails and IPs: chairman chose to publish as is, members-only). Stämma 2025 protocol still missing. Underhållsplan paragraph added 2026-10-25 (general rule from Bostadsrätterna brochure; no claims about Höjden's own plan)")

page("grontbolan", "Grönt bolån", "Föreningen",
     """<p>För att få grönt bolån behöver du dela föreningens certifikat med din bank. Certifikatet finns som bilaga nedan.</p>""",
     docs=["Ekebäckshöjd kv Öst - Hus C_MB2021-0007_20211207.pdf"], note="Green mortgage certificate")

BR_SV = "https://www.bostadsratterna.se/media/oswefzu0/att-bo-i-bostadsr%C3%A4tt-2023.pdf"
BR_EN = "https://www.bostadsratterna.se/media/iqzcj2j3/living-in-co-op-housing-2025.pdf"
BOSTADSRATT_EXTRA = f"""<h2>Bra att veta när du bor i bostadsrätt</h2>
<p>Det här är allmän information om hur bostadsrätt fungerar enligt lagen. Läs också föreningens {a("stadgar", "stadgar")}, som beskriver hur reglerna gäller just i Brf Höjden.</p>
<h3>Äger jag min lägenhet?</h3>
<p>Juridiskt är det föreningen, alltså alla medlemmar tillsammans, som äger huset och marken. Du är medlem och delägare i föreningen och har nyttjanderätt till din lägenhet. Inom stadgarnas ramar får du ändra i lägenheten, hyra ut den och belåna den, och du får sälja den fritt till marknadspris. Följer du inte stadgarna kan du i yttersta fall sägas upp från lägenheten.</p>
<h3>Vem ansvarar för reparationer?</h3>
<p>Du ansvarar för reparationer och underhåll av det som finns inne i din lägenhet. Föreningen ansvarar för det gemensamma, till exempel rörstammar, trapphus, källare, vind, fasader och yttertak. En enkel tumregel är att du ansvarar för det du ser: ytskikt, inredning och vitvaror. Rör och elledningar inne i väggar eller under golv är inte ditt ansvar. Exakt var gränsen går, till exempel för fönster, dörrar och element, står i stadgarna. Se också {a("felanmalan", "Felanmälan")} och {a("skotsel-och-underhall", "Skötsel och underhåll")}.</p>
<h3>Får jag ändra i lägenheten?</h3>
<p>Inne i lägenheten har du stor frihet, men vissa ändringar kräver styrelsens tillstånd. Det gäller till exempel ingrepp i bärande konstruktioner, ändrade ledningar för vatten, avlopp, värme eller gas, ändringar i ventilationen och eldstäder. Du kan alltså inte flytta kök eller badrum, ta upp en dörr i en bärande vägg eller ta bort ett element utan att fråga först. Du får aldrig ändra sådant som föreningen ansvarar för, till exempel att borra i fasaden. Kontakta alltid styrelsen innan du renoverar. Styrelsen får bara säga nej om åtgärden är till påtaglig skada eller olägenhet för föreningen, och kan ställa villkor. Är du missnöjd kan du begära prövning hos hyresnämnden. Gör du ändringar utan tillstånd kan du i värsta fall förlora bostadsrätten. Se också {a("ordningsregler", "Ordningsregler")}.</p>
<h3>Försäkring</h3>
<p>Föreningen har en fastighetsförsäkring som gäller skador på huset, till exempel vattenledningsskador, brand och inbrott. Den täcker inte din egendom eller det du själv ansvarar för inne i lägenheten. Du behöver därför en hemförsäkring, gärna med bostadsrättstillägg. Många föreningar har ett gemensamt tillägg, så fråga styrelsen hur det fungerar hos oss.</p>
<h3>Störningar</h3>
<p>Vi får alla acceptera vardagliga ljud, som att grannen ibland har fest eller att barn leker. Blir en störning ohållbar är första steget att prata med grannen. Hjälper inte det kan styrelsen ta ärendet vidare. Då behöver störningarna dokumenteras, till exempel i ett störningsschema. Fortsätter störningarna efter en varning kan bostadsrätten i yttersta fall sägas upp.</p>
<h3>Hyra ut i andra hand</h3>
<p>Det kräver styrelsens tillstånd. Giltiga skäl är bland annat studier eller arbete på annan ort, provboende med sambo och uthyrning till närstående. Säger styrelsen nej kan du vända dig till hyresnämnden. Du är fortfarande skyldig att betala avgiften och ansvarar för att hyresgästen sköter sig. Hyr du ut längre än två år kan du behöva avtala bort besittningsskyddet, se hyresnamnden.se. Att ha en inneboende är tillåtet utan tillstånd så länge det inte skapar problem för föreningen. Läs mer under {a("andrahandsuthyrning", "Andrahandsuthyrning")}.</p>
<h3>Köpa och sälja</h3>
<p>Köp och försäljning ska ske skriftligt, med pris, lägenhet och båda parters underskrift. Säljaren lämnar en kopia av avtalet till styrelsen när köparen ansöker om medlemskap. Köparen får inte flytta in förrän medlemskapet är godkänt, och beviljas inte medlemskap är köpet ogiltigt. Styrelsen får neka ett företag som medlem för en permanentbostad. Vinst vid försäljning är skattepliktig, och Skatteverket har information om reglerna. Mäklare kan kontakta oss enligt {a("for-maklare", "För mäklare")}.</p>
<h3>Så läser du årsredovisningen</h3>
<p>En årsredovisning består av förvaltningsberättelse, resultaträkning, balansräkning, kassaflödesanalys och noter. Från och med 2024 ska den också innehålla nyckeltal: årsavgift per kvadratmeter, skuldsättning per kvadratmeter, sparande per kvadratmeter, räntekänslighet och energikostnad per kvadratmeter. Ett negativt resultat betyder inte automatiskt att ekonomin är dålig, eftersom stora avskrivningar eller underhåll kan ligga bakom. Det viktigaste är att föreningen kan betala sina räkningar. Föreningens rapporter finns under {a("ekonomi", "Ekonomi och årsredovisningar")} (kräver inloggning).</p>
<h2>Mer att läsa</h2>
<p>Sammanfattningen ovan bygger på Bostadsrätternas broschyr. Läs den i sin helhet hos källan:</p>
<ul>
<li>{a(BR_SV, "Att bo i bostadsrätt (Bostadsrätterna, PDF, december 2023)")}</li>
<li>{a(BR_EN, "Living in co-op housing (Bostadsrätterna, PDF in English, February 2025)")}</li>
</ul>"""
page("bostadsratt", "Att bo i bostadsrätt", "Föreningen", md("foreningen__att-bo-i-bostadsratt") + BOSTADSRATT_EXTRA,
     note="Old generic text + NEW own-words sections from Bostadsrätterna's brochure (added 2026-10-25); links to the SV 2023 and EN 2025 PDFs at the source, NOT hosted copies (copyright). Check: the brochure's own date is Dec 2023")

# ================= BO I HUSET =====================================================
page("nyinflyttad", "Ny i huset: checklista", "Bo i huset",
     f"""<p>Välkommen hem! Här är det som de flesta behöver ordna eller känna till under de första veckorna. Varje punkt har en egen sida med mer information.</p>
<h2>Att ordna själv</h2>
<ul>
<li><strong>Bredband och TV:</strong> ringa Tele2 och be om aktivering av föreningens gemensamma avtal. Det gäller varje ny medlem. Se {a("/bredband-tv-och-telefoni", "Bredband, TV och telefoni")}.</li>
<li><strong>Hemförsäkring och el:</strong> du tecknar eget avtal. Se {a("/manadsavgift-och-avier", "Månadsavgift och avier")} och {a("/elektricitet", "Elektricitet")}.</li>
<li><strong>Parkering:</strong> ställ dig i kö via förvaltaren. Se {a("/parkering", "Parkering")}.</li>
<li><strong>Bil- och cykelpool:</strong> {a("/bil-och-cykelpool", "gå med gratis")}.</li>
</ul>
<h2>Att känna till</h2>
<ul>
<li><strong>Tvätt:</strong> tvättstugan bokas på skärmen i loungen utanför, där du loggar in med din tagg. Se {a("/tvatt", "Tvätt")}.</li>
<li><strong>Tagg och porttelefon:</strong> din tagg öppnar entrén och föreningens utrymmen, och porttelefonen ringer till din mobil. Se {a("/passersystem-och-porttelefon", "Passersystem och porttelefon")}.</li>
<li><strong>Cyklar och förråd:</strong> se {a("/cykelrum-och-forrad", "Cykelrum och förråd")}.</li>
<li><strong>Ordningsregler:</strong> tider för tystnad och borrning, balkongen och mer. Se {a("/ordningsregler", "Ordningsregler")}.</li>
<li><strong>Något är trasigt:</strong> gör en serviceanmälan hos förvaltaren. Se {a("/felanmalan", "Felanmälan")}.</li>
<li><strong>Skötsel av ditt hem:</strong> {a("/skotsel-och-underhall", "tips och instruktioner för badrum, kök, golv och mer")}.</li>
<li><strong>Sopor:</strong> {a("/sopor-och-miljo", "källsortering och miljötips")}.</li>
</ul>""", note="NEW synthesized checklist; every item sourced from existing pages")

page("regler", "Ordningsregler", "Bo i huset",
     f"""<p>För allas trevnad i föreningen gäller följande riktlinjer.</p>
<h2>Tider</h2>
<ul>
<li>Det ska vara lugn och ro mellan kl. 23.00 och 07.00. Inga störningar får förekomma.</li>
<li>Borrning, spikning och liknande får ske vardagar kl. 08.00–20.00 och helger och helgdagar kl. 10.00–19.00.</li>
<li>Behöver du borra eller liknande utanför dessa tider krävs godkännande från styrelsen. Kontakta {EMAIL}.</li>
</ul>
<p>Föreningen kan säga upp bostadsrätten till avflyttning om störningar förekommer.</p>
<h2>Balkongen</h2>
<ul>
<li>Hantera vatten och vattna blommor försiktigt. Vattnet kan annars rinna ner på grannens balkong under din.</li>
<li><strong>Det är absolut förbjudet att sopa ner smuts eller saker, skaka och vädra textilier eller hälla ut vatten eller vätskor från balkongen,</strong> eftersom det drabbar balkongerna under.</li>
</ul>
<h2>Matlagning</h2>
<p>Använd köksfläkten vid matlagning. Dra ut kåpan över spisen tills du hör ett klick, så att matos inte sprider sig till grannlägenheter.</p>
<h2>Ombyggnation och renovering</h2>
<p>Sedan 1 januari 2023 gäller en ny lag om ombyggnation och renovering av bostadsrätter. Vissa förändringar kräver tillstånd från styrelsen. Skicka ansökan i god tid till {EMAIL}. Ansökningar behandlas bara på styrelsemöten.</p>
<h2>Andrahandsuthyrning</h2>
<p>Uthyrning i andra hand kräver styrelsens godkännande i förväg. Se {a("/andrahandsuthyrning", "Andrahandsuthyrning")}.</p>
<h2>Parkering och cyklar</h2>
<p>Se {a("/parkering", "Parkering")} och {a("/cykelrum-och-forrad", "Cykelrum och förråd")}.</p>""",
     note="NEW: standing rules extracted from news 509, 514 (quiet/drilling hours, balcony, köksfläkt, renovation law)")

_park_tail = md("mitt-boende__parkering")
_park_tail = _park_tail[_park_tail.index("<p>Varje lägenhet"):]     # keep the old rules for extra spaces, company cars, etc.
PARK_INTRO = f"""<h2>Platser och pris</h2>
<p>I garaget under gården har Brf Höjden 36 parkeringsplatser: 27 vanliga garageplatser och 9 laddplatser. Alla platser är uthyrda just nu. En vanlig garageplats kostar 1 061 kr per månad.</p>
<h2>Så fungerar det</h2>
<ul>
<li>Alla platser kräver parkeringstillstånd. Du ställer dig i kö, hyr en plats eller säger upp din plats via ARC, föreningens förvaltare: {ARC_MAIL}.</li>
<li>När ARC tilldelar dig en plats får du en inbjudan att aktivera tillståndet hos parkeringsoperatören ePARK. ePARK har varit operatör i området sedan 1 september 2025 (tidigare Aimo Park).</li>
<li>Uppsägning av platsen görs via ARC, och uppsägningstiden är 3 månader. Att säga upp tillståndet i ePARK avslutar inte hyresavtalet med föreningen.</li>
<li>Säljer du din lägenhet får köparen ta över din parkeringsplats utan att gå via kön.</li>
</ul>
<h2>Hyra direkt av ePARK</h2>
<p>Du kan också hyra en plats direkt av ePARK. Då räknas du som extern hyresgäst och betalar moms på priset, så det blir något dyrare. Föreningen har ett begränsat antal platser.</p>
<h2>Regler för fler än en plats och tjänstebil</h2>
"""
page("parkering", "Parkering", "Bo i huset",
     PARK_INTRO + _park_tail + f"""<h2>Gäster och tillfällig parkering</h2>
<p>Det råder parkeringsförbud i hela området, utom på tydligt markerade platser. Vid ingångarna från gatan finns en av- och påstigningszon. Den är allmän gata och tillhör inte föreningen. Parkerar du där mer än 10 minuter riskerar du böter på 800 kronor, och du blockerar taxi, budbilar och grannar som ska lasta av.</p>
<p>Behöver du parkera tillfälligt finns gratis parkering på Västra kyrkogården, där man kan stå ett dygn i taget. Du ansvarar själv för att kontrollera skyltarna. Göteborgs stad erbjuder också gästparkeringar mot avgift.</p>""",
     note="Rewritten 2026-10-25 with chairman's facts: 27+9 spaces all rented, 1 061 kr, ARC assigns, ePARK activation, 3 months notice, buyer takes over, ePARK direct rental; old extra-space/company-car rules kept. Price of charging spaces not stated")

page("tvatt", "Tvätt", "Bo i huset",
     """<p>Tvättstugan och tvättlounge bokas på skärmen i loungen utanför tvättstugan. Du loggar in på skärmen med din tagg.</p>
<p>Här hittar du också skötselråd för tvättstugeinredning.</p>""", docs=["Skötsel tvätt.pdf"], note="Rewritten with user's new info")

page("pool", "Bil- och cykelpool", "Bo i huset",
     f"""<h2>Cykelpool</h2>
<p>Du har möjlighet att gå med i cykelpoolen. Som medlem i poolen kan du hyra cyklar till ett subventionerat pris.</p>
<p><strong>Så här går du med:</strong> registrera dig i cykelpoolens app (GoRide). Om det inte fungerar, kontakta styrelsen: {EMAIL}.</p>
<p>Medlemskapet är gratis. Den första bokade timmen kostar 0 kr, därefter 10 kr eller 15 kr per timme beroende på vilken cykel du väljer.</p>
<h2>Bilpool</h2>
<p>Som boende har du tillgång till bilpoolen KINTO Share (tidigare Aimo Share, byte från 1 maj 2025).</p>
<p>Så här går du med gratis:</p>
<ol><li>Registrera dig på www.kinto-mobility.se</li><li>Ladda ner KINTO-appen</li><li>Boka bil i appen</li></ol>
<p>Mer information finns i bilpoolsinfon nedan. Frågor: kundservice.share@kinto-mobility.se, +46 10 179 96 00.</p>""",
     docs=["BILPOOLSINFO Ekebäckshöjd.pdf"], note="Cykelpool sign-up now 'register in the app (GoRide), else contact the board' per chairman 2026-10-25; GoRide name confirmed and Pennygången 86 address removed by chairman 2026-10-25. Car pool = KINTO Share")

page("cykel", "Cykelrum och förråd", "Bo i huset",
     """<h2>Cykelrum</h2>
<ul>
<li>Cykelrum finns i det övre garaget, under Ekens husdel på Sjupundsgatan 43.</li>
<li>Ett cykelförråd finns på Sjupundsgatan 31 (tidigare rullstolsförråd).</li>
<li>Cykelrummet i det nedre garaget, under Sjupundsgatan 13, är avvecklat.</li>
<li>Cyklar får inte stå i mitten av rummet i övre garaget. Cykelstället där är borttaget.</li>
<li>Oanvända barnvagnsrum får användas till cyklar tillfälligt, så länge det inte finns barnvagnar där.</li>
<li>Läs och följ instruktionerna som sitter på väggarna i cykelrummen.</li>
</ul>
<h2>Förråd</h2>
<p>Barnvagnsförråd finns i fastigheten. Vissa lägenheter har externa förråd och andra har förråd inne i lägenheten. Under vintern 2026 byggdes nya lägenhetsförråd i garagen för de 32 lägenheter som saknade förråd. Utdelningen är klar och det finns inga lediga förråd kvar att dela ut.</p>""",
     note="From uteplats page (edited earlier) + news 504, 536-538. Confirmed by chairman 2026-10-25: no.31 room permanent; no.43 room = upper garage room")

page("balkong", "Balkong och uteplats", "Bo i huset",
     f"""<p>Till varje lägenhet hör en balkong eller uteplats. Du kan också njuta i den gemensamma takparken, som ligger på ett annat hus i kvarteret och delas med de andra boende i Ekebäckshöjd.</p>
<p>Många sätter sin personliga prägel på balkongen. Inred den med eftertanke och var aktsam med husets fasad.</p>
<p>Regler för balkongen finns under {a("/ordningsregler", "Ordningsregler")}.</p>
<h2>Balkonginglasning</h2>
<p>Föreningen har ett avtal med Balkongrutan och bygglov för balkonginglasning är beviljat. Aktuell information finns i nyhetsarkivet (kräver inloggning), eller kontakta styrelsen.</p>""",
     note="uteplats balcony part + glazing summary from news 519-525, 533")

page("las", "Passersystem och porttelefon", "Bo i huset", md("mitt-boende__lassystem", cut_from=r"#{1,4} *Dokument"))

page("bredband", "Bredband, TV och telefoni", "Bo i huset",
     f"""<p>Föreningen har ett gemensamt avtal med Tele2. Kostnaden är <strong>151 kr per månad</strong> och läggs på månadsavgiften.</p>
<h2>Det här ingår</h2>
<ul><li>Bredband (upp till 1 Gbit/s)</li><li>TV Grundutbud, med digital-tv-mottagare (TV-box)</li><li>Trådlös router (Wi-Fi)</li></ul>
<h2>Som nyinflyttad</h2>
<p><strong>Varje ny medlem behöver ringa Tele2 vid inflyttning och be om aktivering.</strong> Kundservice för gruppavtal: 0775-17 17 20 (vardagar 08.00–19.00, lördagar 09.00–15.00). Du kan också beställa på tele2.se/gruppavtal.</p>
<p>Du tecknar själv eget avtal för övriga tjänster utöver det som ingår.</p>""", note="User-supplied facts; replaced 2024 transition text")

page("andra", "Andrahandsuthyrning", "Bo i huset", md("mitt-boende__andrahandsuthyrning", cut_from=r"#{1,4} *Dokument"),
     docs=["ansokan_andrahand.pdf", "Instruktion-andrahandsuthyrning-bostadsrättshavare-hyresgäst.pdf", "avtalupplatelseandrahan_BRF.pdf"],
     note="Typos fixed earlier; policy text unchanged. Docs attached")

page("sopor", "Sopor och miljö", "Bo i huset", md("mitt-boende__miljotips"), note="From Miljötips")

# ================= SKÖTSEL OCH UNDERHÅLL ==========================================
page("skotsel", "Skötsel och underhåll", "Skötsel och underhåll",
     f"""<p>Här hittar du skötselråd och leverantörernas instruktioner för ditt hem.</p>
<ul>
<li>{a("/badrum", "Badrum")}</li><li>{a("/kok", "Kök")}</li><li>{a("/fonster", "Fönster")}</li><li>{a("/golv", "Parkettgolv")}</li>
<li>{a("/vaggar-och-tak", "Väggar och tak")}</li><li>{a("/elektricitet", "Elektricitet")}</li><li>{a("/ventilation", "Ventilation")}</li><li>{a("/brandskydd", "Brandskydd och brandvarnare")}</li>
</ul>
<p>Något som inte fungerar? Gör en serviceanmälan, se {a("/felanmalan", "Felanmälan")}.</p>""", note="NEW overview page")

page("badrum", "Badrum", "Skötsel och underhåll", md("mitt-boende__badrum", cut_from=r"#{1,4} *Dokument"),
     docs=["Skötsel badrumsinredning.pdf", "Kakelbranschen informerar om skötsel av kakel och klinker.pdf", "Montering och skötsel blandare Mora MMIX.pdf",
           "Montering och skötsel Mora MMIX S5.pdf", "Takdusch Mora MMIX Shower System.pdf", "Montering och skötsel, Mora MMIX Blandare.pdf",
           "Montering och skötsel, Nautic Blandare.pdf", "Skötsel blandare Gustavsberg.pdf", "Skötsel Toalettsitsar.pdf", "Skötsel Toalettstol.pdf"])
page("kok", "Kök", "Skötsel och underhåll", md("mitt-boende__kok", cut_from=r"#{1,4} *Dokument"),
     docs=["Skötsel kök och bänkskivor.pdf", "Skötselanvisning Diskho.pdf"])
page("fonster", "Fönster", "Skötsel och underhåll", md("mitt-boende__fonster", cut_from=r"#{1,4} *Dokument"),
     docs=["Skötsel Fönster Elit (val).pdf", "Skötsel Fönsterbänkar Thorsbergs.pdf"])
page("golv", "Parkettgolv", "Skötsel och underhåll", md("mitt-boende__parkettgolv-och-trappa", cut_from=r"#{1,4} *Dokument"),
     docs=["Reparationshandbok Kährs.pdf", "Underhållshandbok Kährs.pdf"])
page("vaggar", "Väggar och tak", "Skötsel och underhåll",
     md("mitt-boende__vaggar-och-tak", cut_from=r"#{1,4} *Dokument") + "<h2>Väggkulör</h2><p>Väggkulören i kök, vardagsrum och samtliga sovrum är NCS S0500-N, bruten vit.</p>",
     docs=["Skötselråd väggar och tak.pdf"], note="Merged Materialval (wall colour)")
page("elektricitet", "Elektricitet", "Skötsel och underhåll",
     md("mitt-boende__elektricitet", cut_from=r"#{1,4} *Dokument", drop_re=[r"^!\[\]\(assets/DCL_uttagen\.jpeg\)\s*$"]),
     note="Stena -> ARC fixed. DCL image not yet embedded")
page("ventilation", "Ventilation", "Skötsel och underhåll", md("mitt-boende__ventilation", cut_from=r"#{1,4} *Dokument"))
page("brandskydd", "Brandskydd och brandvarnare", "Skötsel och underhåll",
     md("mitt-boende__brandskydd", drop_re=[r"^\[Fler goda råd[^\n]*\n"]) + "<h2>Brandvarnare</h2>" + md("mitt-boende__brandvarnare").replace("<h2>Din bostad är utrustad med brandvarnare.</h2>", "<p><strong>Din bostad är utrustad med brandvarnare.</strong></p>"),
     docs=["Goda råd om att förebygga brand i hemmet.pdf", "Manual_brandvarnare_99x105_SE-nordic_19-06_web.pdf"],
     note="Merged Brandskydd + Brandvarnare; other association's link removed")

# ================= FELANMÄLAN OCH KONTAKT =========================================
page("felanmalan", "Felanmälan", "Felanmälan och kontakt",
     f"""<h2>Serviceanmälan</h2>
<p>Gör din serviceanmälan hos föreningens förvaltare, ARC Fastighetspartner: <strong>{ARC}</strong></p>
<p>Akuta ärenden rings in till jouren: <strong>010-551 47 00</strong></p>
<h2>Vem ansvarar för vad?</h2>
<h3>Gemensamma utrymmen i huset</h3>
<p>Ärenden som gäller föreningens gemensamma utrymmen hanterar ARC åt föreningen.</p>
<h3>Inne i din lägenhet</h3>
<p>Det mesta inne i lägenheten är ditt eget ansvar som medlem. ARC kan hjälpa dig, men arbetet debiteras då dig.</p>
<h3>Garantiärenden</h3>
<p>Om du, eller ARC:s fastighetsansvarige, bedömer att felet är ett garantifel anmäls det till Stena Fastigheter. Stena tar hand om ärendet tillsammans med Skanska och återkommer till dig.</p>
<p>Det tar ett tag för en ny fastighet att sätta sig på den nya marken, och då kan så kallade sättningssprickor uppstå. Sprickorna är ofarliga och åtgärdas när huset satt sig ordentligt.</p>
<h3>Om felet är föreningens ansvar</h3>
<p>Då hanterar ARC det. ARC begär nästan alltid styrelsens godkännande innan föreningen betalar för arbetet.</p>
<h2>Allmänna utrymmen utanför trapphusen</h2>
<p>Stena Fastigheter ansvarar för de allmänna utrymmena i Ekebäckshöjd utanför trapphusen, till exempel gårdar, garage, takpark och lounge. Kontakta styrelsen om ärendet gäller dessa ytor. Vid akuta ärenden som rör dem ringer du Stena Fastigheters jour: 0771-80 50 60 eller 031-718 00 08.</p>
<h2>Hiss</h2>
<p>Varje gång hissleverantören Otis kontaktas kostar det mellan 1 500 och 3 000 kronor, även om hissen visar sig fungera. Kontakta därför alltid ARC först, som kan bedöma om Otis behöver tillkallas. Undantag: i akuta situationer, till exempel om du blir fast i hissen, använder du nödknappen.</p>
<h2>Vitvaror</h2>
<p>Vid problem med dina vitvaror gör du en felanmälan direkt till Elon via e-post: {ELON_MAIL}. Mer information och telefonnummer till Elon finns i garantibevisen nedan.</p>""",
     docs=["garantibevis_BRF Höjden .pdf", "garantibevis vitvaror höjden.pdf"],
     note="Rewritten 2026-10-25 per chairman: common areas -> ARC for BRF; inside apartment mostly member's cost; warranty -> Stena with Skanska; BRF issues -> ARC (board approval). Stena paragraph for areas outside stairwells kept (news 516). CHECK: '2 år' settlement-crack wording removed; unsure if still relevant")

page("kontakt", "Kontakta styrelsen", "Felanmälan och kontakt",
     f"""<p>E-post: <strong>{EMAIL}</strong></p>
<p>Vid akuta fall, ring ordföranden på <strong>072-970 71 42</strong>.</p>
<p>Gäller det ett fel i huset, se {a("/felanmalan", "Felanmälan")}. Gäller det månadsavgiften, se {a("/manadsavgift-och-avier", "Månadsavgift och avier")}.</p>
<p>Du kan också skicka ett meddelande med formuläret nedan.</p>""", note="Replaces Joomla send-message page; has contact form module")

page("avgift", "Månadsavgift och avier", "Felanmälan och kontakt",
     f"""<p>I månadsavgiften ingår värme och kallvatten. Varmvatten debiteras efter faktisk förbrukning och faktureras två månader i efterhand. Bredband och TV via föreningens avtal läggs också på avgiften, se {a("/bredband-tv-och-telefoni", "Bredband, TV och telefoni")}.</p>
<p>Du behöver teckna eget avtal för hemförsäkring, el och telefoni.</p>
<p>Föreningens ekonomiska förvaltare är ARC Fastighetspartner. Avierna hanteras och skickas via e-post från ARC ({ARC_MAIL}).</p>""",
     note="Old page + Tele2 fee note (151 kr per user)")

page("maklare", "För mäklare", "Felanmälan och kontakt",
     f"""<p>För att hämta mäklarbild från Brf Höjden, kontakta ARC Fastighetspartner: {ARC_MAIL}</p>""")

page("medlemskontakter", "Medlemskontakter", "Felanmälan och kontakt",
     f"""<p>Praktiska kontaktuppgifter för medlemmar. Sidan kräver inloggning.</p>
<h2>Föreningen</h2>
<ul><li>Styrelsen: {EMAIL}</li><li>Valberedningen (Petter Thomée): {a("mailto:petterthomee@gmail.com", "petterthomee@gmail.com")}</li></ul>
<h2>Förvaltare: ARC Fastighetspartner</h2>
<ul><li>Växel och jour: 010-551 47 00</li><li>Ansvarig för fastigheten, Johannes Lindqvist: 010-551 47 34</li><li>Serviceanmälan: {ARC}</li><li>Avier, parkeringskö och mäklarbild: {ARC_MAIL}</li></ul>
<h2>Stena Fastigheter (allmänna utrymmen, jour)</h2>
<ul><li>0771-80 50 60 eller 031-718 00 08</li></ul>
<h2>Övrigt</h2>
<ul><li>Vitvaror (Elon): {ELON_MAIL}</li><li>Tele2 kundservice för gruppavtalet: 0775-17 17 20</li><li>KINTO Share (bilpool): kundservice.share@kinto-mobility.se, +46 10 179 96 00</li></ul>""",
     access=MEMBERS, note="NEW members-only directory; holds the personal contact details moved off public pages")


# ================= START PAGE ======================================================
START_HTML = f"""<p>Brf Höjden består av 84 ljusa och välplanerade lägenheter i de nya kvarteren Ekebäckshöjd i Högsbohöjd, strax sydväst om centrala Göteborg. Här hittar du som medlem och boende det mesta du behöver veta om föreningen och ditt hem.</p>
<h2>Vanliga frågor</h2>
<ul>
<li><strong>Något är trasigt?</strong> {a("sidor/felanmalan", "Felanmälan")}</li>
<li><strong>Ny i huset?</strong> {a("sidor/ny-i-huset", "Checklista för nyinflyttade")}</li>
<li><strong>Bredband och TV:</strong> {a("sidor/bredband-tv-och-telefoni", "så aktiverar du")}</li>
<li><strong>Tvätt, parkering, cykel och förråd:</strong> {a("sidor/tvatt", "Tvätt")}, {a("sidor/parkering", "Parkering")}, {a("sidor/cykelrum-och-forrad", "Cykelrum och förråd")}</li>
<li><strong>Regler i huset:</strong> {a("sidor/ordningsregler", "Ordningsregler")}</li>
<li><strong>Skötsel av ditt hem:</strong> {a("sidor/skotsel-och-underhall", "badrum, kök, golv och mer")}</li>
<li><strong>Månadsavgift och avier:</strong> {a("sidor/manadsavgift-och-avier", "läs mer")}</li>
</ul>
<h2>Nyheter och dokument för medlemmar</h2>
<p>Nyheter, årsredovisningar och medlemskontakter kräver inloggning. {a("nyheter", "Gå till nyheterna")} eller {a("sidor/ekonomi", "Ekonomi och årsredovisningar")}.</p>
<h2>Kontakt</h2>
<p>Styrelsen: {EMAIL}<br>Akut: ring ordföranden på 072-970 71 42<br>Jour för fel i huset: 010-551 47 00</p>"""

SLUGS = dict(om="om-brf-hojden", styrelse="styrelse-och-valberedning", stamma="foreningsstamma", stadgar="stadgar", ekonomi="ekonomi", grontbolan="gront-bolan",
             bostadsratt="att-bo-i-bostadsratt", nyinflyttad="ny-i-huset", regler="ordningsregler", parkering="parkering", tvatt="tvatt",
             pool="bil-och-cykelpool", cykel="cykelrum-och-forrad", balkong="balkong-och-uteplats", las="passersystem-och-porttelefon",
             bredband="bredband-tv-och-telefoni", andra="andrahandsuthyrning", sopor="sopor-och-miljo", skotsel="skotsel-och-underhall",
             badrum="badrum", kok="kok", fonster="fonster", golv="golv", vaggar="vaggar-och-tak", elektricitet="elektricitet",
             ventilation="ventilation", brandskydd="brandskydd", felanmalan="felanmalan", kontakt="kontakt", avgift="manadsavgift-och-avier",
             maklare="for-maklare", medlemskontakter="medlemskontakter", bilagor="bilagor-till-nyheter", start="valkommen")


def finalize():
    """Relative internal links (work under any base path/domain) + slugs; returns list of page dicts."""
    out = []
    allp = PAGES + [dict(key="start", title="Välkommen", section=None, html=START_HTML, access=PUBLIC, docs=[], note="NEW start page", reuse=None)]
    for p in allp:
        h = p["html"]
        h = re.sub(r'href="/(?!/)([a-z0-9-]+)"', r'href="\1"', h)            # /felanmalan -> felanmalan (same sidor/ dir)
        # old pages glue a bold lead-in to its text: make it a proper sub-heading
        def lead(m):
            title, rest = m.group(1), m.group(2).lstrip()
            rest = re.sub(r"^(<br ?/?>\s*)+", "", rest)
            return f"<h3>{title}</h3>" + (f"<p>{rest}" if rest.strip() not in ("", "</p>") else "")
        h = re.sub(r"<p><strong>([^<.:]{3,45})</strong>(.*?)(?=$|\n)", lead, h, flags=re.M)
        p = dict(p, html=h, slug=SLUGS[p["key"]])
        out.append(p)
    return out


page("bilagor", "Bilagor till nyheter", "Föreningen",
     """<p>Här finns bilagor och bilder som hör till nyheter i nyhetsarkivet.</p>
<ul>
<li><strong>Visning av balkonginglasning (mars 2025):</strong> presentation från visningen.</li>
<li><strong>Priser och detaljer för balkonginglasning:</strong> offert från Balkongrutan.</li>
<li><strong>Nyhetsbrev januari 2026:</strong> bilder från cykelrum och förråd.</li>
</ul>""",
     access=MEMBERS, docs=["Offert Brf Höjden 2.1-komprimerad.pdf", "BR Visning Brf Höjden BF.pdf", "IMG_1413.jpg", "IMG_1414.jpg", "IMG_1416.jpg", "IMG_1417.jpg",
                           "IMG_1419.jpg", "IMG_1420.jpg", "IMG_1421.jpg", "IMG_1424.jpg"],
     note="NEW members page: attachments/images that belonged to news posts (news form has no file module)")
