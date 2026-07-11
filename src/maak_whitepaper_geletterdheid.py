#!/usr/bin/env python3
"""GVI-whitepaper 2: 'AI-geletterdheid als mensenwerk' — menselijke, pedagogische invalshoek."""
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

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGO = os.path.join(SITE, "assets", "gvi-logo.png")
UIT = os.path.join(SITE, "downloads", "gvi-whitepaper-ai-geletterdheid.pdf")

NACHT = HexColor("#1D1039"); NACHT2 = HexColor("#2E1A55")
FUCHSIA = HexColor("#E6349C"); FUCHSIA_L = HexColor("#FF3DA6")
INKT = HexColor("#241834"); INKT_Z = HexColor("#5A4E70")
MIST = HexColor("#F7F5FB"); LIJN = HexColor("#E7E2F2")

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
    c.setStrokeColor(kleur); c.setStrokeAlpha(alpha)
    c.setLineWidth(2.6 * schaal); c.setLineCap(1)
    for i, h in enumerate(hoogtes):
        xx = x + i * 7.5 * schaal
        c.line(xx, y - h * schaal, xx, y + h * schaal)
    c.restoreState()

def omslag(c, doc):
    c.saveState()
    c.setFillColor(NACHT); c.rect(0, 0, W, H, stroke=0, fill=1)
    c.setFillColor(NACHT2); c.circle(W * 0.82, H * 0.78, 190, stroke=0, fill=1)
    c.setFillColor(NACHT); c.setFillAlpha(.4)
    c.circle(W * 0.82, H * 0.78, 190, stroke=0, fill=1)
    c.setFillAlpha(1)
    spraakgolf(c, 40, H * 0.30, HexColor("#B9A9E0"), alpha=.55)
    golven(c, H * 0.28, sterkte=1.2)
    golven(c, H * 0.24, sterkte=.7, kleur=FUCHSIA)
    try:
        c.drawImage(LOGO, M, H - M - 26 * mm, width=52 * mm, height=52 * mm * 601 / 1195,
                    mask='auto', preserveAspectRatio=True)
    except Exception as e:
        print("logo:", e)
    c.setFillColor(white); c.setFont(KOP_B, 32)
    c.drawString(M, H * 0.62, "AI-geletterdheid")
    c.drawString(M, H * 0.62 - 12.5 * mm, "als mensenwerk")
    c.setFillColor(FUCHSIA_L); c.setFont(KOP_B, 17)
    c.drawString(M, H * 0.62 - 25 * mm, "Een actieplan in vier fasen —")
    c.drawString(M, H * 0.62 - 32 * mm, "voorbij het compliance-vinkje")
    c.setFillColor(HexColor("#CFC5E8")); c.setFont(BODY, 11.5)
    c.drawString(M, H * 0.62 - 45 * mm, "Voor organisaties die teams echt willen meenemen —")
    c.drawString(M, H * 0.62 - 51 * mm, "want elke technologie-verandering is mensenwerk.")
    c.setFillColor(HexColor("#9F92C8")); c.setFont(BODY, 9.5)
    c.drawString(M, 18 * mm, "GVI Whitepaper · juli 2026 · globalvoiceintelligence.com")
    c.restoreState()

def binnenpagina(c, doc):
    c.saveState()
    c.setStrokeColor(LIJN); c.setLineWidth(1)
    c.line(M, H - 14 * mm, W - M, H - 14 * mm)
    c.setFillColor(INKT_Z); c.setFont(BODY, 8.2)
    c.drawString(M, H - 12 * mm, "GVI — AI met menselijke maat")
    c.drawRightString(W - M, H - 12 * mm, "AI-geletterdheid als mensenwerk")
    c.setFillColor(INKT_Z); c.setFont(BODY, 8.2)
    c.drawString(M, 12 * mm, "© 2026 GVI — Global Voice Intelligence")
    c.setFillColor(FUCHSIA); c.setFont(KOP_B, 9)
    c.drawRightString(W - M, 12 * mm, str(doc.page))
    golven(c, 26, sterkte=.35, kleur=FUCHSIA)
    c.restoreState()

