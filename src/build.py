#!/usr/bin/env python3
"""Bouwt de statische GVI-site: src/template.html + src/pages/*.html -> site-root.

Gebruik:  python3 src/build.py   (vanuit de map gvi-website)

Per pagina staat de metadata bovenaan het fragment als HTML-commentaar:
<!--META
title: ...
desc: ...
path: /ai-regie-scan/
-->
De rest van het fragment is de inhoud van <main>.
"""
import html as html_lib
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
PAGES = SRC / "pages"
DOMEIN = "https://www.globalvoiceintelligence.com"
OPERATIONS_PADEN = {
    "/ai-regie-scan/",
    "/ai-workflow-pilot/",
    "/ai-strategie-roadmap/",
}

# Illustratie-varianten in Iris Glow: lila, fuchsia en koraal op diep irispaars.
# Golven — subtiel, voor footer en enkele hero's
ART_SUBTIEL = """<svg viewBox="0 0 1440 400" preserveAspectRatio="xMidYMax slice" style="position:absolute;inset:0;width:100%;height:100%;opacity:.5" aria-hidden="true" focusable="false"><defs><linearGradient id="fgrad" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#A887FF" stop-opacity="0"/><stop offset=".52" stop-color="#FF4FA3" stop-opacity=".38"/><stop offset="1" stop-color="#FF8A5B" stop-opacity=".6"/></linearGradient></defs><g fill="none" stroke="url(#fgrad)" stroke-width="1.6"><path d="M-50 320 C 300 260, 600 380, 900 300 S 1300 240, 1500 300"/><path d="M-50 345 C 320 285, 620 400, 920 320 S 1320 260, 1500 325"/><path d="M-50 370 C 340 315, 640 420, 940 345 S 1340 285, 1500 350"/></g></svg>"""


class HoofdtekstParser(HTMLParser):
    """Zet de zichtbare hoofdinhoud van een gebouwde pagina om in rustige tekst."""

    OVER_SLAAN = {"script", "style", "svg", "dialog", "form", "noscript"}
    BLOKKEN = {
        "section", "article", "div", "p", "blockquote", "details", "summary",
        "header", "footer", "figure", "figcaption", "ol", "ul", "dl", "dt", "dd",
    }

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.in_main = False
        self.skip_diepte = 0
        self.regels = []
        self.huidig = ""

    def breek(self, voorvoegsel=""):
        regel = re.sub(r"\s+", " ", self.huidig).strip()
        if regel:
            self.regels.append(regel)
        self.huidig = voorvoegsel

    def handle_starttag(self, tag, attrs):
        if tag == "main":
            self.in_main = True
            return
        if not self.in_main:
            return
        if self.skip_diepte:
            if tag in self.OVER_SLAAN:
                self.skip_diepte += 1
            return
        if tag in self.OVER_SLAAN:
            self.skip_diepte = 1
        elif tag in {"h1", "h2", "h3", "h4"}:
            self.breek("#" * int(tag[1]) + " ")
        elif tag == "li":
            self.breek("- ")
        elif tag == "br":
            self.breek()
        elif tag in self.BLOKKEN:
            self.breek()

    def handle_endtag(self, tag):
        if tag == "main":
            self.breek()
            self.in_main = False
            return
        if not self.in_main:
            return
        if self.skip_diepte:
            if tag in self.OVER_SLAAN:
                self.skip_diepte -= 1
            return
        if tag in {"h1", "h2", "h3", "h4", "li"} or tag in self.BLOKKEN:
            self.breek()

    def handle_data(self, data):
        if not self.in_main or self.skip_diepte:
            return
        tekst = re.sub(r"\s+", " ", data).strip()
        if not tekst:
            return
        if self.huidig and not self.huidig.endswith(" ") and not tekst.startswith(tuple(".,;:!?")):
            self.huidig += " "
        self.huidig += tekst

    def tekst(self):
        self.breek()
        schoon = []
        vorige_leeg = False
        for regel in self.regels:
            if regel:
                schoon.append(regel)
                vorige_leeg = False
            elif not vorige_leeg:
                schoon.append("")
                vorige_leeg = True
        return "\n\n".join(schoon).strip()


def doelpad_voor_route(pad: str) -> Path:
    if pad == "/":
        return ROOT / "index.html"
    return ROOT / pad.strip("/") / "index.html"


