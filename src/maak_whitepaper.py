#!/usr/bin/env python3
"""GVI-whitepaper: 'AI met menselijke maat — verantwoord starten met AI in vijf stappen'."""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Spacer, NextPageTemplate, PageBreak, Table, TableStyle)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

SITE = "/Users/irisfickeryounge/Documents/Claude/Projects/Fable 5 Projects/gvi-website"
LOGO = os.path.join(SITE, "assets", "gvi-logo.png")
UIT = os.path.join(SITE, "downloads", "gvi-whitepaper-ai-met-menselijke-maat.pdf")

NACHT = HexColor("#1D1039")
NACHT2 = HexColor("#2E1A55")
FUCHSIA = HexColor("#E6349C")
FUCHSIA_L = HexColor("#FF3DA6")
INKT = HexColor("#241834")
INKT_Z = HexColor("#5A4E70")
MIST = HexColor("#F7F5FB")
LIJN = HexColor("#E7E2F2")

# ---- Fonts: probeer nette systeemfonts (Avenir Next ~ Sora, Helvetica Neue ~ Inter) ----
KOP, KOP_B, BODY, BODY_B = "Helvetica", "Helvetica-Bold", "Helvetica", "Helvetica-Bold"
try:
    pdfmetrics.registerFont(TTFont("AvenirNext", "/System/Library/Fonts/Avenir Next.ttc", subfontIndex=5))
    pdfmetrics.registerFont(TTFont("AvenirNext-Bold", "/System/Library/Fonts/Avenir Next.ttc", subfontIndex=0))
    KOP, KOP_B = "AvenirNext", "AvenirNext-Bold"
except Exception as e:
    print("Avenir niet geladen:", e)
try:
    pdfmetrics.registerFont(TTFont("HelvNeue", "/System/Library/Fonts/HelveticaNeue.ttc", subfontIndex=0))
    pdfmetrics.registerFont(TTFont("HelvNeue-Bold", "/System/Library/Fonts/HelveticaNeue.ttc", subfontIndex=1))
    BODY, BODY_B = "HelvNeue", "HelvNeue-Bold"
except Exception as e:
    print("HelveticaNeue niet geladen:", e)
from reportlab.pdfbase.pdfmetrics import registerFontFamily
registerFontFamily(KOP, normal=KOP, bold=KOP_B, italic=KOP, boldItalic=KOP_B)
registerFontFamily(BODY, normal=BODY, bold=BODY_B, italic=BODY, boldItalic=BODY_B)

W, H = A4
M = 22 * mm

# ---- Achtergrondtekeningen ----
def golven(c, y_basis, sterkte=1.0, kleur=FUCHSIA_L):
    c.saveState()
    c.setLineWidth(1.1)
    for i, dy in enumerate((0, 9, 20)):
        c.setStrokeColor(kleur)
        c.setStrokeAlpha((0.5 - i * 0.13) * sterkte)
        p = c.beginPath()
        p.moveTo(-20, y_basis - dy)
        p.curveTo(W * 0.3, y_basis - dy + 26, W * 0.55, y_basis - dy - 22, W * 0.8, y_basis - dy + 8)
        p.curveTo(W * 0.9, y_basis - dy + 18, W * 0.97, y_basis - dy + 4, W + 20, y_basis - dy + 12)
        c.drawPath(p, stroke=1, fill=0)
    c.restoreState()

def spraakgolf(c, x, y, kleur, alpha=.8, schaal=1.0):
    hoogtes = [8, 20, 34, 15, 28, 10, 22, 13, 6]
    c.saveState()
    c.setStrokeColor(kleur)
    c.setStrokeAlpha(alpha)
    c.setLineWidth(2.6 * schaal)
    c.setLineCap(1)
    for i, h in enumerate(hoogtes):
        xx = x + i * 7.5 * schaal
        c.line(xx, y - h * schaal, xx, y + h * schaal)
    c.restoreState()

