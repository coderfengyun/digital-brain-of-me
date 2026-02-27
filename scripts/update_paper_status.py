#!/usr/bin/env python3
"""
Script to update paper reading status and metadata.

Usage:
    ./scripts/update_paper_status.py paper-20260227-001 --status reading
    ./scripts/update_paper_status.py paper-20260227-001 --status completed --claim "Your main claim"
    ./scripts/update_paper_status.py paper-20260227-001 --add-tags "deep-learning,nlp"
    ./scripts/update_paper_status.py paper-20260227-001 --relate paper-20260101-001
"""

import json
import argparse
from pathlib import Path
from datetime import datetime

# Paths
ROOT = Path(__file__).parent.parent
PAPERS_DIR = ROOT / "knowledge" / "papers"
PAPERS_JSONL = PAPERS_DIR / "papers.jsonl"


def load_papers():
    """Load all papers from papers.jsonl"""
    if not PAPERS_JSONL.exists():
        return []

    papers = []
    with open(PAPERS_JSONL, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                papers.append(json.loads(line))
    return papers


def save_papers(papers):
    """Save papers back to papers.jsonl"""
    with open(PAPERS_JSONL, 'w', encoding='utf-8') as f:
        for paper in papers:
            f.write(json.dumps(paper, ensure_ascii=False) + '\n')


def find_paper(papers, paper_id):
    """Find paper by ID"""
    for i, paper in enumerate(papers):
        if paper['id'] == paper_id:
            return i, paper
    return None, None


def update_status(paper_id, new_status, main_claim=None):
    """Update reading status of a paper"""
    papers = load_papers()
    idx, paper = find_paper(papers, paper_id)

    if paper is None:
        print(f"❌ Paper not found: {paper_id}")
        return False

    old_status = paper['reading_status']
    paper['reading_status'] = new_status

    # Update timestamps
    if new_status == 'completed' and old_status != 'completed':
        paper['read_at'] = datetime.now().strftime("%Y-%m-%d")

    # Update main claim if provided
    if main_claim:
        paper['main_claim'] = main_claim

    papers[idx] = paper
    save_papers(papers)

    print(f"✅ Updated {paper_id}")
    print(f"   Status: {old_status} → {new_status}")
    if main_claim:
        print(f"   Main claim: {main_claim}")

    return True


def add_tags(paper_id, new_tags):
    """Add tags to a paper"""
    papers = load_papers()
    idx, paper = find_paper(papers, paper_id)

    if paper is None:
        print(f"❌ Paper not found: {paper_id}")
        return False

    tags_to_add = [t.strip() for t in new_tags.split(',')]
    existing_tags = set(paper['tags'])

    for tag in tags_to_add:
        if tag not in existing_tags:
            paper['tags'].append(tag)

    papers[idx] = paper
    save_papers(papers)

    print(f"✅ Updated tags for {paper_id}")
    print(f"   Tags: {', '.join(paper['tags'])}")

    return True


def remove_tags(paper_id, tags_to_remove):
    """Remove tags from a paper"""
    papers = load_papers()
    idx, paper = find_paper(papers, paper_id)

    if paper is None:
        print(f"❌ Paper not found: {paper_id}")
        return False

    tags_list = [t.strip() for t in tags_to_remove.split(',')]
    paper['tags'] = [t for t in paper['tags'] if t not in tags_list]

    papers[idx] = paper
    save_papers(papers)

    print(f"✅ Removed tags from {paper_id}")
    print(f"   Remaining tags: {', '.join(paper['tags'])}")

    return True


def add_related_paper(paper_id, related_id):
    """Add a related paper link"""
    papers = load_papers()
    idx, paper = find_paper(papers, paper_id)

    if paper is None:
        print(f"❌ Paper not found: {paper_id}")
        return False

    # Check if related paper exists
    _, related_paper = find_paper(papers, related_id)
    if related_paper is None:
        print(f"⚠️  Warning: Related paper {related_id} not found in database")

    if related_id not in paper['related_papers']:
        paper['related_papers'].append(related_id)

    papers[idx] = paper
    save_papers(papers)

    print(f"✅ Added relation: {paper_id} → {related_id}")

    return True


def show_paper_info(paper_id):
    """Show detailed information about a paper"""
    papers = load_papers()
    _, paper = find_paper(papers, paper_id)

    if paper is None:
        print(f"❌ Paper not found: {paper_id}")
        return

    status_icons = {
        'unread': '⚪',
        'reading': '🔵',
        'completed': '✅'
    }

    icon = status_icons.get(paper['reading_status'], '❓')

    print(f"\n{icon} {paper['title']}")
    print("="*60)
    print(f"ID:            {paper['id']}")
    print(f"Authors:       {', '.join(paper['authors'])}")
    print(f"Year:          {paper.get('year', 'N/A')}")
    print(f"Venue:         {paper.get('venue', 'N/A')}")
    print(f"Status:        {paper['reading_status']}")
    print(f"Tags:          {', '.join(paper['tags']) if paper['tags'] else 'None'}")
    print(f"Added:         {paper['added_at']}")
    if paper['read_at']:
        print(f"Completed:     {paper['read_at']}")
    print(f"URL:           {paper['url']}")

    if paper.get('main_claim'):
        print(f"\nMain Claim:")
        print(f"  {paper['main_claim']}")

    if paper['related_papers']:
        print(f"\nRelated Papers:")
        for rid in paper['related_papers']:
            print(f"  - {rid}")

    note_file = PAPERS_DIR / f"{paper_id}.md"
    if note_file.exists():
        print(f"\nNote File:     {note_file}")
    else:
        print(f"\nNote File:     ❌ Not found")

    print("="*60 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description="Update paper metadata and reading status",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Update reading status
  %(prog)s paper-20260227-001 --status reading

  # Mark as completed with main claim
  %(prog)s paper-20260227-001 --status completed --claim "Transformers replace RNNs with pure attention"

  # Add tags
  %(prog)s paper-20260227-001 --add-tags "deep-learning,architecture"

  # Remove tags
  %(prog)s paper-20260227-001 --remove-tags "old-tag"

  # Link related papers
  %(prog)s paper-20260227-001 --relate paper-20260101-001

  # Show paper info
  %(prog)s paper-20260227-001 --info
        """
    )

    parser.add_argument("paper_id", help="Paper ID (e.g., paper-20260227-001)")
    parser.add_argument("--status", choices=['unread', 'reading', 'completed'],
                       help="Update reading status")
    parser.add_argument("--claim", help="Update main claim (usually with --status completed)")
    parser.add_argument("--add-tags", help="Add tags (comma-separated)")
    parser.add_argument("--remove-tags", help="Remove tags (comma-separated)")
    parser.add_argument("--relate", help="Add related paper ID")
    parser.add_argument("--info", action="store_true",
                       help="Show paper information")

    args = parser.parse_args()

    # Show info
    if args.info:
        show_paper_info(args.paper_id)
        return

    # Perform updates
    updated = False

    if args.status:
        if update_status(args.paper_id, args.status, args.claim):
            updated = True

    if args.add_tags:
        if add_tags(args.paper_id, args.add_tags):
            updated = True

    if args.remove_tags:
        if remove_tags(args.paper_id, args.remove_tags):
            updated = True

    if args.relate:
        if add_related_paper(args.paper_id, args.relate):
            updated = True

    if not updated and not args.info:
        parser.print_help()


if __name__ == "__main__":
    main()
