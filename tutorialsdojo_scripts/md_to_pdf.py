# Convert MD to PDF

import os
import subprocess

INPUT_DIR = "tutorialsdojo_cheatsheets"
OUTPUT_DIR = "tutorialsdojo_cheatsheets_pdf"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def convert_md_to_pdf(input_file, output_file):
    try:
        subprocess.run([
            "pandoc",
            input_file,
            "-o",
            output_file,
            "--pdf-engine=xelatex",
            "--toc",
            "--highlight-style", "tango"
        ], check=True)
        print(f"Converted: {input_file} → {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error converting {input_file}: {e}")

def batch_convert():
    for filename in os.listdir(INPUT_DIR):
        if filename.endswith(".md"):
            input_path = os.path.join(INPUT_DIR, filename)
            output_filename = filename.replace(".md", ".pdf")
            output_path = os.path.join(OUTPUT_DIR, output_filename)
            convert_md_to_pdf(input_path, output_path)

if __name__ == "__main__":
    batch_convert()