def omslag(c, doc):
    c.saveState()
    c.setFillColor(NACHT)
    c.rect(0, 0, W, H, stroke=0, fill=1)
    # zachte gloed rechtsboven
    c.setFillColor(NACHT2)
    c.circle(W * 0.85, H * 0.8, 180, stroke=0, fill=1)
    c.setFillColor(NACHT)
    c.setFillAlpha(.4)
    c.circle(W * 0.85, H * 0.8, 180, stroke=0, fill=1)
    c.setFillAlpha(1)
    # spraakgolf → stromen
    spraakgolf(c, 40, H * 0.32, HexColor("#B9A9E0"), alpha=.55)
    golven(c, H * 0.30, sterkte=1.2)
    golven(c, H * 0.26, sterkte=.7, kleur=FUCHSIA)
    # logo
    try:
        c.drawImage(LOGO, M, H - M - 26 * mm, width=52 * mm, height=52 * mm * 601 / 1195,
                    mask='auto', preserveAspectRatio=True)
    except Exception as e:
        print("logo:", e)
    # titelblok
    c.setFillColor(white)
    c.setFont(KOP_B, 34)
    c.drawString(M, H * 0.60, "AI met menselijke maat")
    c.setFillColor(FUCHSIA_L)
    c.setFont(KOP_B, 19)
    c.drawString(M, H * 0.60 - 13.5 * mm, "Verantwoord starten met AI")
    c.drawString(M, H * 0.60 - 21 * mm, "in vijf stappen")
    c.setFillColor(HexColor("#CFC5E8"))
    c.setFont(BODY, 11.5)
    c.drawString(M, H * 0.60 - 34 * mm, "Een praktische gids voor MKB en publieke organisaties —")
    c.drawString(M, H * 0.60 - 40 * mm, "zonder hype, met regie.")
    # onderregel
    c.setFillColor(HexColor("#9F92C8"))
    c.setFont(BODY, 9.5)
    c.drawString(M, 18 * mm, "GVI Whitepaper · juli 2026 · globalvoiceintelligence.com")
    c.restoreState()

def binnenpagina(c, doc):
    c.saveState()
    # kopregel
    c.setStrokeColor(LIJN); c.setLineWidth(1)
    c.line(M, H - 14 * mm, W - M, H - 14 * mm)
    c.setFillColor(INKT_Z); c.setFont(BODY, 8.2)
    c.drawString(M, H - 12 * mm, "GVI — AI met menselijke maat")
    c.drawRightString(W - M, H - 12 * mm, "Verantwoord starten met AI in vijf stappen")
    # voetregel
    c.setFillColor(INKT_Z); c.setFont(BODY, 8.2)
    c.drawString(M, 12 * mm, "© 2026 GVI — Global Voice Intelligence")
    c.setFillColor(FUCHSIA)
    c.setFont(KOP_B, 9)
    c.drawRightString(W - M, 12 * mm, str(doc.page))
    # subtiele golf onderaan
    golven(c, 26, sterkte=.35, kleur=FUCHSIA)
    c.restoreState()

def slotpagina(c, doc):
    c.saveState()
    c.setFillColor(NACHT)
    c.rect(0, 0, W, H, stroke=0, fill=1)
    spraakgolf(c, W - 120, H * 0.78, HexColor("#B9A9E0"), alpha=.45, schaal=.8)
    golven(c, H * 0.22, sterkte=1.0)
    try:
        c.drawImage(LOGO, M, H - M - 30 * mm, width=60 * mm, height=60 * mm * 601 / 1195,
                    mask='auto', preserveAspectRatio=True)
    except Exception:
        pass
    c.setFillColor(white)
    c.setFont(KOP_B, 20)
    c.drawString(M, H * 0.62, "Verder praten?")
    c.setFillColor(HexColor("#DDD5F0"))
    c.setFont(BODY, 11.5)
    regels = [
        "Wil je weten waar jouw organisatie staat met AI?",
        "",
        "•  AI Regie Scan — in één sessie weten waar je staat",
        "•  Plan een verkennend gesprek — altijd een persoonlijke reactie",
        "",
        "www.globalvoiceintelligence.com",
        "irisfickeryounge+gvi@gmail.com",
    ]
    y = H * 0.62 - 12 * mm
    for r in regels:
        c.drawString(M, y, r)
        y -= 7.2 * mm
    c.setFillColor(HexColor("#9F92C8"))
    c.setFont(BODY, 9)
    c.drawString(M, 18 * mm, "GVI — Global Voice Intelligence · AI met menselijke maat · © 2026")
    c.restoreState()

