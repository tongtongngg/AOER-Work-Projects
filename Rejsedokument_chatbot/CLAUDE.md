# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Purpose

Scrapes DTU Inside travel policy pages and PDFs, cleans the content, and merges everything into a single `dtu_training_master.md` file for use as chatbot training data.

## Setup

```bash
pip install crawl4ai httpx markitdown[all]
crawl4ai-setup
```

## Running

```bash
# Crawl web pages, download PDFs, clean content
python Main_file.py gather

# Merge all cleaned sources into dtu_training_master.md
python Main_file.py combine
```

**Before first run**, edit the top of `Main_file.py`:
- `project_root` — absolute path to this project folder
- `my_cookies` — `ASP.NET_SessionId` and `.ASPXAUTH` from your browser session (required for PDF downloads)
- `my_hubs` — the DTU Inside hub URLs to crawl from

## Architecture

`Main_file.py` is the orchestrator and sole configuration file. It calls three modules in sequence:

**Phase 1 — `InsideToPDFauto.py` (`run_smart_pipeline`)**
- Opens a non-headless Chromium browser with a persistent profile stored in `dtu_session/` (cwd) so DTU SSO login survives between runs.
- Pauses and waits for a manual ENTER after the user logs in the first time.
- Scans each hub URL for internal links matching keywords (`oekonomi`, `rejser`, `udgifter`, `afregning`).
- Crawls matched pages one level deep, saving raw Markdown to `dtu_training_data/`.
- PDF links are not crawled — they are logged to `manual_download_list.txt` for Phase 2.
- Pages that contain `"404"` or are under 500 characters are skipped.

**Phase 2 — `PDFhandler.py` (`process_dtu_pdfs`)**
- Reads PDF URLs from `manual_download_list.txt`.
- Downloads each with `httpx` using the session cookies from `Main_file.py`.
- Converts to Markdown via `MarkItDown` and saves to `dtu_training_data_pdf/`.

**Phase 3 — `MDCleaning.py`**
- `process_dtu_files`: Extracts content between the DTU Inside page markers `"DEL På"` and `"Intern information på DTU"`, strips navigation noise (asterisk-only lines, menu links) with regex, writes cleaned files to `cleaned_dtu_data/`. Files where markers are absent are discarded.
- `combine_all_sources`: Concatenates all cleaned web `.md` and PDF-converted `.md` files into `dtu_training_master.md`, labelling each block as `WEB SOURCE` or `PDF SOURCE`.

**Generated output layout (inside `project_root`):**
```
dtu_training_data/       ← raw crawled pages
dtu_training_data_pdf/   ← PDF-to-MD conversions
cleaned_dtu_data/        ← marker-extracted, noise-filtered pages
dtu_training_master.md   ← final merged output
manual_download_list.txt ← PDF URLs discovered during crawl
```

## Authentication

The browser session (`dtu_session/`) persists the DTU SSO login across runs — delete this folder to force a fresh login. The `my_cookies` dict in `Main_file.py` is separate: it is only used by the `httpx`-based PDF downloader and must be updated when the session expires.