def maak_llms_full(paden):
    """Genereer de volledige publieke sitetekst in de volgorde van de sitemap."""
    delen = [
        "# GVI — volledige sitetekst",
        "> Automatisch gegenereerd uit dezelfde bronpagina's als de website. "
        "Voor het beknopte, gecontroleerde overzicht: https://www.globalvoiceintelligence.com/llms.txt",
    ]
    for pad in paden:
        bron = doelpad_voor_route(pad).read_text(encoding="utf-8")
        titel_match = re.search(r"<title>(.*?)</title>", bron, re.S)
        titel = html_lib.unescape(titel_match.group(1).strip()) if titel_match else pad
        parser = HoofdtekstParser()
        parser.feed(bron)
        hoofdtekst = parser.tekst()
        if not hoofdtekst:
            sys.exit(f"FOUT: geen hoofdtekst gevonden voor {pad}")
        delen.extend([
            "---",
            f"## Pagina: {titel}",
            f"URL: {DOMEIN}{pad}",
            hoofdtekst,
        ])
    (ROOT / "llms-full.txt").write_text("\n\n".join(delen) + "\n", encoding="utf-8")
    print(f"  ✓ llms-full.txt ({len(paden)} pagina's)")

def lees_fragment(pad: Path):
    tekst = pad.read_text(encoding="utf-8")
    m = re.search(r"<!--META(.*?)-->\s*", tekst, re.S)
    if not m:
        sys.exit(f"FOUT: geen META-blok in {pad.name}")
    meta = {}
    for regel in m.group(1).strip().splitlines():
        k, _, v = regel.partition(":")
        meta[k.strip()] = v.strip()
    inhoud = tekst[m.end():]
    for veld in ("title", "desc", "path"):
        if veld not in meta:
            sys.exit(f"FOUT: '{veld}' ontbreekt in META van {pad.name}")
    return meta, inhoud


def namespace_svg_ids(html: str) -> str:
    """Maak SVG-id's uniek per inline SVG.

    Dezelfde illustratie kan meerdere keren op één pagina staan. Zonder namespace
    levert dat dubbele id-attributen op en kan een url(#gradient)-verwijzing naar
    de verkeerde SVG wijzen.
    """
    teller = 0

    def vervang_svg(match):
        nonlocal teller
        teller += 1
        svg = match.group(0)
        for oud_id in re.findall(r'\bid="([^"]+)"', svg):
            nieuw_id = f"{oud_id}-{teller}"
            svg = re.sub(rf'\bid="{re.escape(oud_id)}"', f'id="{nieuw_id}"', svg)
            svg = svg.replace(f"url(#{oud_id})", f"url(#{nieuw_id})")
        return svg

    return re.sub(r"<svg\b.*?</svg>", vervang_svg, html, flags=re.S)


def bouw():
    template = (SRC / "template.html").read_text(encoding="utf-8")
    paden = []
    for frag in sorted(PAGES.glob("*.html")):
        meta, inhoud = lees_fragment(frag)
        if meta.get("build") == "nee":
            print(f"  — {frag.name:28s} (bron-template, niet publiceren)")
            continue
        pad = meta["path"]

        html = template
        html = html.replace("{{TITLE}}", html_lib.escape(meta["title"], quote=True))
        html = html.replace("{{DESC}}", html_lib.escape(meta["desc"], quote=True))
        html = html.replace("{{PATH}}", pad)
        html = html.replace("{{JSONLD}}", meta.get("jsonld", ""))
        html = html.replace("{{CONTENT}}", inhoud)
        html = html.replace("{{ART_SUBTIEL}}", ART_SUBTIEL)
        html = namespace_svg_ids(html)
        # De drie Operations-fasen vormen in de hoofdnavigatie één propositie.
        html = html.replace(
            "{{ACTOPS}}",
            ' aria-current="page"' if pad in OPERATIONS_PADEN else "",
        )
        # actieve navigatielink markeren
        html = re.sub(r"\{\{ACT:" + re.escape(pad) + r"\}\}", ' aria-current="page"', html)
        html = re.sub(r"\{\{ACT:[^}]*\}\}", "", html)

        if pad == "/":
            doel = ROOT / "index.html"
        elif pad.endswith(".html"):
            doel = ROOT / pad.lstrip("/")
        else:
            doel = ROOT / pad.strip("/") / "index.html"
        doel.parent.mkdir(parents=True, exist_ok=True)
        doel.write_text(html, encoding="utf-8")
        if not pad.endswith(".html") and meta.get("sitemap") != "nee":  # 404/templates niet in sitemap
            paden.append(pad)
        print(f"  ✓ {pad:28s} → {doel.relative_to(ROOT)}")

    # sitemap.xml
    regels = ['<?xml version="1.0" encoding="UTF-8"?>',
              '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    sitemap_paden = sorted(paden, key=lambda p: (p != "/", p))
    for pad in sitemap_paden:
        regels.append(f"  <url><loc>{DOMEIN}{pad}</loc></url>")
    regels.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(regels) + "\n", encoding="utf-8")
    print(f"  ✓ sitemap.xml ({len(paden)} url's)")
    maak_llms_full(sitemap_paden)


if __name__ == "__main__":
    bouw()
