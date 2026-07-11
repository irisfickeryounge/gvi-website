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
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
PAGES = SRC / "pages"
DOMEIN = "https://www.globalvoiceintelligence.com"

# Illustratie-varianten (afgewisseld per pagina, allemaal fuchsia/paars op nachtpaars)
# Golven — subtiel, voor footer en enkele hero's
ART_SUBTIEL = """<svg viewBox="0 0 1440 400" preserveAspectRatio="xMidYMax slice" style="position:absolute;inset:0;width:100%;height:100%;opacity:.5" aria-hidden="true" focusable="false"><defs><linearGradient id="fgrad" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#FF3DA6" stop-opacity="0"/><stop offset=".6" stop-color="#FF3DA6" stop-opacity=".35"/><stop offset="1" stop-color="#D91C87" stop-opacity=".55"/></linearGradient></defs><g fill="none" stroke="url(#fgrad)" stroke-width="1.5"><path d="M-50 320 C 300 260, 600 380, 900 300 S 1300 240, 1500 300"/><path d="M-50 345 C 320 285, 620 400, 920 320 S 1320 260, 1500 325"/><path d="M-50 370 C 340 315, 640 420, 940 345 S 1340 285, 1500 350"/></g></svg>"""

# Stroom — spraakgolf die overgaat in vloeiende stromen ("voice" als vormtaal)
ART_STROOM = """<svg viewBox="0 0 1440 400" preserveAspectRatio="xMidYMid slice" style="position:absolute;inset:0;width:100%;height:100%;opacity:.7" aria-hidden="true" focusable="false"><defs><linearGradient id="sgrad" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#9F92C8" stop-opacity=".5"/><stop offset=".5" stop-color="#FF3DA6" stop-opacity=".3"/><stop offset="1" stop-color="#D91C87" stop-opacity=".5"/></linearGradient></defs><g stroke="#B9A9E0" stroke-opacity=".55" stroke-width="3" stroke-linecap="round"><line x1="980" y1="190" x2="980" y2="210"/><line x1="1000" y1="175" x2="1000" y2="225"/><line x1="1020" y1="155" x2="1020" y2="245"/><line x1="1040" y1="180" x2="1040" y2="220"/><line x1="1060" y1="165" x2="1060" y2="235"/><line x1="1080" y1="185" x2="1080" y2="215"/><line x1="1100" y1="170" x2="1100" y2="230"/><line x1="1120" y1="192" x2="1120" y2="208"/></g><g fill="none" stroke="url(#sgrad)" stroke-width="1.6"><path d="M1130 200 C 1230 190, 1300 230, 1460 205"/><path d="M1130 200 C 1240 220, 1320 170, 1460 185" stroke-opacity=".7"/><path d="M1130 200 C 1250 180, 1340 260, 1460 235" stroke-opacity=".5"/></g><path d="M-50 360 C 420 320, 920 395, 1500 345" fill="none" stroke="#FF3DA6" stroke-opacity=".2" stroke-width="1.5"/></svg>"""

# Sterren — vierpuntige sterren uit het logo, gestrooid
ART_STER = """<svg viewBox="0 0 1440 400" preserveAspectRatio="xMidYMid slice" style="position:absolute;inset:0;width:100%;height:100%;opacity:.65" aria-hidden="true" focusable="false"><g fill="#FF3DA6"><path d="M1180 90 l7 -28 l7 28 l28 7 l-28 7 l-7 28 l-7 -28 l-28 -7 Z" fill-opacity=".55"/><path d="M1330 230 l5 -20 l5 20 l20 5 l-20 5 l-5 20 l-5 -20 l-20 -5 Z" fill-opacity=".4"/><path d="M1060 280 l4 -16 l4 16 l16 4 l-16 4 l-4 16 l-4 -16 l-16 -4 Z" fill-opacity=".35"/></g><g fill="#FF9AD1" fill-opacity=".6"><circle cx="1250" cy="180" r="2.5"/><circle cx="1120" cy="140" r="2"/><circle cx="1390" cy="120" r="2"/><circle cx="1200" cy="320" r="2"/></g><path d="M-50 370 C 420 330, 920 395, 1500 350" fill="none" stroke="#FF3DA6" stroke-opacity=".2" stroke-width="1.5"/></svg>"""


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


def bouw():
    template = (SRC / "template.html").read_text(encoding="utf-8")
    paden = []
    for frag in sorted(PAGES.glob("*.html")):
        meta, inhoud = lees_fragment(frag)
        pad = meta["path"]

        html = template
        html = html.replace("{{TITLE}}", meta["title"])
        html = html.replace("{{DESC}}", meta["desc"])
        html = html.replace("{{PATH}}", pad)
        html = html.replace("{{JSONLD}}", meta.get("jsonld", ""))
        html = html.replace("{{CONTENT}}", inhoud)
        html = html.replace("{{ART_SUBTIEL}}", ART_SUBTIEL)
        html = html.replace("{{ART_STROOM}}", ART_STROOM)
        html = html.replace("{{ART_STER}}", ART_STER)
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
    for pad in sorted(paden, key=lambda p: (p != "/", p)):
        regels.append(f"  <url><loc>{DOMEIN}{pad}</loc></url>")
    regels.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(regels) + "\n", encoding="utf-8")
    print(f"  ✓ sitemap.xml ({len(paden)} url's)")


if __name__ == "__main__":
    bouw()