def slotpagina(c, doc):
    c.saveState()
    c.setFillColor(NACHT); c.rect(0, 0, W, H, stroke=0, fill=1)
    spraakgolf(c, W - 120, H * 0.78, HexColor("#B9A9E0"), alpha=.45, schaal=.8)
    golven(c, H * 0.22, sterkte=1.0)
    try:
        c.drawImage(LOGO, M, H - M - 30 * mm, width=60 * mm, height=60 * mm * 601 / 1195,
                    mask='auto', preserveAspectRatio=True)
    except Exception:
        pass
    c.setFillColor(white); c.setFont(KOP_B, 20)
    c.drawString(M, H * 0.62, "Verder praten?")
    c.setFillColor(HexColor("#DDD5F0")); c.setFont(BODY, 11.5)
    regels = [
        "Wil je AI-geletterdheid planmatig opbouwen in jouw organisatie?",
        "",
        "•  AI-geletterdheid & Adoptie — programma in vier fasen",
        "•  AI Trainingen — workshops, AI Impact Dag en keynotes",
        "•  AI Regie Scan — in één sessie weten waar je staat",
        "",
        "www.globalvoiceintelligence.com",
        "irisfickeryounge+gvi@gmail.com",
    ]
    y = H * 0.62 - 12 * mm
    for r in regels:
        c.drawString(M, y, r)
        y -= 7.2 * mm
    c.setFillColor(HexColor("#9F92C8")); c.setFont(BODY, 9)
    c.drawString(M, 18 * mm, "GVI — Global Voice Intelligence · AI met menselijke maat · © 2026")
    c.restoreState()

st_kicker = ParagraphStyle("kicker", fontName=KOP_B, fontSize=10, leading=13, textColor=FUCHSIA, spaceAfter=3 * mm)
st_h1 = ParagraphStyle("h1", fontName=KOP_B, fontSize=21, leading=26, textColor=NACHT, spaceAfter=5 * mm)
st_h2 = ParagraphStyle("h2", fontName=KOP_B, fontSize=13.5, leading=17, textColor=NACHT, spaceBefore=5 * mm, spaceAfter=2.5 * mm)
st_body = ParagraphStyle("body", fontName=BODY, fontSize=10.6, leading=16, textColor=INKT, spaceAfter=3.2 * mm, alignment=TA_LEFT)
st_intro = ParagraphStyle("intro", parent=st_body, fontSize=12, leading=18.5, textColor=INKT_Z, spaceAfter=4 * mm)
st_quote = ParagraphStyle("quote", fontName=KOP_B, fontSize=12.5, leading=18, textColor=NACHT, leftIndent=6 * mm, spaceBefore=3 * mm, spaceAfter=4 * mm)
st_check_t = ParagraphStyle("checkt", fontName=KOP_B, fontSize=10.5, leading=14, textColor=white)
st_check = ParagraphStyle("check", fontName=BODY, fontSize=10, leading=15.5, textColor=white)

def kader(titel, punten):
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

doc = BaseDocTemplate(UIT, pagesize=A4, leftMargin=M, rightMargin=M,
                      topMargin=24 * mm, bottomMargin=22 * mm,
                      title="AI-geletterdheid als mensenwerk — een actieplan in vier fasen",
                      author="GVI — Global Voice Intelligence")
frame = Frame(M, 22 * mm, W - 2 * M, H - 24 * mm - 22 * mm, id="f")
doc.addPageTemplates([
    PageTemplate(id="omslag", frames=[frame], onPage=omslag),
    PageTemplate(id="binnen", frames=[frame], onPage=binnenpagina),
    PageTemplate(id="slot", frames=[frame], onPage=slotpagina),
])

S = []
S.append(NextPageTemplate("binnen"))
S.append(Spacer(1, 1))
S.append(PageBreak())

