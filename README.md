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
├── assets/                ← logo, favicon, og-afbeelding
├── sitemap.xml            ← gegenereerd
├── robots.txt · llms.txt  ← voor zoekmachines en AI-agents
└── 404.html
```

**Tekst aanpassen:** open het juiste bestand in `src/pages/`, wijzig de tekst, en laat Claude (of jijzelf via Terminal) dit draaien vanuit de map `gvi-website`:

```
python3 src/build.py
```

**Lokaal bekijken:** `python3 -m http.server 8080` vanuit de map `gvi-website`, dan http://localhost:8080 openen. (Direct dubbelklikken op index.html werkt niet goed — de links beginnen met `/`.)

## Formulieren (actief via Web3Forms ✓)

Contactformulier, nieuwsbrief-inschrijving (2×) en download-aanvragen versturen allemaal via **Web3Forms** naar `irisfickeryounge@gmail.com`. De access key staat in `js/main.js` (`WEB3FORMS_KEY`). Getest en werkend op 4 juli 2026.

**Let op:** in je Web3Forms-account staat `localhost` als domein. Zet daar bij livegang `globalvoiceintelligence.com` bij (of haal de domeinbeperking weg), anders weigert Web3Forms inzendingen vanaf het echte domein.

- Nieuwsbrief-inschrijvingen en download-aanvragen komen als e-mail binnen; zolang er geen mailtool (MailerLite/Brevo) is gekoppeld, beheer je de lijst handmatig en mail je download-links zelf.

### Automatische ontvangstbevestiging (Google Apps Script ✓)

Wie een formulier invult krijgt binnen ± 5 minuten een warme ontvangstbevestiging, verstuurd vanaf Iris' eigen Gmail — géén betaald Web3Forms Pro nodig. Het script staat in `src/gmail-autobevestiging.gs` en draait op https://script.google.com (project "GVI autobevestiging", tijdgestuurde trigger elke 5 minuten). Het herkent de formulier-mails aan hun onderwerp, haalt het adres van de inzender uit de Reply-To/het email-veld, en stuurt per formuliertype (contact / nieuwsbrief / download) een eigen tekst. Alleen een ontvangstbevestiging — nooit een inhoudelijk antwoord. Beantwoorde mails krijgen het Gmail-label `GVI-bevestigd`.

Tekst van de bevestigingen aanpassen: wijzig `src/gmail-autobevestiging.gs` én plak de nieuwe versie in de editor op script.google.com (het bestand hier is de bron, het script daar is wat draait).

## Live zetten (als je zover bent)

1. Maak een gratis account op **Cloudflare Pages** of **Netlify**.
2. Sleep de map `gvi-website` in het upload-venster (of koppel een GitHub-repo).
3. Koppel het domein `globalvoiceintelligence.com` via de DNS-instellingen bij TransIP.

## Conversie-sporen (iteratie 5 jul 2026)

Drie drempelniveaus met elk een eigen knopstijl — bewust géén zes identieke roze pillen:
- **Fuchsia pil** (`knop-primair`): alléén de betaalde instap — AI Regie Scan (€ 1.500 aanloopprijs; bedrag aanpassen in `src/pages/01-home.html` en `02-ai-regie-scan.html`).
- **Nachtpaars/rustig** (`knop-donker`): "Plan een verkennend gesprek" en formulier-verzendknoppen.
- **Wit pilletje** (`knop-licht`): gratis downloads en nieuwsbrief.

**Whitepaper**: `downloads/gvi-whitepaper-ai-met-menselijke-maat.pdf` (11 pag., huisstijl) — opnieuw genereren na tekstwijzigingen: `python3 src/maak_whitepaper.py`. Download loopt via e-mailcapture (modal) en start daarna direct; de aanvraag komt óók als lead-mail binnen.

**Artikel-template** voor de essayhub: `/kennis/voorbeeld-artikel/` (noindex, niet in sitemap) — kopieer `src/pages/15-kennis-artikel-template.html` voor elk nieuw artikel.

## Voorbereid voor fase 2 (plug-in-plekken)

- **Agenda-boeking (Cal.com):** commentaar-plek in `src/pages/12-contact.html` (zijkolom).
- **Lead magnet + nieuwsbrief (MailerLite/Brevo):** blok toevoegen op `/kennis/` zodra er een document + account is.
- **Betaallink (Mollie):** knop op de Regie Scan-pagina zodra prijs bekend is.
- **Analytics (Plausible):** uitgecommentarieerd in `src/template.html` — pas activeren als gewenst.

## Nog aan te leveren (openstaand voor Iris)

1. Definitieve biotekst + portretfoto (Over GVI + founder-blok home)
2. LinkedIn-URL (contactpagina)
3. Zakelijk e-mailadres (vervangt gmail — staat in `src/template.html`, `src/pages/12-contact.html`, `13-privacy.html`, `js/main.js`, `llms.txt`)
4. Web3Forms access key (zie boven)
5. Prijsrichting AI Regie Scan
6. Privacytekst juridisch laten nalopen
7. Hosting + domeinkoppeling