# ---- Stijlen ----
st_kicker = ParagraphStyle("kicker", fontName=KOP_B, fontSize=10, leading=13,
                           textColor=FUCHSIA, spaceAfter=3 * mm)
st_h1 = ParagraphStyle("h1", fontName=KOP_B, fontSize=21, leading=26,
                       textColor=NACHT, spaceAfter=5 * mm)
st_h2 = ParagraphStyle("h2", fontName=KOP_B, fontSize=13.5, leading=17,
                       textColor=NACHT, spaceBefore=5 * mm, spaceAfter=2.5 * mm)
st_body = ParagraphStyle("body", fontName=BODY, fontSize=10.6, leading=16,
                         textColor=INKT, spaceAfter=3.2 * mm, alignment=TA_LEFT)
st_intro = ParagraphStyle("intro", parent=st_body, fontSize=12, leading=18.5,
                          textColor=INKT_Z, spaceAfter=4 * mm)
st_quote = ParagraphStyle("quote", fontName=KOP_B, fontSize=12.5, leading=18,
                          textColor=NACHT, leftIndent=6 * mm, spaceBefore=3 * mm,
                          spaceAfter=4 * mm, borderPadding=0)
st_check_t = ParagraphStyle("checkt", fontName=KOP_B, fontSize=10.5, leading=14, textColor=white)
st_check = ParagraphStyle("check", fontName=BODY, fontSize=10, leading=15.5, textColor=white)

def kader(titel, punten):
    """Nachtpaars checklist-kader."""
    inhoud = [[Paragraph(titel, st_check_t)]]
    for p in punten:
        inhoud.append([Paragraph('<font color="#FF3DA6"><b>•</b></font>&nbsp;&nbsp;' + p, st_check)])
    t = Table(inhoud, colWidths=[W - 2 * M - 10 * mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), NACHT),
        ("LEFTPADDING", (0, 0), (-1, -1), 6 * mm),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6 * mm),
        ("TOPPADDING", (0, 0), (0, 0), 5 * mm),
        ("TOPPADDING", (0, 1), (-1, -1), 1.6 * mm),
        ("BOTTOMPADDING", (0, -1), (-1, -1), 5 * mm),
        ("LINEBEFORE", (0, 0), (0, -1), 3, FUCHSIA),
        ("ROUNDEDCORNERS", [8, 8, 8, 8]),
    ]))
    return t

def statement(tekst):
    t = Table([[Paragraph(tekst, st_quote)]], colWidths=[W - 2 * M - 8 * mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), MIST),
        ("LINEBEFORE", (0, 0), (0, -1), 3, FUCHSIA),
        ("LEFTPADDING", (0, 0), (-1, -1), 5 * mm),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5 * mm),
        ("TOPPADDING", (0, 0), (-1, -1), 4 * mm),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4 * mm),
    ]))
    return t

# ---- Document ----
doc = BaseDocTemplate(UIT, pagesize=A4, leftMargin=M, rightMargin=M,
                      topMargin=24 * mm, bottomMargin=22 * mm,
                      title="AI met menselijke maat — verantwoord starten met AI in vijf stappen",
                      author="GVI — Global Voice Intelligence")
frame = Frame(M, 22 * mm, W - 2 * M, H - 24 * mm - 22 * mm, id="f")
doc.addPageTemplates([
    PageTemplate(id="omslag", frames=[frame], onPage=omslag),
    PageTemplate(id="binnen", frames=[frame], onPage=binnenpagina),
    PageTemplate(id="slot", frames=[frame], onPage=slotpagina),
])

