# DTU Inside: Rejsedokumenter Scraper

Dette modul automatiserer hentning og konvertering af rejsedokumenter fra DTU Inside-portalen. Det bruger Crawl4AI til webnavigation og MarkItDown til at sikre, at alle hentede data lagres i et læsbart og struktureret format.

## Funktioner
- Asynkron Crawling: Bruger asyncio og Crawl4AI til hurtig, ikke-blokerende sidebehandling.
- Markdown-konvertering: Konverterer kompleks HTML og dokumentfragmenter til ren Markdown via MarkItDown.
- Automatiseret Regex: Bruger re-modulet til at identificere og sortere dokumenttyper såsom fakturaer, billetter eller godkendelser.

## Opsætning og installation

### 1. Miljø
Sørg for, at du er i dit Conda-miljø, og installér derefter de grundlæggende afhængigheder:
```bash
pip install crawl4ai httpx markitdown[all]
```

Kør herefter denne kommando i forbindelse med installationen af crawl4ai:
```bash
crawl4ai-setup
```

## Projektstruktur
- main.py: Hovedscriptet med AsyncWebCrawler-logikken.
- requirements.txt: Minimal liste over tredjepartspakker (crawl4ai, httpx, markitdown).
- data/: (Genereres automatisk) Indeholder de konverterede .md-rejsedokumenter.

## Bemærkning om godkendelse
DTU Inside kræver login. Denne scraper håndterer sessionen via BrowserConfig for at administrere persistente kontekster eller session-cookies.

## Anvendelse
Kør scraperen fra terminalen (husk at redigere sti-koden i Main_file.py)
```bash
# Web-scrape DTU Inside og rens data
python main.py gather

# Kombinér alle scrapede websider
python main.py combine
```
