#!/bin/bash

# Copies everything in a directory to clipboard

# Usage: ./list_and_preview.sh [directory] [max_depth]
# Defaults: current directory, max depth = 1

DIR="${1:-.}"
MAX_DEPTH="${2:-1}"

# Define code file extensions
CODE_EXTENSIONS=("py" "json" "js" "ts" "sh" "rb" "java" "c" "cpp" "cs" "go" "html" "css" "xml" "yml" "yaml" "toml")

# Choose clipboard command
if command -v pbcopy &> /dev/null; then
  CLIP_CMD="pbcopy"
elif command -v xclip &> /dev/null; then
  CLIP_CMD="xclip -selection clipboard"
else
  echo "No clipboard utility found (pbcopy or xclip required)."
  exit 1
fi

# Temp file for capturing output
TMPFILE=$(mktemp)

# Helper: check if file has a known code extension
is_code_file() {
  local filename="$1"
  local ext="${filename##*.}"
  for code_ext in "${CODE_EXTENSIONS[@]}"; do
    if [[ "$ext" == "$code_ext" ]]; then
      return 0
    fi
  done
  return 1
}

# Process files
find "$DIR" -maxdepth "$MAX_DEPTH" -type f | while read -r file; do
  echo "=== $file ===" >> "$TMPFILE"
  
  if file --mime-type "$file" | grep -q 'text/' || is_code_file "$file"; then
    cat "$file" >> "$TMPFILE"
  else
    echo "[Binary or non-text file, skipped]" >> "$TMPFILE"
  fi

  echo -e "\n" >> "$TMPFILE"
done

# Output to clipboard and also to stdout
cat "$TMPFILE" | eval "$CLIP_CMD"
cat "$TMPFILE"

# Cleanup
rm "$TMPFILE"

