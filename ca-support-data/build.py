"""
build.py — converts all .md files in /articles into articles_all.jsonl
Run automatically by GitHub Actions on every push.
You never need to run or edit this file manually.
"""

import json
import os
import re

ARTICLES_DIR = "articles"
OUTPUT_FILE  = "articles_all.jsonl"

def parse_md(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Extract front matter if present (--- key: value ---)
    title    = ""
    url      = ""
    category = ""
    body     = content

    front_matter_match = re.match(r"^---\n(.*?)\n---\n", content, re.DOTALL)
    if front_matter_match:
        fm = front_matter_match.group(1)
        body = content[front_matter_match.end():]
        title_m    = re.search(r"^title:\s*(.+)$",    fm, re.MULTILINE)
        url_m      = re.search(r"^url:\s*(.+)$",      fm, re.MULTILINE)
        category_m = re.search(r"^category:\s*(.+)$", fm, re.MULTILINE)
        if title_m:    title    = title_m.group(1).strip()
        if url_m:      url      = url_m.group(1).strip()
        if category_m: category = category_m.group(1).strip()

    # Fall back to first H1 as title
    if not title:
        h1 = re.search(r"^#\s+(.+)$", body, re.MULTILINE)
        if h1:
            title = h1.group(1).strip()
            body  = body[h1.end():].strip()

    # Use filename slug as fallback title
    if not title:
        title = os.path.splitext(os.path.basename(filepath))[0].replace("-", " ").title()

    return {
        "id":         os.path.splitext(os.path.basename(filepath))[0],
        "title":      title,
        "url":        url,
        "categories": [category] if category else [],
        "body":       body.strip(),
        "source":     filepath
    }

def main():
    if not os.path.isdir(ARTICLES_DIR):
        print(f"No '{ARTICLES_DIR}' folder found.")
        return

    md_files = sorted([
        os.path.join(ARTICLES_DIR, f)
        for f in os.listdir(ARTICLES_DIR)
        if f.endswith(".md")
    ])

    if not md_files:
        print("No .md files found in articles/")
        return

    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        for filepath in md_files:
            try:
                record = parse_md(filepath)
                out.write(json.dumps(record, ensure_ascii=False) + "\n")
                print(f"  ✓ {filepath}  →  {record['title']}")
            except Exception as e:
                print(f"  ✗ {filepath}  →  ERROR: {e}")

    print(f"\nDone! {len(md_files)} articles written to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