S = []
S.append(NextPageTemplate("binnen"))
S.append(Spacer(1, 1))  # omslag is puur canvas
S.append(PageBreak())

# --- p2: waarom deze gids ---
S.append(Paragraph("Vooraf", st_kicker))
S.append(Paragraph("AI komt het werk binnen. De vraag is wie de regie houdt.", st_h1))
S.append(Paragraph("Medewerkers experimenteren al met AI — vaak zonder afspraken, soms zonder dat de leiding het weet. Leidinggevenden voelen urgentie, teams hebben vragen over werk, veiligheid en kwaliteit, en ergens tussen kansen, risico's en tijdgebrek moet iemand overzicht brengen.", st_intro))
S.append(Paragraph("Deze gids is voor bestuurders, managers en programmaleiders bij MKB-bedrijven en publieke of maatschappelijke organisaties die verantwoord met AI willen starten — zonder zich te verliezen in hype, en zonder maandenlang richtingloos te experimenteren.", st_body))
S.append(Paragraph("Vijf stappen, één principe", st_h2))
S.append(Paragraph("De route in deze gids volgt één principe: <b>technologie volgt mensen, niet andersom</b>. AI kan werk verlichten en versnellen, maar alleen als jouw organisatie zelf blijft kiezen: wat we gebruiken, waarvoor, binnen welke grenzen en met wie. Dat noemen wij AI met menselijke maat.", st_body))
S.append(statement("Begin niet met een tool. Begin met regie."))
S.append(Paragraph("Elke stap sluit af met een korte checklist. Ben je door alle vijf de stappen heen, dan heb je geen AI-strategie van veertig pagina's — wel overzicht, een eerste veilige toepassing en afspraken waar je op kunt bouwen.", st_body))
S.append(PageBreak())

# --- p3: overzicht vijf stappen ---
S.append(Paragraph("Overzicht", st_kicker))
S.append(Paragraph("De vijf stappen in het kort", st_h1))
stappen_ov = [
    ("1 · Zien", "Breng in beeld wat er al gebeurt: wie gebruikt welke AI-tools, waarvoor, en met welke gegevens?"),
    ("2 · Kiezen", "Prioriteer op waarde, risico en haalbaarheid. Niet alles wat kan, hoeft."),
    ("3 · Kaders vóór tools", "Maak eerst afspraken over data, verantwoordelijkheid en veilig gebruik — kies dan pas gereedschap."),
    ("4 · Maak teams AI-geletterd", "AI-geletterdheid is sinds de AI Act (artikel 4) een verplichting — en de snelste weg naar veilig gebruik."),
    ("5 · Begin klein en overdraagbaar", "Eén pilot met een eigenaar, afspraken en een meetpunt — geen losse experimenten."),
]
for kop, tekst in stappen_ov:
    S.append(Paragraph(f'<font color="#E6349C"><b>{kop}</b></font> — {tekst}', st_body))
S.append(Spacer(1, 4 * mm))
S.append(statement("De volgorde is de boodschap: eerst zien en kiezen, dan pas bouwen. Wie bij stap 5 begint, koopt een tool. Wie bij stap 1 begint, houdt de regie."))
S.append(PageBreak())