# --- p2: vooraf ---
S.append(Paragraph("Vooraf", st_kicker))
S.append(Paragraph("Verplicht sinds 2025. Maar daar gaat het niet om.", st_h1))
S.append(Paragraph("Sinds februari 2025 vraagt artikel 4 van de Europese AI Act van organisaties die AI gebruiken een passend niveau van AI-geletterdheid bij hun mensen. Veel organisaties reageren daarop met een reflex: een training inkopen, een presentielijst bewaren, klaar.", st_intro))
S.append(Paragraph("Deze whitepaper kiest een andere invalshoek. Niet omdat de verplichting onbelangrijk is — die haal je onderweg vanzelf — maar omdat het vinkje niet het doel is. AI-geletterdheid gaat over mensen die dagelijks met een nieuwe, invloedrijke technologie moeten werken: over hun vakmanschap, hun twijfels en hun oordeelsvermogen. Wie dát serieus neemt, bouwt iets dat blijft. Wie alleen het vinkje haalt, traint voor de bühne.", st_body))
S.append(Paragraph("Voor wie is dit bedoeld?", st_h2))
S.append(Paragraph("Voor bestuurders, leidinggevenden, HR- en programmaverantwoordelijken bij MKB-bedrijven en publieke of maatschappelijke organisaties. Je hoeft geen techneut te zijn — juist niet. De rode draad van dit stuk: <b>elke invoering van nieuwe technologie is mensenwerk en verandermanagement, vaak meer dan techniek.</b>", st_body))
S.append(statement("AI-geletterdheid is geen cursus die je afvinkt, maar een vermogen dat je organisatie opbouwt: begrijpen, kunnen, en durven begrenzen."))
S.append(PageBreak())

# --- p3: wat is het (breed) ---
S.append(Paragraph("Begrip", st_kicker))
S.append(Paragraph("Wat AI-geletterdheid wél is", st_h1))
S.append(Paragraph("AI-geletterdheid wordt vaak versmald tot knoppenkennis: kunnen prompten, de juiste tool kennen. Maar geletterdheid is breder. Het omvat vier lagen die samen bepalen of iemand verantwoord met AI kan werken:", st_body))
S.append(Paragraph("<b>1. Begrijpen</b> — op basisniveau weten hoe AI werkt, waar het sterk in is en waar het systematisch faalt. Wie weet dat een taalmodel overtuigend kan verzinnen, leest de uitkomst anders.", st_body))
S.append(Paragraph("<b>2. Toepassen</b> — AI inzetten in het eigen werk, op een manier die tijd oplevert zonder kwaliteit te kosten. Dit is per rol verschillend: een planner heeft niets aan de voorbeelden van een communicatieadviseur.", st_body))
S.append(Paragraph("<b>3. Wegen</b> — de sociale en ethische kant: welke gegevens deel je, wie raakt de uitkomst, kun je uitleggen wat er gebeurt? Hier hoort ook het besef dat technologie niet neutraal is: elke tool draagt keuzes en waarden in zich en stuurt gedrag.", st_body))
S.append(Paragraph("<b>4. Begrenzen</b> — misschien wel de meest onderschatte laag: weten wanneer je AI níet gebruikt. Technologie is niet onvermijdelijk; het blijft een keuze wat je inzet, waarvoor, en wat je bewust laat.", st_body))
S.append(Paragraph("Niet iedereen hoeft alles", st_h2))
S.append(Paragraph("Het gewenste niveau verschilt per rol. Wie AI-systemen inkoopt of erover beslist, moet dieper begrijpen wat er onder de motorkap gebeurt en welke risico's er zijn. Wie er dagelijks mee werkt, heeft vooral laag 2 en 4 nodig. En iedereen heeft een gedeelde basis nodig om het gesprek te kunnen voeren. Begin dus niet met één training voor iedereen, maar met de vraag: wie moet wat kunnen?", st_body))
S.append(PageBreak())

