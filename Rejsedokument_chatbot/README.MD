# DTU Inside: Rejsedokumenter Scraper

This module automates the retrieval and conversion of travel documents (rejsedokumenter) from the DTU Inside portal. It uses Crawl4AI for web navigation and MarkItDown to ensure all retrieved data is stored in a readable, structured format.

## Features
- Asynchronous Crawling: Uses asyncio and Crawl4AI for fast, non-blocking page processing.
- Markdown Conversion: Converts complex HTML and document fragments into clean Markdown using MarkItDown.
- Automated Regex: Uses the re module to identify and sort document types such as invoices, tickets, or approvals.

## Setup and Installation

### 1. Environment
Ensure you are in your Conda environment, then install the core dependencies:
```bash
pip install crawl4ai httpx markitdown[all]
```

And then run this command when installing crawl4ai:
```bash
crawl4ai-setup
```

## Project Structure
```
src/                       Python source modules
  main.py                  orchestrator + configuration
  crawler.py               Phase 1: web crawl
  pdf_handler.py           Phase 2: PDF download + MD conversion
  md_cleaner.py            Phase 3: clean + combine
data/
  raw/web/                 raw crawled pages (auto-generated)
  raw/pdf/                 PDF-to-MD conversions (auto-generated)
  raw/manual_download_list.txt
  interim/cleaned_web/     marker-extracted, noise-filtered pages
  processed/
    dtu_training_master.md final merged training file
docs/                      project notes
.cache/dtu_session/        persistent Chromium profile (gitignored)
requirements.txt
```

All paths in code are anchored to the project root, so the scripts can be run from any working directory.

## Authentication Note
DTU Inside requires a login. The scraper persists the SSO session in `.cache/dtu_session/` via BrowserConfig. PDF downloads additionally need the `ASP.NET_SessionId` and `.ASPXAUTH` cookies set in `src/main.py`.

## Usage
Edit cookies and hub URLs at the top of `src/main.py`, then:
```bash
# Web scrape DTU inside and clean data
python src/main.py gather

# Combine all scraped sources into data/processed/dtu_training_master.md
python src/main.py combine
```
