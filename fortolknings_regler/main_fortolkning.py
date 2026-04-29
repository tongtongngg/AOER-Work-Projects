import asyncio
import os
import sys
from inside_to_pdf_fortolkning import run_smart_pipeline
from merge_md import combine_markdown_files
from md_cleaner_fortolkning import process_dtu_files, combine_all_sources
from pdf_to_md_test import process_pdfs


async def main():
    # ==========================================
    # --- CONFIGURATION ---
    # ==========================================
    
    # 1. PROJECT ROOT
    project_root = r"C:\Users\s204093\Documents\Kode\AOER-Work-Projects\fortolknings_regler\data\test" 
    
    # 2. STARTING URL
    target_start_url = "https://www.inside.dtu.dk/oekonomi/projektoekonomi/projekttype/eksternt-finansierede-projekter" 
    
    # ==========================================
    # --- PATHS ---
    # ==========================================
    raw_web_dir = os.path.join(project_root, "dtu_training_data")
    pdf_list_path = os.path.join(project_root, "manual_download_list.txt")
    pdf_raw_dir = os.path.join(project_root, "downloaded_pdfs")
    pdf_output_dir = os.path.join(project_root, "dtu_training_data_pdf")
    cleaned_web_dir = os.path.join(project_root, "cleaned_dtu_data")

    final_master_file = os.path.join(project_root, "dtu_training_master.md")
    final_pdf_master_file = os.path.join(project_root, "dtu_training_master_pdf.md")

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
        print("\n--- PHASE 1: Web Crawling & PDF Logging ---")

        await run_smart_pipeline(base_url=target_start_url, project_root=project_root)

        print(f"\nGather complete! Web pages saved to '{raw_web_dir}' and PDFs logged to '{pdf_list_path}'.")

        process_dtu_files(raw_web_dir, cleaned_web_dir)


    elif mode == "combine_webpages":
        print("\n--- MANUAL OVERRIDE: Merging Existing Sources ---")

        combine_markdown_files(cleaned_web_dir, final_master_file)
        print(f"\n[Placeholder] Combine functionality will be added here soon.")

    elif mode == "pdf_to_md":
        print("\n--- PHASE 2: Downloading & Converting PDFs ---")
        process_pdfs(
            url_file=pdf_list_path, 
            pdf_dir=pdf_raw_dir, 
            md_dir=pdf_output_dir
        )
        print(f"\nPDF processing complete! Markdown files saved to '{pdf_output_dir}'.")

    elif mode == "combine_pdf": # <-- NEW: Handles PDF merging
        print("\n--- MANUAL OVERRIDE: Merging PDF Markdown Files ---")
        combine_markdown_files(pdf_output_dir, final_pdf_master_file)
        print(f"\nPDFs combined into '{final_pdf_master_file}'.")

    else:
        print(f"Error: Unknown command '{mode}'")
        print("Available commands: gather, combine_webpages, pdf_to_md, combine_pdf")

if __name__ == "__main__":
    asyncio.run(main())