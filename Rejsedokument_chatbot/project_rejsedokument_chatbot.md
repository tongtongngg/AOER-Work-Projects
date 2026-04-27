---
name: Rejsedokument Chatbot Project
description: DTU travel document scraper and processor for building a chatbot trained on DTU expense/travel policies
type: project
---

# Rejsedokument Chatbot

**What it does:** Scrapes DTU Inside portal for travel/expense (rejsedokument) guidelines, converts PDFs and web pages to Markdown, cleans and consolidates them into a master training document — likely for a chatbot that answers employee questions about DTU travel expense policies.

**Why:** DTU employees need answers about rejse (travel) and økonomi (expense) reimbursement procedures. The master doc is the training data source.

**Location:** `Projekter/Rejsedokument_chatbot/`

## Tech Stack
- Python (async / asyncio)
- Crawl4AI — async web crawler with persistent browser session
- MarkItDown (Microsoft) — PDF/document → Markdown
- httpx — HTTP client with cookie/auth support

## Key Files
| File | Role |
|------|------|
| `Main_file.py` | Orchestrator; two modes: `gather` (scrape) and `combine` (clean+merge) |
| `InsideToPDFauto.py` | Crawls DTU Inside hubs, extracts relevant pages to `.md` |
| `PDFhandler.py` | Downloads PDFs and converts via MarkItDown |
| `MDCleaning.py` | Filters navigation noise, merges web + PDF into master file |
| `dtu_training_master.md` | Final consolidated output (~1427 lines) |

## Data Flow
```
DTU Inside Portal → dtu_training_data/ → cleaned_dtu_data/ ↘
                                                              dtu_training_master.md
PDF downloads    → dtu_training_data_pdf/               ↗
```

## Notable Details
- Auth: persistent browser context + ASP.NET_SessionId / .ASPXAUTH cookies
- Content extraction: looks for DTU-specific markers ("DEL På" start, "Intern information på DTU" end)
- Targets keywords: oekonomi, rejser, udgifter, afregning
- PDFs require a manual download list and credential setup
