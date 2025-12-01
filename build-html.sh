#!/bin/bash

echo "=== Regenerating HTML files for GitHub Pages ==="

files=(
  "src/slides/00-overview-introduction.md"
  "src/slides/topic-01-google-gemini.md"
  "src/slides/topic-02-google-gem.md"
  "src/slides/topic-03-workspace-integration.md"
  "src/slides/topic-04-notebooklm.md"
  "src/slides/topic-05-gemini-in-apps.md"
  "src/slides/topic-06-ai-image-generation.md"
  "src/slides/topic-07-diagram-generation.md"
  "src/slides/topic-08-long-document-creation.md"
)

for file in "${files[@]}"; do
  basename_file=$(basename "$file" .md)
  output="dist/${basename_file}.html"

  echo "Converting ${basename_file}.md..."
  bun x @marp-team/marp-cli@latest "$file" \
    --html \
    --allow-local-files \
    -o "$output" 2>&1 | grep -E "(INFO|ERROR)" || true

  if [ -f "$output" ]; then
    size=$(ls -lh "$output" | awk '{print $5}')
    echo "  ✓ Generated: $output ($size)"
  else
    echo "  ✗ Failed: $output"
  fi
done

echo ""
echo "=== HTML generation complete ==="
ls -lh dist/*.html
