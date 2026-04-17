import os
import httpx
from markitdown import MarkItDown

def process_dtu_pdfs(url_file, output_dir, cookies=None):
    if not os.path.exists(url_file):
        print(f"Error: PDF list file not found at {url_file}")
        return

    md_converter = MarkItDown()
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(url_file, "r", encoding="utf-8") as f:
        urls = [line.strip() for line in f if line.strip().startswith("http")]

    if not urls:
        print("No PDF URLs found to process.")
        return

    print(f"Found {len(urls)} PDFs to process...")

    with httpx.Client(cookies=cookies, follow_redirects=True) as client:
        for url in urls:
            try:
                base_name = url.split("/")[-1]
                target_name = base_name.replace(".pdf", ".md")
                output_path = os.path.join(output_dir, target_name)

                print(f"Downloading: {base_name}...")
                
                response = client.get(url)
                response.raise_for_status()

                temp_pdf = "temp_processing.pdf"
                with open(temp_pdf, "wb") as f:
                    f.write(response.content)

                result = md_converter.convert(temp_pdf)

                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(result.text_content)

                print(f"Successfully saved to: {output_path}")

            except Exception as e:
                print(f"Error processing {url}: {e}")
            finally:
                if os.path.exists("temp_processing.pdf"):
                    os.remove("temp_processing.pdf")

                    
