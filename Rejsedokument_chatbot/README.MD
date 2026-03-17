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
- main.py: The primary script containing the AsyncWebCrawler logic.
- requirements.txt: Minimal list of 3rd party packages (crawl4ai, httpx, markitdown).
- data/: (Auto-generated) Stores the converted .md rejsedokumenter.

## Authentication Note
DTU Inside requires a login. This scraper handles the session via BrowserConfig to manage persistent contexts or session cookies.

## Usage
Run the scraper from terminal (remember to edit path code in Main_file.py)
```bash
# Web scrape DTU inside and clean data
python main.py gather

# Combine all scraped websites
python main.py combine
```