# --- p4: waarom losse training niet werkt ---
S.append(Paragraph("De valkuil", st_kicker))
S.append(Paragraph("Waarom één training niet beklijft", st_h1))
S.append(Paragraph("Het patroon is herkenbaar: een inspirerende workshop, enthousiaste reacties, en drie weken later is alles zoals het was. Dat ligt zelden aan de training en bijna altijd aan wat eromheen ontbreekt.", st_body))
S.append(Paragraph("<b>Kennis zonder toepassing vervliegt.</b> Wat je niet binnen twee weken in je eigen werk gebruikt, verdwijnt. Trainen met vergezochte demo-voorbeelden versnelt dat vergeten alleen maar.", st_body))
S.append(Paragraph("<b>Gedrag volgt de omgeving, niet de cursus.</b> Als er na de training geen afspraken zijn over wat mag en niet mag, valt iedereen terug op eigen inschattingen — of op stilte. En als de leiding zelf zichtbaar anders omgaat met AI dan de training voorschreef, wint het voorbeeld altijd van de lesstof.", st_body))
S.append(Paragraph("<b>Zorgen verdwijnen niet door ze te negeren.</b> In elk team leven vragen over banen, kwaliteit en verantwoordelijkheid. Een training die daar geen ruimte voor maakt, leert mensen vooral om hun twijfels voor zich te houden. Terwijl juist die twijfels risicosignalering zijn van de mensen die het werk het beste kennen — wie zich veilig voelt, leert sneller én meldt eerder wat er misgaat.", st_body))
S.append(Paragraph("<b>Iedereen start met een andere rugzak.</b> De één experimenteert thuis al maanden, de ander heeft vooral frustratie of onzekerheid opgebouwd. Eén uniform programma doet alsof die verschillen niet bestaan — en verliest daarmee beide groepen.", st_body))
S.append(statement("Een losse training is een prima begin. Het wordt pas een probleem als het ook het einde is."))
S.append(PageBreak())

# --- p5: het plan overzicht ---
S.append(Paragraph("Het actieplan", st_kicker))
S.append(Paragraph("Vier fasen, in het ritme van je organisatie", st_h1))
S.append(Paragraph("AI-geletterdheid bouw je op zoals elke duurzame verandering: stap voor stap, met de mensen zelf, en met de leiding zichtbaar voorop. De vier fasen hieronder vormen een doorlopend ritme — geen project met een einddatum, wel met heldere mijlpalen per fase.", st_intro))
fasen = [
    ("Fase 1 · Bewustwording & gesprek", "Begrip en draagvlak: wat is AI, wat gebeurt er al bij ons, en wat vinden we daarvan?"),
    ("Fase 2 · Leren in het eigen werk", "Rolgericht oefenen op echte taken — vaardigheid en vertrouwen opbouwen."),
    ("Fase 3 · Afspraken & voorleven", "Korte werkbare kaders, en een leiding die het goede voorbeeld geeft."),
    ("Fase 4 · Borgen & vernieuwen", "Onderhoud, meten wat werkt, en ruimte voor nieuwe toepassingen — aantoonbaar op orde."),
]
for kop, tekst in fasen:
    S.append(Paragraph(f'<font color="#E6349C"><b>{kop}</b></font> — {tekst}', st_body))
S.append(Spacer(1, 3 * mm))
S.append(Paragraph("De volgorde is bewust. Wie bij fase 2 begint (meteen trainen), slaat het gesprek over dat draagvlak bouwt. Wie bij fase 3 begint (eerst beleid), krijgt regels zonder praktijk. Elke fase sluit af met iets tastbaars — een gedeeld beeld, geoefende vaardigheden, één A4 met afspraken, een leerritme — zodat je nooit maanden werkt zonder resultaat.", st_body))
S.append(PageBreak())

# --- p6: fase 1 ---
S.append(Paragraph("Fase 1", st_kicker))
S.append(Paragraph("Bewustwording & gesprek", st_h1))
S.append(Paragraph("Het doel van deze fase is niet dat iedereen AI snapt, maar dat het gesprek erover normaal wordt. Wat gebruiken we al — ook onder de radar? Waar zijn we nieuwsgierig naar, waar zijn we bang voor? In dit gesprek komt alles boven wat je later nodig hebt: de kansen, de risico's én de zorgen.", st_body))
S.append(Paragraph("Werkvormen die passen: een interactieve kick-off met echte voorbeelden uit de eigen organisatie, korte demonstraties waarin ook de missers van AI te zien zijn, en gesprekken per team over wat AI met het vak zou kunnen doen. Belangrijk: geen verkooppraatje. Laat zien wat AI kan én waar het faalt — geloofwaardigheid is het fundament onder alles wat volgt.", st_body))
S.append(Paragraph("De menselijke praktijk", st_h2))
S.append(Paragraph("Let in deze fase vooral op de stille collega's. Enthousiastelingen melden zich vanzelf; de aarzelaars dragen vaak de scherpste inzichten over kwaliteit en risico. Vraag expliciet naar hun ervaringen en zorgen — en doe er zichtbaar iets mee.", st_body))
S.append(kader("Mijlpaal · na fase 1", [
    "Er ligt een eerlijk beeld van het huidige AI-gebruik, ook het informele.",
    "Zorgen en vragen van medewerkers zijn opgehaald en vastgelegd.",
    "Teams kunnen in gewone taal uitleggen wat AI wel en niet kan.",
    "Er is draagvlak om te gaan oefenen — óók bij de leiding.",
]))
S.append(PageBreak())

