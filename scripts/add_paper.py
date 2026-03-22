#!/usr/bin/env python3
"""
Script to quickly add a new paper to the reading list.

Usage:
    ./scripts/add_paper.py "https://arxiv.org/abs/xxxx"
    ./scripts/add_paper.py "https://arxiv.org/abs/xxxx" --source paper.pdf
"""

import json
import argparse
from datetime import datetime
from pathlib import Path

# Paths
ROOT = Path(__file__).parent.parent
PAPERS_DIR = ROOT / "papers"
PAPERS_JSONL = PAPERS_DIR / "papers.jsonl"


def generate_paper_id():
    """Generate paper ID in format: paper-YYYYMMDD-XXX"""
    date_str = datetime.now().strftime("%Y%m%d")

    # Find existing papers with same date prefix
    if PAPERS_JSONL.exists():
        with open(PAPERS_JSONL, 'r', encoding='utf-8') as f:
            existing_ids = [
                json.loads(line)['id']
                for line in f
                if line.strip()
            ]

        # Extract numbers for today
        today_numbers = [
            int(pid.split('-')[-1])
            for pid in existing_ids
            if pid.startswith(f"paper-{date_str}-")
        ]

        next_num = max(today_numbers, default=0) + 1
    else:
        next_num = 1

    return f"paper-{date_str}-{next_num:03d}"


def add_paper(url, source=""):
    """Add a new paper to papers.jsonl"""

    paper_id = generate_paper_id()

    # Create paper folder
    paper_dir = PAPERS_DIR / paper_id
    paper_dir.mkdir(parents=True, exist_ok=True)

    paper_data = {
        "id": paper_id,
        "url": url,
        "source": source,
        "notes": ""
    }

    # Append to papers.jsonl
    with open(PAPERS_JSONL, 'a', encoding='utf-8') as f:
        f.write(json.dumps(paper_data, ensure_ascii=False) + '\n')

    print(f"Added paper: {paper_id}")
    print(f"  URL: {url}")
    print(f"  Folder: {paper_dir}")
    print(f"\nNext steps:")
    print(f"  1. Download source to {paper_dir}/")
    print(f"  2. Read and create notes at {paper_dir}/notes.md")
    print(f"  3. Update source/notes fields in papers.jsonl")

    return paper_id


def main():
    parser = argparse.ArgumentParser(
        description="Add a new paper to your reading list",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "https://arxiv.org/abs/1706.03762"
  %(prog)s "https://arxiv.org/abs/1706.03762" --source "paper-XXXXXXXX-XXX/paper.html"
        """
    )

    parser.add_argument("url", help="Paper URL")
    parser.add_argument("--source", default="", help="Local source document path")

    args = parser.parse_args()

    # Ensure papers directory exists
    PAPERS_DIR.mkdir(parents=True, exist_ok=True)

    add_paper(url=args.url, source=args.source)


if __name__ == "__main__":
    main()
