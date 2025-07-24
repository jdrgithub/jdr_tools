import os
import re

INPUT_DIR = "tutorialsdojo_cheatsheets"
OUTPUT_DIR = "tutorialsdojo_cheatsheets_clean"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def clean_file(filename):
    with open(os.path.join(INPUT_DIR, filename), "r", encoding="utf-8") as f:
        lines = f.readlines()

    cleaned_lines = []
    skip_mode = False

    for i, line in enumerate(lines):
        lower_line = line.lower()

        # If we're skipping, continue skipping until we hit a new heading or blank line
        if skip_mode:
            if re.match(r"^#{1,6}\s", line) or line.strip() == "":
                skip_mode = False
            else:
                continue

        # Check for skip triggers (case-insensitive)
        if any(trigger in lower_line for trigger in [
            "validate your knowledge",
            "subscribe to our newsletter",
            "written by:",
            "recent posts",
            "references:",
            "follow us on",
            "view our aws",
            "check out our free courses",
            "did you find our content helpful"
        ]):
            skip_mode = True
            continue

        # Filter out nav-dump style lines (super long single list items)
        if line.startswith("- ") and len(line) > 400:
            continue

        cleaned_lines.append(line)

    # Save cleaned output
    if cleaned_lines:
        with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
            f.writelines(cleaned_lines)
        print(f"Cleaned: {filename}")
    else:
        print(f"Skipped {filename}: Empty after cleaning.")

def main():
    files = [f for f in os.listdir(INPUT_DIR) if f.endswith(".md")]
    for file in files:
        clean_file(file)

if __name__ == "__main__":
    main()
