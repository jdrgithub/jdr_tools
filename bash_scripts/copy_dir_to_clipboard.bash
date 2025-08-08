#!/bin/bash

# Usage:
#   ./copy_dir_to_clipboard.bash                # current dir, depth 1
#   ./copy_dir_to_clipboard.bash mydir          # mydir, depth 1
#   ./copy_dir_to_clipboard.bash --depth 2      # current dir, depth 2
#   ./copy_dir_to_clipboard.bash mydir --depth 2  # mydir, depth 2

# Default values
DIR="."
MAX_DEPTH=1

# Parse arguments
while [[ $# -gt 0 ]]; do
  case "$1" in
    --depth)
      shift
      MAX_DEPTH="$1"
      ;;
    *)
      DIR="$1"
      ;;
  esac
  shift
done

# Code file extensions
CODE_EXTENSIONS=("py" "json" "js" "ts" "sh" "rb" "java" "c" "cpp" "cs" "go" "html" "css" "xml" "yml" "yaml" "toml")

# Clipboard support
if command -v clip.exe &>/dev/null; then
  CLIP_CMD="clip.exe"
elif command -v pbcopy &>/dev/null; then
  CLIP_CMD="pbcopy"
elif command -v xclip &>/dev/null; then
  CLIP_CMD="xclip -selection clipboard"
else
  echo "No clipboard utility found (clip.exe, pbcopy, or xclip)."
  exit 1
fi

# Create temporary file
TMPFILE=$(mktemp /tmp/clipdump.XXXXXX)

# Check file extension
is_code_file() {
  local ext="${1##*.}"
  for e in "${CODE_EXTENSIONS[@]}"; do
    [[ "$ext" == "$e" ]] && return 0
  done
  return 1
}

# Collect files
find "$DIR" -maxdepth "$MAX_DEPTH" -type f | while read -r file; do
  echo "=== $file ===" >> "$TMPFILE"
  if file --mime-type "$file" | grep -q 'text/' || is_code_file "$file"; then
    cat "$file" >> "$TMPFILE"
  else
    echo "[Binary or non-text file, skipped]" >> "$TMPFILE"
  fi
  echo -e "\n" >> "$TMPFILE"
done

# Output to clipboard and terminal
cat "$TMPFILE" | eval "$CLIP_CMD"
cat "$TMPFILE"
rm "$TMPFILE"

