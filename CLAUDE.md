# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a collection of automation tools developed for **DTU AØR** (Administration, Økonomi og Ressourcer). It contains three independent projects:

| Project | Purpose |
|---|---|
| `Rejsedokument_chatbot/` | Scrapes DTU Inside travel policy pages → produces a master `.md` training file for a chatbot |
| `fortolknings_regler/` | Same scraping pipeline but for DTU project economy rules (`eksternt-finansierede-projekter`), using hierarchical (BFS) crawling instead of hub-list crawling |
| `CopilotTimeoversigt/` | A standalone `RUNME.py` that users upload to a Microsoft Copilot Agent to process timetable CSV exports from Fusion |

All Python projects run in a **Conda environment**.

## Setup

```bash
# Install dependencies (Rejsedokument_chatbot and fortolknings_regler share these)
pip install crawl4ai httpx markitdown[all]
crawl4ai-setup
```

## Running the Scrapers

Both `Rejsedokument_chatbot` and `fortolknings_regler` use the same two-command interface:

```bash
# Phase 1–3: crawl web pages, download PDFs, clean content
python Main_file.py gather        # Rejsedokument_chatbot
python main_fortolkning.py gather # fortolknings_regler

# Merge all cleaned sources into one master .md file
python Main_file.py combine
python main_fortolkning.py combine
```

**Before running**, update the hardcoded paths and credentials at the top of the main file:
- `project_root` — absolute path to where output folders should be created
- `my_cookies` — `ASP.NET_SessionId` and `.ASPXAUTH` values (needed for PDF downloads from DTU Inside)
- Hub URLs / `target_start_url` — the DTU Inside pages to scrape from

## Architecture: Scraper Pipeline

Both scrapers share a 4-module structure with an identical 3-phase pipeline:

```
Main_file.py / main_fortolkning.py   ← orchestrator, config lives here
    ├── InsideToPDFauto.py / inside_to_pdf_fortolkning.py   ← Phase 1: web crawl
    ├── PDFhandler.py / pdf_handler_fortolkning.py          ← Phase 2: PDF download
    └── MDCleaning.py / md_cleaner_fortolkning.py           ← Phase 3: clean + combine
```

**Phase 1 – Web crawl (`InsideToPDFauto` / `inside_to_pdf_fortolkning`):**
- Uses Crawl4AI's `AsyncWebCrawler` in non-headless mode with a persistent browser profile (`dtu_session/` in cwd) to survive DTU SSO login across runs.
- On first run the browser opens and pauses for a manual ENTER after the user logs in.
- `Rejsedokument_chatbot` scans a fixed list of hub URLs for keyword-matching links, then crawls those pages (one level deep).
- `fortolknings_regler` performs a full BFS/hierarchical crawl starting from a single `base_url`, following any sub-links that stay within that URL prefix.
- PDF links found during crawl are logged to `manual_download_list.txt` rather than crawled.
- Pages that are 404s or under 500 characters are skipped.
- Output: raw `.md` files in `dtu_training_data/`.

**Phase 2 – PDF download (`PDFhandler`):**
- Reads URLs from `manual_download_list.txt`, downloads each PDF using `httpx` with DTU session cookies, converts to Markdown via `MarkItDown`, saves as `.md` in `dtu_training_data_pdf/`.

**Phase 3 – Clean & combine (`MDCleaning`):**
- `process_dtu_files`: Extracts content between DTU Inside page markers `"DEL På"` and `"Intern information på DTU"`, strips nav/menu noise using regex patterns, saves to `cleaned_dtu_data/`.
  - `fortolknings_regler` version falls back to using the full page text if markers are absent (more permissive than the chatbot version, which discards marker-less pages).
- `combine_all_sources`: Merges all cleaned web `.md` files and PDF-converted `.md` files into a single `dtu_training_master.md`.

**Generated directory layout (inside `project_root`):**
```
dtu_training_data/       ← raw crawled pages
dtu_training_data_pdf/   ← PDF-to-MD conversions
cleaned_dtu_data/        ← cleaned web pages
dtu_training_master.md   ← final combined output
manual_download_list.txt ← PDF URLs found during crawl
```

## CopilotTimeoversigt

`RUNME.py` is a self-contained script with no external dependencies beyond standard data-science libraries (pandas, openpyxl). Users upload it together with a Fusion CSV export to the **DTU Automatisk Timeoversigt** Copilot Agent and send the message `Kør timeoversigten.` The agent executes the script and returns a formatted Excel file. This project is not run locally.
