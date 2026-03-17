import os
import re
from pathlib import Path

def clean_dtu_content(content):
    start_marker = "DEL På"
    end_marker = "Intern information på DTU"
    
    # 1. Check for basic markers first
    if start_marker not in content or end_marker not in content:
        return None


    block = content.split(start_marker, 1)[1]
    block = block.split(end_marker, 1)[0]
    
    # 3. Clean and filter the extracted block line by line
    lines = block.splitlines()
    cleaned_lines = []
    

    filter_patterns = [
        r'^\s*\*\s*$',                # Lines containing ONLY an asterisk, like '* ' or '  * '
        r'student\.dtu\.dk',        # Menu links like ' * student.dtu.dk'
        r'PhD studies',             # Menu links
        r'Institutter og afdelinger', # Menu links
        r'DEL På.*'                  # If 'DEL På' appears again (unlikely, but for safety)
    ]
    
    # Compile the regular expressions for efficiency
    compiled_regexes = [re.compile(pattern, re.IGNORECASE) for pattern in filter_patterns]
    
    content_area_found = False # Flag to mark when we hit the ACTUAL content (like a header)

    for line in lines:
        # A. If we haven't found the actual content area yet, we ignore all filter patterns.
        if not content_area_found:
            is_filtered = any(regex.search(line) for regex in compiled_regexes)
            if is_filtered or line.strip() == "":
                continue # Skip current line
            else:
                # We found a line that isn't filtered or empty, so content starts here.
                content_area_found = True
        
        if any(regex.search(line) for regex in compiled_regexes):
            continue # Skip this specific line even within content area
            
        cleaned_lines.append(line)

    # 4. Final join and strip, and return None if result is empty or too short.
    result = "\n".join(cleaned_lines).strip()
    return result if len(result) > 20 else None

def process_dtu_files(input_folder, output_folder):
    input_path = Path(input_folder)
    output_path = Path(output_folder)
    output_path.mkdir(parents=True, exist_ok=True)
    
    files_processed = 0
    print(f"Scanning directory: {input_path.absolute()}")

    for md_file in input_path.glob("*.md"):
        try:
            with open(md_file, "r", encoding="utf-8") as f:
                raw_data = f.read()
            
            cleaned_data = clean_dtu_content(raw_data)
            
            if cleaned_data:
                output_file_path = output_path / md_file.name
                with open(output_file_path, "w", encoding="utf-8") as f:
                    f.write(cleaned_data)
                files_processed += 1
                print(f"Cleaned: {md_file.name}")
            else:
                print(f"Skipped (Markers not found): {md_file.name}")
        except Exception as e:
            print(f"Error processing {md_file.name}: {e}")

    print(f"\nSuccess! {files_processed} files saved to '{output_folder}'.")


def combine_all_sources(cleaned_folder, pdf_folder, output_master_file):
    """
    Merges both the cleaned web files and the raw PDF-based files into one master MD.
    """
    master_file_path = Path(output_master_file)
    combined_count = 0
    
    with open(master_file_path, "w", encoding="utf-8") as master_f:
        # --- PART 1: Process Cleaned Web Data ---
        clean_path = Path(cleaned_folder)
        if clean_path.exists():
            print(f"\nMerging cleaned web data from: {clean_path.name}")
            for md_file in sorted(list(clean_path.glob("*.md"))):
                with open(md_file, "r", encoding="utf-8") as f:
                    content = f.read().strip()
                if content:
                    master_f.write(f"\n\n--- DOCUMENT (WEB SOURCE): {md_file.name} ---\n\n")
                    master_f.write(content)
                    master_f.write("\n")
                    combined_count += 1
                    print(f"Added cleaned: {md_file.name}")

        # --- PART 2: Process Raw PDF Data (Directly as MD) ---
        pdf_source_path = Path(pdf_folder)
        if pdf_source_path.exists():
            print(f"\nMerging raw PDF-to-MD data from: {pdf_source_path.name}")
            for pdf_file in sorted(list(pdf_source_path.glob("*.md"))):
                with open(pdf_file, "r", encoding="utf-8") as f:
                    content = f.read().strip()
                if content:
                    master_f.write(f"\n\n--- DOCUMENT (PDF SOURCE): {pdf_file.name} ---\n\n")
                    master_f.write(content)
                    master_f.write("\n")
                    combined_count += 1
                    print(f"Added raw PDF content: {pdf_file.name}")

    print(f"\nFinal Success! Combined {combined_count} files into '{output_master_file}'.")

