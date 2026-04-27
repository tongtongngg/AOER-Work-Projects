import os
import requests
import pymupdf4llm
from urllib.parse import urlparse, unquote

def process_pdfs(url_file, pdf_dir, md_dir):
    # Create directories if they don't exist
    os.makedirs(pdf_dir, exist_ok=True)
    os.makedirs(md_dir, exist_ok=True)

    # 1. Read the URLs
    if not os.path.exists(url_file):
        print(f"Error: Could not find {url_file}")
        return

    with open(url_file, "r", encoding="utf-8") as file:
        # Read lines, strip whitespace, and ONLY keep lines that are actual web links
        urls = [line.strip() for line in file.readlines() if line.strip().startswith("http")]

    if not urls:
        print("No valid URLs found in the list.")
        return

    print(f"Found {len(urls)} URLs to process.")

    # 2. Loop through and download/convert each one
    for index, url in enumerate(urls, start=1):
        print(f"\nProcessing {index}/{len(urls)}: {url}")
        
        # Extract the filename from the URL
        parsed_url = urlparse(url)
        # unquote removes URL encoding (e.g., turns '%20' into spaces)
        filename = os.path.basename(unquote(parsed_url.path))
        
        # Fallback just in case the URL doesn't end in a clean filename
        if not filename:
            filename = f"document_{index}.pdf"
            
        # Strip the existing .pdf extension so we can reuse the base name for the .md file
        base_name, _ = os.path.splitext(filename)

        # Create safe paths
        pdf_path = os.path.join(pdf_dir, f"{base_name}.pdf")
        md_path = os.path.join(md_dir, f"{base_name}.md")

        # --- DOWNLOAD ---
        try:
            # We use a user-agent header because some servers block basic python requests
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            response = requests.get(url, headers=headers, stream=True, timeout=15)
            response.raise_for_status() # Check for HTTP errors

            with open(pdf_path, "wb") as pdf_file:
                for chunk in response.iter_content(chunk_size=8192):
                    pdf_file.write(chunk)
            print(f" ✓ Downloaded successfully as {base_name}.pdf")
            
        except Exception as e:
            print(f" ✗ Failed to download: {e}")
            continue # Skip to the next URL if download fails

        # --- CONVERT TO MARKDOWN ---
        try:
            # pymupdf4llm extracts the text, headings, and tables into markdown format
            md_text = pymupdf4llm.to_markdown(pdf_path)

            with open(md_path, "w", encoding="utf-8") as md_file:
                md_file.write(md_text)
            print(f" ✓ Converted to Markdown successfully as {base_name}.md")
            
        except Exception as e:
            print(f" ✗ Failed to convert to markdown: {e}")

# (Optional) Kept for testing the script directly
if __name__ == "__main__":
    print("Please run this via main_fortolkning.py")