# --- p7: fase 2 ---
S.append(Paragraph("Fase 2", st_kicker))
S.append(Paragraph("Leren in het eigen werk", st_h1))
S.append(Paragraph("Nu wordt het praktisch: teams leren AI gebruiken op hun eigen taken. Niet in een generieke cursus, maar rolgericht — beleidsmedewerkers oefenen op beleidsstukken, planners op planningen, leidinggevenden op sturingsvragen. Het materiaal komt uit de eigen praktijk; wat je vandaag leert, gebruik je morgen.", st_body))
S.append(Paragraph("Zorg voor een veilige oefenomgeving: duidelijke afspraken over welke gegevens wél en niet in tools mogen (vooruitlopend op fase 3), ruimte om fouten te maken, en aandacht voor verschillen in tempo. Werk modelonafhankelijk: het gaat om het denkwerk — formuleren, beoordelen, verbeteren — niet om de knoppen van één leverancier. Wie bij één tool leert, is geletterd tot de licentie afloopt.", st_body))
S.append(Paragraph("De menselijke praktijk", st_h2))
S.append(Paragraph("Verwacht geen gelijkmatige groei. Sommige collega's versnellen direct, anderen hebben een tweede of derde sessie nodig. Plan daarom korte herhaalmomenten in plaats van één grote klap. En vier de kleine successen: één collega die een vervelende taak heeft gehalveerd, overtuigt meer dan tien slides.", st_body))
S.append(kader("Mijlpaal · na fase 2", [
    "Elk team heeft geoefend op eigen werkvoorbeelden.",
    "Medewerkers weten wanneer ze AI-uitkomsten kunnen vertrouwen — en wanneer niet.",
    "Er zijn per team twee of drie toepassingen die aantoonbaar tijd of kwaliteit opleveren.",
    "Verschillen in tempo zijn zichtbaar en krijgen ruimte.",
]))
S.append(PageBreak())

# --- p8: fase 3 ---
S.append(Paragraph("Fase 3", st_kicker))
S.append(Paragraph("Afspraken & voorleven", st_h1))
S.append(Paragraph("Zodra teams echt met AI werken, ontstaat de behoefte aan duidelijkheid: wat mag, wat mag niet, wie is waarvoor verantwoordelijk? Maak die afspraken kort en begrijpelijk — één A4 dat iedereen kent, verslaat een beleidsdocument dat niemand leest. Kern: welke gegevens blijven buiten AI-tools, waar blijft een mens aantoonbaar aan het stuur, en hoe melden we twijfels of incidenten?", st_body))
S.append(Paragraph("En dan het deel dat in geen enkel beleidsstuk past: <b>voorleven</b>. Teams kijken niet naar wat er is opgeschreven, maar naar wat hun leidinggevenden doen. Een directeur die zelf transparant is over waar hij AI voor gebruikt — en waar bewust niet — zet meer neer dan drie richtlijnen. Wat je normaliseert, wordt de norm.", st_body))
S.append(Paragraph("De menselijke praktijk", st_h2))
S.append(Paragraph("Betrek de teams bij het opstellen van de afspraken; regels die mensen zelf hebben helpen formuleren, worden nageleefd. En houd de toon volwassen: kaders zijn er om veilig te kunnen werken, niet om te betuttelen.", st_body))
S.append(kader("Mijlpaal · na fase 3", [
    "Er ligt één A4 met werkbare afspraken — door teams mede opgesteld.",
    "Menselijke controle is belegd op de plekken waar het ertoe doet.",
    "Leidinggevenden leven het gebruik zichtbaar voor.",
    "Er is een laagdrempelige plek voor vragen, twijfels en incidenten.",
]))
S.append(PageBreak())

