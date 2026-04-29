import tempfile
from pathlib import Path

import httpx
from markitdown import MarkItDown


def process_dtu_pdfs(url_file, output_dir, cookies=None):
    url_file = Path(url_file)
    output_dir = Path(output_dir)

    if not url_file.exists():
        print(f"Error: PDF list file not found at {url_file}")
        return

    md_converter = MarkItDown()
    output_dir.mkdir(parents=True, exist_ok=True)

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
                output_path = output_dir / target_name

                print(f"Downloading: {base_name}...")

                response = client.get(url)
                response.raise_for_status()

                with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
                    tmp.write(response.content)
                    temp_pdf = Path(tmp.name)

                try:
                    result = md_converter.convert(str(temp_pdf))

                    with open(output_path, "w", encoding="utf-8") as f:
                        f.write(result.text_content)

                    print(f"Successfully saved to: {output_path}")
                finally:
                    temp_pdf.unlink(missing_ok=True)

            except Exception as e:
                print(f"Error processing {url}: {e}")
