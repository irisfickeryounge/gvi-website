# GVI-website — globalvoiceintelligence.com

Statische Nederlandstalige website voor **GVI — Global Voice Intelligence**. Geen framework, geen abonnementen: pure HTML, CSS en een klein beetje JavaScript.

## Hoe de site in elkaar zit

```
gvi-website/
├── src/
│   ├── template.html      ← header, navigatie en footer (één keer aanpassen = overal aangepast)
│   ├── build.py           ← bouwt de site: template + fragmenten → pagina's
│   └── pages/*.html       ← de TEKST van elke pagina (hier pas je copy aan)
├── index.html             ← gegenereerd — niet met de hand bewerken
├── ai-regie-scan/ …       ← gegenereerd — niet met de hand bewerken
├── css/style.css          ← design system (kleuren, typografie, componenten)
├── js/main.js             ← menu, animaties, contactformulier
├── assets/brand/          ← vergrendelde V4-logo's en Iris-ster
├── assets/favicons/       ← officiële V4-faviconset en webmanifest
├── assets/fonts/          ← lokale Newsreader- en Manrope-webfonts
├── assets/                ← portretten en social/OG-afbeelding
├── sitemap.xml            ← gegenereerd
├── robots.txt · llms.txt · llms-full.txt ← voor zoekmachines en AI-assistenten
└── 404.html
```

**Tekst aanpassen:** open het juiste bestand in `src/pages/`, wijzig de tekst, en laat Claude (of jijzelf via Terminal) dit draaien vanuit de map `gvi-website`:

```
python3 src/build.py
```

De build genereert naast de HTML en sitemap ook automatisch `llms-full.txt` uit de publieke pagina's. Draai de build daarom na iedere inhoudelijke wijziging; `llms.txt` blijft het handmatig gecontroleerde, beknopte overzicht.

**Lokaal bekijken:** `python3 -m http.server 8766 --bind 127.0.0.1` vanuit deze map, daarna [http://127.0.0.1:8766/](http://127.0.0.1:8766/) openen. Direct dubbelklikken op `index.html` werkt niet goed omdat de links bij `/` beginnen.

## Merksysteem V4

De publieke merkassets staan versioneerbaar in `assets/brand/`, `assets/favicons/` en `assets/fonts/`; de webtoepassing staat in `css/style.css`. De vaste merkhiërarchie is **AI met grip en regie.** gevolgd door **Beslissen blijft mensenwerk.** De ondersteunende begrippen zijn **onderscheidingsvermogen, creativiteit en oordeel**.

## Formulieren (actief via Web3Forms ✓)

Contactformulier, nieuwsbrief-inschrijving en download-aanvragen zijn in `js/main.js` ingericht voor **Web3Forms**. De access key staat daar als `WEB3FORMS_KEY`. Een geslaagde lokale build bewijst niet dat productie-inzendingen aankomen; test dit na iedere wijziging aan domeininstellingen of formulierconfiguratie end-to-end op de live site.

**Let op:** in je Web3Forms-account staat `localhost` als domein. Zet daar bij livegang `globalvoiceintelligence.com` bij (of haal de domeinbeperking weg), anders weigert Web3Forms inzendingen vanaf het echte domein.

- Na een geslaagde downloadaanvraag start het PDF-bestand direct. Nieuwsbriefadressen worden handmatig beheerd zolang er geen mailtool is gekoppeld.

### Automatische ontvangstbevestiging (Google Apps Script — verificatie open)

Het script voor een warme ontvangstbevestiging staat voorbereid in `src/gmail-autobevestiging.gs`. De actuele OAuth-autorisatie, trigger en een echte testmail moeten nog aantoonbaar worden geverifieerd voordat de website mag beloven dat iedere inzender automatisch een bevestiging ontvangt. Het script herkent de formulier-mails aan hun onderwerp, haalt het adres van de inzender uit de Reply-To/het email-veld, en stuurt per formuliertype (contact / nieuwsbrief / download) een eigen tekst. Alleen een ontvangstbevestiging — nooit een inhoudelijk antwoord. Beantwoorde mails krijgen het Gmail-label `GVI-bevestigd`.

Tekst van de bevestigingen aanpassen: wijzig `src/gmail-autobevestiging.gs` én plak de nieuwe versie in de editor op script.google.com (het bestand hier is de bron, het script daar is wat draait).

## Publiceren

De bron en de lokale preview zijn niet automatisch de live website. Bouw eerst met `python3 src/build.py`, voer de validaties uit en publiceer uitsluitend na Iris' expliciete akkoord.

Na een push naar `main` publiceert `.github/workflows/deploy-pages.yml` de statische repository via GitHubs officiële Pages-actions. Controleer na iedere livegang dat de workflow is geslaagd én dat het productiedomein de nieuwe inhoud, downloads en formulierflow werkelijk serveert.

## Conversiehiërarchie (V4, 22 augustus 2026)

Drie drempelniveaus met elk een eigen knopstijl — bewust géén zes identieke roze pillen:
- **Koraal-roze-lila gradient** (`knop-primair`): de belangrijkste eerste stap.
- **Iris-lila** (`knop-iris`): de onderzoekende of testende tweede stap.
- **Nachtpaars/rustig** (`knop-donker`): "Plan een verkennend gesprek" en formulier-verzendknoppen.
- **Wit pilletje** (`knop-licht`): downloads en nieuwsbrief.

**Whitepaper**: `downloads/gvi-whitepaper-ai-met-menselijke-maat.pdf` (11 pag., huisstijl) — opnieuw genereren na tekstwijzigingen: `python3 src/maak_whitepaper.py`. Download loopt via e-mailcapture (modal) en start daarna direct; de aanvraag komt óók als lead-mail binnen.

**Artikel-template** voor de essayhub: `src/pages/15-kennis-artikel-template.html` — dit bronbestand wordt bewust niet gebouwd of gepubliceerd. Kopieer het voor een nieuw artikel en verwijder in de kopie `build: nee` zodra de tekst af is.

## Voorbereid voor fase 2 (plug-in-plekken)

- **Agenda-boeking (Cal.com):** commentaar-plek in `src/pages/12-contact.html` (zijkolom).
- **Lead magnet + nieuwsbrief (MailerLite/Brevo):** blok toevoegen op `/kennis/` zodra er een document + account is.
- **Betaallink (Mollie):** knop op de Operations Sprint-pagina zodra prijs en scope zijn gevalideerd.
- **Analytics (Plausible):** uitgecommentarieerd in `src/template.html` — pas activeren als gewenst.

## Openstaande beslissingen

1. prijs en definitieve leveringsscope van de AI Operations Sprint en het AI Operations Partnership;
2. productieformulieren en downloadflow end-to-end testen;
3. privacytekst juridisch laten nalopen;
4. whitepapers in een volgende ronde visueel naar V4 brengen;
5. publicatie van deze lokale rebuild afzonderlijk goedkeuren.