# --- p4: stap 1 ---
S.append(Paragraph("Stap 1", st_kicker))
S.append(Paragraph("Zien: breng in beeld wat er al gebeurt", st_h1))
S.append(Paragraph("In vrijwel elke organisatie wordt AI al gebruikt — officieel of onder de radar. Medewerkers vatten notulen samen met ChatGPT, herschrijven mails met Copilot of proberen thuis iets uit dat 'op het werk zo handig zou zijn'. Dat is geen probleem; het is informatie.", st_body))
S.append(Paragraph("Maak het gebruik bespreekbaar zonder oordeel. Wie straft, drijft het gebruik ondergronds — en verliest juist het zicht dat nodig is om verantwoord te sturen. Vraag teams wat ze gebruiken, wat het oplevert en waar ze over twijfelen. Noteer ook de zorgen: over banen, kwaliteit en verantwoordelijkheid. Die zorgen zijn geen weerstand, maar risicosignalering van mensen die het werk het beste kennen.", st_body))
S.append(Paragraph("Let daarbij op drie dingen", st_h2))
S.append(Paragraph("<b>Gegevens</b> — gaan er klant-, personeels- of bedrijfsgegevens naar publieke AI-diensten? <b>Afhankelijkheid</b> — ontstaat er werk dat stilvalt als één tool wegvalt? <b>Stille processen</b> — zijn er uitkomsten (adviezen, teksten, beslissingen) waarvan niemand weet dat er AI achter zit?", st_body))
S.append(kader("Checklist · Zien", [
    "We weten welke AI-tools er in de organisatie gebruikt worden — ook informeel.",
    "We weten globaal welke gegevens daarbij gedeeld worden.",
    "Zorgen van medewerkers zijn opgehaald en serieus genomen.",
    "De eerste risicosignalen (data, afhankelijkheid, stille processen) zijn genoteerd.",
]))
S.append(PageBreak())

# --- p5: stap 2 ---
S.append(Paragraph("Stap 2", st_kicker))
S.append(Paragraph("Kiezen: prioriteer op waarde, risico en haalbaarheid", st_h1))
S.append(Paragraph("Veel organisaties hebben tientallen AI-ideeën en nul besluiten. De oplossing is niet méér ideeën, maar een eerlijke rangorde. Leg elk idee langs drie vragen:", st_body))
S.append(Paragraph("<b>1. Waarde</b> — verlicht dit echt werk, of is het vooral leuk om te laten zien? <b>2. Risico</b> — wat kan er misgaan met gegevens, kwaliteit of vertrouwen, en hoe erg is dat? <b>3. Haalbaarheid</b> — hebben we de data, de mensen en de tijd om dit goed te doen?", st_body))
S.append(Paragraph("Kies vervolgens bewust <i>niet</i> voor alles wat overblijft. Twee of drie toepassingen die er echt toe doen, verslaan tien halve experimenten. En durf toepassingen te parkeren waar de risico's nog niet te overzien zijn — zeker waar beslissingen over mensen worden genomen.", st_body))
S.append(Paragraph("Voor publieke organisaties weegt er één vraag extra: <b>kunnen we dit uitleggen?</b> Aan inwoners, aan de raad, aan de toezichthouder. Een toepassing die je niet kunt uitleggen, is nog niet klaar voor gebruik — hoe goed de demo ook was.", st_body))
S.append(kader("Checklist · Kiezen", [
    "Elk idee is gewogen op waarde, risico en haalbaarheid.",
    "Er ligt een top 3 — en een bewuste 'nu niet'-lijst.",
    "Toepassingen die mensen direct raken, krijgen extra zorgvuldigheid.",
    "We kunnen elke gekozen toepassing in gewone taal uitleggen.",
]))
S.append(PageBreak())

# --- p6: stap 3 ---
S.append(Paragraph("Stap 3", st_kicker))
S.append(Paragraph("Kaders vóór tools: afspraken over data en veilig gebruik", st_h1))
S.append(Paragraph("De verleiding is groot om te beginnen bij de tool: een abonnement, een pilotlicentie, kijken wat het doet. Draai het om. Zonder kaders wordt elke tool een risico; met kaders kun je vrijwel elke tool veilig proberen.", st_body))
S.append(Paragraph("Drie basisafspraken die elke organisatie kan maken", st_h2))
S.append(Paragraph("<b>Data</b> — welke gegevens mogen wél en niet in AI-diensten? Maak het concreet: persoonsgegevens, klantdossiers en niet-openbare stukken blijven eruit, tenzij de dienst daar aantoonbaar op is ingericht.", st_body))
S.append(Paragraph("<b>Verantwoordelijkheid</b> — AI mag voorbereiden, mensen beslissen. Spreek af waar menselijke controle verplicht blijft: alles wat naar buiten gaat, alles wat mensen raakt.", st_body))
S.append(Paragraph("<b>Leveranciers</b> — kies bewust waar je afhankelijk van wordt. Vraag naar dataverwerking (AVG), opslaglocatie en exit-mogelijkheden. Digitale soevereiniteit begint bij weten wat je uitbesteedt.", st_body))
S.append(Paragraph("De AI Act en de AVG stellen hier eisen aan — maar laat dat geen papieren exercitie worden. Goede kaders zijn kort, begrijpelijk en werkbaar: één A4 dat iedereen kent, verslaat een beleidsdocument dat niemand leest.", st_body))
S.append(kader("Checklist · Kaders", [
    "Er is een korte, begrijpelijke afspraak over wat wél en niet in AI-tools mag.",
    "Menselijke controle is belegd: AI bereidt voor, mensen beslissen.",
    "Van elke tool weten we: waar staat de data, wie verwerkt haar, hoe komen we eruit?",
    "De kaders passen op één A4 en iedereen kent ze.",
]))
S.append(PageBreak())

