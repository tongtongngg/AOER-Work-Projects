import asyncio
import os
import sys
from InsideToPDFauto import run_smart_pipeline
from PDFhandler import process_dtu_pdfs
from MDCleaning import process_dtu_files, combine_all_sources

async def main():
    # --- CONFIGURATION ---
    project_root = r"C:\Users\botyu\OneDrive - Danmarks Tekniske Universitet\Skrivebord\Arbejde\Projekter\Rejsedokument_chatbot"
    
    my_hubs = [
        "https://www.inside.dtu.dk/oekonomi/afregning-af-udgifter-og-rejser",
        "https://www.inside.dtu.dk/oekonomi/tjenesterejser-og-transport"
    ]
    
    # Paths
    raw_web_dir = os.path.join(project_root, "dtu_training_data")
    pdf_list_path = os.path.join(project_root, "manual_download_list.txt")
    pdf_output_dir = os.path.join(project_root, "dtu_training_data_pdf")
    cleaned_web_dir = os.path.join(project_root, "cleaned_dtu_data")
    final_master_file = os.path.join(project_root, "dtu_training_master.md")

    # Cookies for PDF access
    my_cookies = {
        "ASP.NET_SessionId": "YOUR_ID",
        ".ASPXAUTH": "YOUR_AUTH"
    }

    # --- DEFINE MODE FIRST ---
    # This ensures 'mode' always has a value before we start checking IF statements
    if len(sys.argv) < 2:
        mode = "gather"
    else:
        mode = sys.argv[1].lower()

    # --- EXECUTION ---

    if mode == "gather":
        print("\n--- PHASE 1: Web Crawling ---")
        await run_smart_pipeline(my_hubs, project_root=project_root)

        print("\n--- PHASE 2: PDF Processing ---")
        process_dtu_pdfs(
            url_file=pdf_list_path,
            output_dir=pdf_output_dir,
            cookies=my_cookies
        )

        print("\n--- PHASE 3: Cleaning Web Content ---")
        process_dtu_files(raw_web_dir, cleaned_web_dir)

        print(f"\nGather complete!")

    elif mode == "combine":
        print("\n--- MANUAL OVERRIDE: Merging Existing Sources ---")
        combine_all_sources(cleaned_web_dir, pdf_output_dir, final_master_file)
        print(f"\nCombination complete! Master file updated: {final_master_file}")

    else:
        print(f"Error: Unknown command '{mode}'")
        print("Available commands: gather, combine")

if __name__ == "__main__":
    asyncio.run(main())