# --- p9: fase 4 ---
S.append(Paragraph("Fase 4", st_kicker))
S.append(Paragraph("Borgen & vernieuwen", st_h1))
S.append(Paragraph("Geletterdheid slijt. Tools veranderen, collega's stromen in en uit, en wat vorig jaar veilig gebruik was, is dat dit jaar misschien niet meer. Daarom eindigt het actieplan niet — het gaat over in een licht ritme: periodiek opfrissen, nieuwe toepassingen samen wegen, en nieuwe collega's vanaf dag één meenemen.", st_body))
S.append(Paragraph("Meet daarbij wat er echt toe doet. Niet alleen hoeveel mensen een training volgden, maar of het werk beter wordt: minder tijd aan routinetaken, minder incidenten met gegevens, meer collega's die durven te melden waar ze twijfelen. In deze fase wordt de AI Act-verplichting vanzelf aantoonbaar: je kunt laten zien wie wat heeft geleerd, welke afspraken er gelden en hoe je bijstuurt.", st_body))
S.append(Paragraph("De menselijke praktijk", st_h2))
S.append(Paragraph("Geef de geletterdheid een eigenaar — iemand die het ritme bewaakt, signalen ophaalt en het onderwerp op de agenda houdt. Zonder eigenaar verwatert elk programma; niet uit onwil, maar uit drukte. En pas op met 'weg-integreren': als AI-geletterdheid overal een beetje belegd is, is niemand er verantwoordelijk voor.", st_body))
S.append(kader("Mijlpaal · doorlopend", [
    "Er is een eigenaar en een licht leerritme (opfrissen, nieuwe toepassingen wegen).",
    "Nieuwe collega's worden vanaf de start meegenomen.",
    "Je meet effect op het werk, niet alleen deelname aan trainingen.",
    "De AI Act-verplichting is hiermee aantoonbaar ingevuld — als bijvangst.",
]))
S.append(PageBreak())

# --- p10: rol van de leiding + wat levert het op ---
S.append(Paragraph("Leiderschap", st_kicker))
S.append(Paragraph("De rol van de leiding — en wat het oplevert", st_h1))
S.append(Paragraph("AI-geletterdheid is niet weg te delegeren naar HR of IT. De leiding bepaalt of het gesprek veilig is, of er tijd is om te leren, en wat er wordt voorgeleefd. Concreet betekent dat: zelf meedoen aan de basissessies, transparant zijn over eigen AI-gebruik, en zorgen serieus behandelen in plaats van wegwuiven.", st_body))
S.append(Paragraph("Wat een geletterde organisatie terugziet", st_h2))
S.append(Paragraph("<b>Rust en tempo tegelijk</b> — geen paniekreacties op elk nieuw AI-bericht, maar gewogen keuzes. <b>Betere besluiten</b> — mensen die AI-uitkomsten op waarde schatten in plaats van blind overnemen of blind wantrouwen. <b>Tijd voor het echte werk</b> — routinetaken worden lichter, vakmanschap houdt de regie. <b>Minder risico</b> — gegevens blijven waar ze horen, en twijfels worden gemeld voordat het incidenten worden. <b>Aantoonbare compliance</b> — als resultaat van goed werk, niet als doel op zich.", st_body))
S.append(statement("Regie op AI, meer tijd voor het werk dat er echt toe doet — dat is de opbrengst van geletterdheid met menselijke maat."))
S.append(Paragraph("Verder lezen", st_h2))
S.append(Paragraph('Over de AI Act-verplichting en praktische startpunten: het overzichtsartikel "Wat je moet weten over AI-geletterdheid" op digitaleoverheid.nl. Voor de bredere, pedagogische kijk op digitale geletterdheid — technologie is niet neutraal en niet onvermijdelijk — de wegwijzer digitale geletterdheid van Kennisnet.', st_body))
S.append(NextPageTemplate("slot"))
S.append(PageBreak())
S.append(Spacer(1, 1))

doc.build(S)
print("PDF gemaakt:", UIT)
