import asyncio
import os
import sys
from inside_to_pdf_fortolkning import run_smart_pipeline
from pdf_handler_fortolkning import process_dtu_pdfs
from md_cleaner_fortolkning import process_dtu_files, combine_all_sources

async def main():
    # ==========================================
    # --- CONFIGURATION (FILL THESE OUT) ---
    # ==========================================
    
    # 1. PROJECT ROOT: The main folder where everything will be saved.
    # The one you have here looks correct based on your previous code.
    project_root = r"C:\Users\s204093\Documents\Kode\AOER-Work-Projects\fortolknings_regler\data"  # <-- UPDATE THIS PATH TO YOUR DESIRED LOCATION
    # 2. STARTING URL: The exact page you want to scrape downwards from.
    target_start_url = "https://www.inside.dtu.dk/oekonomi/projektoekonomi/projekttype/eksternt-finansierede-projekter" 
    
    # 3. COOKIES: Needed so your Python PDF downloader can access locked DTU files.
    # See the instructions below the code block on how to get these!
    #my_cookies = {
    #    "ASP.NET_SessionId": "",
    #    ".ASPXAUTH": "YOUR_AUTH_HERE"
    #}

    # ==========================================
    # --- PATHS (Generated automatically) ---
    # ==========================================
    raw_web_dir = os.path.join(project_root, "dtu_training_data")
    pdf_list_path = os.path.join(project_root, "manual_download_list.txt")
    pdf_output_dir = os.path.join(project_root, "dtu_training_data_pdf")
    cleaned_web_dir = os.path.join(project_root, "cleaned_dtu_data")
    final_master_file = os.path.join(project_root, "dtu_training_master.md")

    # ==========================================
    # --- DEFINE MODE ---
    # ==========================================
    if len(sys.argv) < 2:
        mode = "gather"
    else:
        mode = sys.argv[1].lower()

    # ==========================================
    # --- EXECUTION ---
    # ==========================================
    if mode == "gather":
        print("\n--- PHASE 1: Web Crawling ---")
        # Notice we are now passing base_url instead of my_hubs
        await run_smart_pipeline(base_url=target_start_url, project_root=project_root)

        print("\n--- PHASE 2: PDF Processing ---")
        #process_dtu_pdfs(
        #    url_file=pdf_list_path,
        #    output_dir=pdf_output_dir,
        #    cookies=my_cookies
        #)

        print("\n--- PHASE 3: Cleaning Web Content ---")
        process_dtu_files(raw_web_dir, cleaned_web_dir)

        print("\nGather complete! If you are ready, run 'python main.py combine' to merge.")

    elif mode == "combine":
        print("\n--- MANUAL OVERRIDE: Merging Existing Sources ---")
        combine_all_sources(cleaned_web_dir, pdf_output_dir, final_master_file)
        print(f"\nCombination complete! Master file updated: {final_master_file}")

    else:
        print(f"Error: Unknown command '{mode}'")
        print("Available commands: gather, combine")

if __name__ == "__main__":
    asyncio.run(main())