# --- p7: stap 4 ---
S.append(Paragraph("Stap 4", st_kicker))
S.append(Paragraph("Maak teams AI-geletterd — het is bovendien verplicht", st_h1))
S.append(Paragraph("Sinds februari 2025 verplicht de Europese AI Act (artikel 4) organisaties die AI inzetten om te zorgen voor een passend niveau van <b>AI-geletterdheid</b> bij hun medewerkers. Maar wie alleen traint omdat het moet, mist het punt: AI-geletterdheid is de snelste route naar veilig én waardevol gebruik.", st_body))
S.append(Paragraph("AI-geletterdheid is meer dan een prompttraining. Het gaat over begrijpen wat AI wel en niet kan, wanneer je uitkomsten kunt vertrouwen, wat veilig is en wat niet — en hoe je AI inzet zonder vakmanschap te verliezen.", st_body))
S.append(Paragraph("Wat werkt", st_h2))
S.append(Paragraph("Train <b>in het eigen werk</b>, met eigen voorbeelden — niet met vergezochte demo's. Maak het <b>rolgericht</b>: een beleidsmedewerker heeft andere vragen dan een planner of een bestuurder. En geef <b>ruimte aan zorgen</b> over baanverlies, kwaliteit en verantwoordelijkheid. Wie zich veilig voelt, leert sneller.", st_body))
S.append(statement("Wie zich veilig voelt, leert sneller — en wie begrijpt wat AI niet kan, gebruikt het beter dan wie alleen de trucjes kent."))
S.append(kader("Checklist · AI-geletterdheid", [
    "Iedereen die met AI werkt, heeft een basis: kunnen, grenzen en risico's.",
    "Training gebeurt met eigen werkvoorbeelden, rolgericht.",
    "Leidinggevenden kunnen sturen op AI zonder zelf techneut te zijn.",
    "We voldoen daarmee aantoonbaar aan AI Act artikel 4.",
]))
S.append(PageBreak())

# --- p8: stap 5 ---
S.append(Paragraph("Stap 5", st_kicker))
S.append(Paragraph("Begin klein en overdraagbaar", st_h1))
S.append(Paragraph("Kies uit je top 3 (stap 2) één toepassing en maak er een echte pilot van — geen los experiment op een privé-account, maar een afgebakende proef met drie ingrediënten:", st_body))
S.append(Paragraph("<b>Een eigenaar</b> — iemand is verantwoordelijk voor de pilot, ook na de eerste weken enthousiasme. <b>Afspraken</b> — de kaders uit stap 3 gelden vanaf dag één. <b>Een meetpunt</b> — spreek vooraf af hoe je ziet of het werkt: tijd, kwaliteit, tevredenheid.", st_body))
S.append(Paragraph("Test met de mensen die er straks mee moeten werken, niet ernaast. En maak het resultaat <b>overdraagbaar</b>: korte documentatie, beheerafspraken, en een eerlijke beslissing na afloop — doorzetten, aanpassen of stoppen. Ook stoppen is een resultaat; het bewijst dat jullie kiezen in plaats van meedrijven.", st_body))
S.append(Paragraph("Geen pilot-theater", st_h2))
S.append(Paragraph("Het grootste risico in deze fase is 'pilot-theater': experimenten die eindeloos doorlopen zonder eigenaar, proces of meetpunt — druk gedoe dat nooit een besluit wordt. De remedie is simpel: elke pilot eindigt op een afgesproken datum met een beslissing.", st_body))
S.append(kader("Checklist · Klein beginnen", [
    "Er loopt één pilot, met eigenaar, kaders en meetpunt.",
    "De mensen die ermee moeten werken, testen mee.",
    "Er is een einddatum met een beslismoment: doorzetten, aanpassen of stoppen.",
    "Het resultaat is gedocumenteerd en overdraagbaar.",
]))
S.append(PageBreak())

