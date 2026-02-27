#!/usr/bin/env python3
"""
Script to quickly add a new paper to the reading list.

Usage:
    ./scripts/add_paper.py "Paper Title" "https://arxiv.org/abs/xxxx" --tags nlp,transformer
    ./scripts/add_paper.py --interactive
"""

import json
import argparse
from datetime import datetime
from pathlib import Path
import re

# Paths
ROOT = Path(__file__).parent.parent
PAPERS_DIR = ROOT / "knowledge" / "papers"
PAPERS_JSONL = PAPERS_DIR / "papers.jsonl"
TEMPLATE_PATH = PAPERS_DIR / "TEMPLATE.md"


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


def slugify(text):
    """Convert text to URL-friendly slug"""
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text[:50]  # Limit length


def add_paper(title, url, authors=None, year=None, venue=None, tags=None, pdf_path=None):
    """Add a new paper to papers.jsonl and create note file"""

    paper_id = generate_paper_id()

    # Prepare paper metadata
    paper_data = {
        "id": paper_id,
        "title": title,
        "authors": authors or [],
        "year": year or datetime.now().year,
        "venue": venue or "",
        "url": url,
        "pdf_path": pdf_path or "",
        "tags": tags or [],
        "reading_status": "unread",
        "main_claim": "",
        "added_at": datetime.now().strftime("%Y-%m-%d"),
        "read_at": "",
        "related_papers": []
    }

    # Append to papers.jsonl
    with open(PAPERS_JSONL, 'a', encoding='utf-8') as f:
        f.write(json.dumps(paper_data, ensure_ascii=False) + '\n')

    # Create note file from template
    note_filename = f"{paper_id}.md"
    note_path = PAPERS_DIR / note_filename

    # Read template
    if TEMPLATE_PATH.exists():
        with open(TEMPLATE_PATH, 'r', encoding='utf-8') as f:
            template = f.read()

        # Replace placeholders
        authors_str = ", ".join(authors) if authors else "作者名"
        tags_str = " ".join([f"`#{tag}`" for tag in (tags or ["tag1", "tag2"])])

        note_content = template.replace("paper-YYYYMMDD-XXX", paper_id)
        note_content = note_content.replace("[论文标题]", title)
        note_content = note_content.replace("作者1, 作者2, 作者3", authors_str)
        note_content = note_content.replace("YYYY", str(year or datetime.now().year))
        note_content = note_content.replace("会议/期刊名称", venue or "Venue")
        note_content = note_content.replace("(url)", f"({url})")
        note_content = note_content.replace("`#tag1` `#tag2` `#tag3`", tags_str)
        note_content = note_content.replace("🔵 Reading / ✅ Completed", "⚪ Unread")

        with open(note_path, 'w', encoding='utf-8') as f:
            f.write(note_content)

    print(f"✅ Added paper: {paper_id}")
    print(f"   Title: {title}")
    print(f"   Note: {note_path}")
    print(f"\n📖 Next steps:")
    print(f"   1. Open {note_path}")
    print(f"   2. Start Phase 1: Extract the narrative (15-30 min)")
    print(f"   3. Update reading_status to 'reading' in papers.jsonl")

    return paper_id


def interactive_add():
    """Interactive mode to add paper"""
    print("📝 Add New Paper (Interactive Mode)\n")

    title = input("Paper Title: ").strip()
    if not title:
        print("❌ Title is required")
        return

    url = input("URL (arXiv, PDF, etc.): ").strip()
    if not url:
        print("❌ URL is required")
        return

    authors_input = input("Authors (comma-separated, optional): ").strip()
    authors = [a.strip() for a in authors_input.split(',')] if authors_input else []

    year_input = input(f"Year (default: {datetime.now().year}): ").strip()
    year = int(year_input) if year_input else datetime.now().year

    venue = input("Venue/Conference (optional): ").strip()

    tags_input = input("Tags (comma-separated, e.g., nlp,transformer): ").strip()
    tags = [t.strip() for t in tags_input.split(',')] if tags_input else []

    pdf_path = input("Local PDF path (optional): ").strip()

    print("\n" + "="*50)
    print("Summary:")
    print(f"  Title: {title}")
    print(f"  Authors: {', '.join(authors) if authors else 'N/A'}")
    print(f"  Year: {year}")
    print(f"  Venue: {venue or 'N/A'}")
    print(f"  URL: {url}")
    print(f"  Tags: {', '.join(tags) if tags else 'N/A'}")
    print("="*50 + "\n")

    confirm = input("Add this paper? (y/n): ").strip().lower()
    if confirm == 'y':
        add_paper(title, url, authors, year, venue, tags, pdf_path)
    else:
        print("❌ Cancelled")


def main():
    parser = argparse.ArgumentParser(
        description="Add a new paper to your reading list",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Quick add
  %(prog)s "Attention Is All You Need" "https://arxiv.org/abs/1706.03762" --tags nlp,transformer --year 2017

  # Interactive mode
  %(prog)s --interactive
        """
    )

    parser.add_argument("title", nargs='?', help="Paper title")
    parser.add_argument("url", nargs='?', help="Paper URL")
    parser.add_argument("--authors", help="Comma-separated authors")
    parser.add_argument("--year", type=int, help="Publication year")
    parser.add_argument("--venue", help="Conference/Journal name")
    parser.add_argument("--tags", help="Comma-separated tags")
    parser.add_argument("--pdf", help="Local PDF path")
    parser.add_argument("--interactive", "-i", action="store_true",
                       help="Interactive mode")

    args = parser.parse_args()

    # Ensure papers directory exists
    PAPERS_DIR.mkdir(parents=True, exist_ok=True)

    if args.interactive:
        interactive_add()
    elif args.title and args.url:
        authors = args.authors.split(',') if args.authors else []
        tags = args.tags.split(',') if args.tags else []
        add_paper(
            title=args.title,
            url=args.url,
            authors=[a.strip() for a in authors],
            year=args.year,
            venue=args.venue,
            tags=[t.strip() for t in tags],
            pdf_path=args.pdf
        )
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
