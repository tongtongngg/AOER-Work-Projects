import asyncio
import sys
from pathlib import Path

from crawler import run_smart_pipeline
from pdf_handler import process_dtu_pdfs
from md_cleaner import process_dtu_files, combine_all_sources

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "data"
RAW_WEB_DIR = DATA_DIR / "raw" / "web"
RAW_PDF_DIR = DATA_DIR / "raw" / "pdf"
PDF_LIST_PATH = DATA_DIR / "raw" / "manual_download_list.txt"
CLEANED_WEB_DIR = DATA_DIR / "interim" / "cleaned_web"
FINAL_MASTER_FILE = DATA_DIR / "processed" / "dtu_training_master.md"
SESSION_DIR = PROJECT_ROOT / ".cache" / "dtu_session"


async def main():
    my_hubs = [
        "https://www.inside.dtu.dk/oekonomi/afregning-af-udgifter-og-rejser",
        "https://www.inside.dtu.dk/oekonomi/tjenesterejser-og-transport",
    ]

    my_cookies = {
        "ASP.NET_SessionId": "YOUR_ID",
        ".ASPXAUTH": "YOUR_AUTH",
    }

    mode = sys.argv[1].lower() if len(sys.argv) >= 2 else "gather"

    if mode == "gather":
        print("\n--- PHASE 1: Web Crawling ---")
        await run_smart_pipeline(
            my_hubs,
            output_dir=RAW_WEB_DIR,
            pdf_log_file=PDF_LIST_PATH,
            session_dir=SESSION_DIR,
        )

        print("\n--- PHASE 2: PDF Processing ---")
        process_dtu_pdfs(
            url_file=PDF_LIST_PATH,
            output_dir=RAW_PDF_DIR,
            cookies=my_cookies,
        )

        print("\n--- PHASE 3: Cleaning Web Content ---")
        process_dtu_files(RAW_WEB_DIR, CLEANED_WEB_DIR)

        print("\nGather complete!")

    elif mode == "combine":
        print("\n--- MANUAL OVERRIDE: Merging Existing Sources ---")
        combine_all_sources(CLEANED_WEB_DIR, RAW_PDF_DIR, FINAL_MASTER_FILE)
        print(f"\nCombination complete! Master file updated: {FINAL_MASTER_FILE}")

    else:
        print(f"Error: Unknown command '{mode}'")
        print("Available commands: gather, combine")


if __name__ == "__main__":
    asyncio.run(main())
