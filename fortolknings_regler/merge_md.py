import os
from pathlib import Path

def combine_markdown_files(input_folder, output_file):
    """
    Combines all .md files in a folder into a single master .md file.
    """
    source_dir = Path(input_folder)
    master_file = Path(output_file)
    
    # Check if the input directory exists
    if not source_dir.exists() or not source_dir.is_dir():
        print(f"Error: The folder '{input_folder}' does not exist.")
        return

    # Find all .md files and sort them alphabetically
    md_files = sorted(list(source_dir.glob("*.md")))
    
    if not md_files:
        print(f"No Markdown files found in '{input_folder}'.")
        return

    print(f"Found {len(md_files)} Markdown files. Starting merge...")

    # Open the master file in write mode ('w' overwrites, 'a' appends)
    with open(master_file, "w", encoding="utf-8") as outfile:
        # Add a main title to the top of the document
        outfile.write("# Master Training Data Document\n\n")
        
        for file_path in md_files:
            try:
                with open(file_path, "r", encoding="utf-8") as infile:
                    content = infile.read().strip()
                    
                # Only add files that actually have text
                if content:
                    # Create a clear visual separator between documents
                    outfile.write(f"\n\n{'='*50}\n")
                    outfile.write(f"### SOURCE: {file_path.name}\n")
                    outfile.write(f"{'='*50}\n\n")
                    
                    # Write the actual content
                    outfile.write(content)
                    outfile.write("\n") # Add a trailing newline
                    
                    print(f"Merged: {file_path.name}")
                else:
                    print(f"Skipped (empty): {file_path.name}")
                    
            except Exception as e:
                print(f"Error reading {file_path.name}: {e}")

    print(f"\nSuccess! All files have been merged into '{master_file.name}'")


if __name__ == "__main__":
    # --- UPDATE THESE PATHS TO MATCH YOUR FOLDERS ---
    
    # The folder where your converted PDF .md files are saved
    TARGET_FOLDER = r"C:\Users\s204093\Documents\Kode\AOER-Work-Projects\fortolknings_regler\data\pdf_markdown_files"
    
    # The file you want to create with everything inside
    OUTPUT_FILE = r"C:\Users\s204093\Documents\Kode\AOER-Work-Projects\fortolknings_regler\data\dtu_pdfs_combined_v2.md"
    
    combine_markdown_files(TARGET_FOLDER, OUTPUT_FILE)