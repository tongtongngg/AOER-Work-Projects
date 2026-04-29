# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Purpose

Scrapes DTU Inside travel policy pages and PDFs, cleans the content, and merges everything into a single `data/processed/dtu_training_master.md` file for use as chatbot training data.

## Setup

```bash
pip install crawl4ai httpx markitdown[all]
crawl4ai-setup
```

## Running

```bash
# Crawl web pages, download PDFs, clean content
python src/main.py gather

# Merge all cleaned sources into data/processed/dtu_training_master.md
python src/main.py combine
```

All paths are anchored to the project root via `Path(__file__).resolve().parent.parent`, so the scripts run correctly from any working directory.

**Before first run**, edit the top of `src/main.py`:
- `my_cookies` — `ASP.NET_SessionId` and `.ASPXAUTH` from your browser session (required for PDF downloads)
- `my_hubs` — the DTU Inside hub URLs to crawl from

## Layout

```
Rejsedokument_chatbot/
├── src/
│   ├── main.py          ← orchestrator + configuration
│   ├── crawler.py       ← Phase 1: web crawl
│   ├── pdf_handler.py   ← Phase 2: PDF download + MD conversion
│   └── md_cleaner.py    ← Phase 3: clean + combine
├── data/
│   ├── raw/
│   │   ├── web/                      ← raw crawled pages
│   │   ├── pdf/                      ← PDF-to-MD conversions
│   │   └── manual_download_list.txt  ← PDF URLs discovered during crawl
│   ├── interim/cleaned_web/          ← marker-extracted, noise-filtered pages
│   └── processed/
│       └── dtu_training_master.md    ← final merged output
├── docs/
└── .cache/dtu_session/  ← persistent Chromium profile (gitignored)
```

## Architecture

`src/main.py` is the orchestrator and sole configuration file. It calls three modules in sequence:

**Phase 1 — `src/crawler.py` (`run_smart_pipeline`)**
- Opens a non-headless Chromium browser with a persistent profile stored in `.cache/dtu_session/` so DTU SSO login survives between runs.
- Pauses and waits for a manual ENTER after the user logs in the first time.
- Scans each hub URL for internal links matching keywords (`oekonomi`, `rejser`, `udgifter`, `afregning`, etc.).
- Crawls matched pages one level deep, saving raw Markdown to `data/raw/web/`.
- PDF links are not crawled — they are logged to `data/raw/manual_download_list.txt` for Phase 2.
- Pages that contain `"404"` or are under 500 characters are skipped.

**Phase 2 — `src/pdf_handler.py` (`process_dtu_pdfs`)**
- Reads PDF URLs from `data/raw/manual_download_list.txt`.
- Downloads each with `httpx` using the session cookies from `src/main.py`.
- Converts to Markdown via `MarkItDown` and saves to `data/raw/pdf/`.

**Phase 3 — `src/md_cleaner.py`**
- `process_dtu_files`: Extracts content between the DTU Inside page markers `"DEL På"` and `"Intern information på DTU"`, strips navigation noise (asterisk-only lines, menu links) with regex, writes cleaned files to `data/interim/cleaned_web/`. Files where markers are absent are discarded.
- `combine_all_sources`: Concatenates all cleaned web `.md` and PDF-converted `.md` files into `data/processed/dtu_training_master.md`, labelling each block as `WEB SOURCE` or `PDF SOURCE`.

## Authentication

The browser session (`.cache/dtu_session/`) persists the DTU SSO login across runs — delete this folder to force a fresh login. The `my_cookies` dict in `src/main.py` is separate: it is only used by the `httpx`-based PDF downloader and must be updated when the session expires.