# --- p9: valkuilen ---
S.append(Paragraph("Tussendoor", st_kicker))
S.append(Paragraph("Vier valkuilen die je hiermee vermijdt", st_h1))
valkuilen = [
    ("Tool-first denken", "Een licentie kopen en dan pas bedenken waarvoor. De tool wordt het doel, het werk raakt uit beeld — en na een jaar is er 'iets met AI' zonder resultaat."),
    ("Pilot-theater", "Overal experimenten, nergens besluiten. Voelt innovatief, levert niets op en vreet energie van de mensen die wél iets willen afmaken."),
    ("Stille afhankelijkheid", "Werkprocessen die ongemerkt leunen op één tool of leverancier. Pijnlijk zichtbaar bij een prijsverhoging, storing of gewijzigde voorwaarden."),
    ("Angst als beleid", "AI verbieden en hopen dat het overwaait. Het gebruik gaat ondergronds, de risico's nemen toe en de organisatie leert niets."),
]
for kop, tekst in valkuilen:
    S.append(Paragraph(f'<font color="#E6349C"><b>{kop}</b></font>', st_h2))
    S.append(Paragraph(tekst, st_body))
S.append(Spacer(1, 3 * mm))
S.append(statement("Het patroon achter alle vier: de regie ligt bij de technologie in plaats van bij de organisatie. De vijf stappen draaien dat om."))
S.append(PageBreak())

# --- p10: en nu / over GVI ---
S.append(Paragraph("En nu?", st_kicker))
S.append(Paragraph("Van eerste stap naar blijvende regie", st_h1))
S.append(Paragraph("De vijf stappen zijn geen project dat je afvinkt, maar een ritme dat je herhaalt: zien wat er speelt, kiezen wat ertoe doet, kaders bijstellen, mensen meenemen, klein bouwen. Organisaties die dat ritme te pakken hebben, hoeven nooit meer in paniek 'iets met AI'.", st_body))
S.append(Paragraph("Wil je hier niet alleen in staan? GVI helpt organisaties bij precies deze route — van een eerste <b>AI Regie Scan</b> (in één sessie weten waar je staat) tot audit &amp; governance, strategie, werkende pilots en AI-geletterdheid voor teams.", st_body))
S.append(Paragraph("Over GVI", st_h2))
S.append(Paragraph("GVI — Global Voice Intelligence — is de onafhankelijke Nederlandse AI-adviespraktijk van Iris Ficker Younge. Zij combineert beleid, onderwijs, ondernemerschap, duurzaamheid, AI en systeemdenken — voor organisaties die niet alleen sneller willen worden met AI, maar ook zorgvuldiger willen leren kiezen. GVI verkoopt geen tools en heeft geen vendorbelang: advies is advies.", st_body))
S.append(Paragraph("Kernwaarden: menselijke maat, publieke waarden, digitale soevereiniteit, onafhankelijkheid.", st_body))
S.append(Spacer(1, 4 * mm))
S.append(statement("Jij houdt de regie, AI doet het werk."))
S.append(NextPageTemplate("slot"))
S.append(PageBreak())
S.append(Spacer(1, 1))  # slotpagina is puur canvas

doc.build(S)
print("PDF gemaakt:", UIT)
import subprocess
print(subprocess.run(["mdls", "-name", "kMDItemNumberOfPages", UIT], capture_output=True, text=True).stdout)
