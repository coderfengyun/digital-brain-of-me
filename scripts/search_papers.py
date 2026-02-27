#!/usr/bin/env python3
"""
Script to search and query papers from your reading list.

Usage:
    ./scripts/search_papers.py --status unread
    ./scripts/search_papers.py --tags nlp,transformer
    ./scripts/search_papers.py --keyword "attention mechanism"
    ./scripts/search_papers.py --year 2017
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


def filter_papers(papers, status=None, tags=None, year=None, keyword=None):
    """Filter papers based on criteria"""
    filtered = papers

    # Filter by reading status
    if status:
        filtered = [p for p in filtered if p['reading_status'] == status]

    # Filter by tags (any match)
    if tags:
        tag_list = [t.strip() for t in tags.split(',')]
        filtered = [
            p for p in filtered
            if any(tag in p['tags'] for tag in tag_list)
        ]

    # Filter by year
    if year:
        filtered = [p for p in filtered if p.get('year') == year]

    # Filter by keyword in title or main_claim
    if keyword:
        keyword_lower = keyword.lower()
        filtered = [
            p for p in filtered
            if keyword_lower in p['title'].lower()
            or keyword_lower in p.get('main_claim', '').lower()
        ]

    return filtered


def search_in_notes(keyword):
    """Search keyword in all paper notes"""
    results = []
    for note_file in PAPERS_DIR.glob("paper-*.md"):
        with open(note_file, 'r', encoding='utf-8') as f:
            content = f.read()
            if keyword.lower() in content.lower():
                # Extract paper ID from filename
                paper_id = note_file.stem
                # Find matching lines
                lines = content.split('\n')
                matching_lines = [
                    (i+1, line.strip())
                    for i, line in enumerate(lines)
                    if keyword.lower() in line.lower()
                ]
                results.append({
                    'paper_id': paper_id,
                    'file': note_file,
                    'matches': matching_lines[:3]  # First 3 matches
                })
    return results


def format_paper(paper, show_claim=False):
    """Format paper for display"""
    status_icons = {
        'unread': '⚪',
        'reading': '🔵',
        'completed': '✅'
    }

    icon = status_icons.get(paper['reading_status'], '❓')
    tags_str = ', '.join(paper['tags']) if paper['tags'] else 'no tags'

    output = f"{icon} [{paper['id']}] {paper['title']}\n"
    output += f"   Authors: {', '.join(paper['authors'][:3])}"
    if len(paper['authors']) > 3:
        output += f" et al."
    output += "\n"
    output += f"   Year: {paper.get('year', 'N/A')} | Venue: {paper.get('venue', 'N/A')}\n"
    output += f"   Tags: {tags_str}\n"

    if show_claim and paper.get('main_claim'):
        output += f"   📝 Claim: {paper['main_claim']}\n"

    output += f"   🔗 {paper['url']}\n"

    return output


def print_statistics(papers):
    """Print statistics about papers"""
    total = len(papers)
    by_status = {}
    by_year = {}
    all_tags = []

    for paper in papers:
        # Count by status
        status = paper['reading_status']
        by_status[status] = by_status.get(status, 0) + 1

        # Count by year
        year = paper.get('year', 'Unknown')
        by_year[year] = by_year.get(year, 0) + 1

        # Collect tags
        all_tags.extend(paper['tags'])

    # Tag frequency
    tag_freq = {}
    for tag in all_tags:
        tag_freq[tag] = tag_freq.get(tag, 0) + 1

    print("📊 Statistics")
    print("="*50)
    print(f"Total papers: {total}\n")

    print("By reading status:")
    for status in ['unread', 'reading', 'completed']:
        count = by_status.get(status, 0)
        pct = (count / total * 100) if total > 0 else 0
        print(f"  {status:12} {count:3} ({pct:5.1f}%)")

    print(f"\nBy year:")
    for year in sorted(by_year.keys(), reverse=True)[:5]:  # Top 5 years
        print(f"  {year}: {by_year[year]}")

    print(f"\nTop tags:")
    sorted_tags = sorted(tag_freq.items(), key=lambda x: x[1], reverse=True)[:10]
    for tag, count in sorted_tags:
        print(f"  {tag:20} {count}")

    print("="*50 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description="Search and query papers from your reading list",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Show all unread papers
  %(prog)s --status unread

  # Find papers with specific tags
  %(prog)s --tags nlp,transformer

  # Search by keyword in title/claim
  %(prog)s --keyword "attention"

  # Full-text search in notes
  %(prog)s --full-text "self-attention mechanism"

  # Show statistics
  %(prog)s --stats

  # Combine filters
  %(prog)s --status reading --tags nlp --year 2017
        """
    )

    parser.add_argument("--status", choices=['unread', 'reading', 'completed'],
                       help="Filter by reading status")
    parser.add_argument("--tags", help="Filter by tags (comma-separated)")
    parser.add_argument("--year", type=int, help="Filter by year")
    parser.add_argument("--keyword", help="Search keyword in title and main_claim")
    parser.add_argument("--full-text", help="Full-text search in note files")
    parser.add_argument("--show-claim", action="store_true",
                       help="Show main claim in results")
    parser.add_argument("--stats", action="store_true",
                       help="Show statistics")
    parser.add_argument("--recent", type=int, metavar="N",
                       help="Show N most recently added papers")

    args = parser.parse_args()

    # Load papers
    papers = load_papers()

    if not papers:
        print("❌ No papers found in papers.jsonl")
        return

    # Show statistics
    if args.stats:
        print_statistics(papers)
        return

    # Full-text search
    if args.full_text:
        print(f"🔍 Searching for '{args.full_text}' in notes...\n")
        results = search_in_notes(args.full_text)

        if not results:
            print("❌ No matches found")
        else:
            print(f"✅ Found in {len(results)} paper(s):\n")
            for result in results:
                print(f"📄 {result['paper_id']}")
                print(f"   File: {result['file']}")
                print(f"   Matches:")
                for line_num, line in result['matches']:
                    print(f"      Line {line_num}: {line[:80]}...")
                print()
        return

    # Show recent papers
    if args.recent:
        sorted_papers = sorted(
            papers,
            key=lambda p: p['added_at'],
            reverse=True
        )[:args.recent]
        print(f"📚 {args.recent} Most Recently Added Papers\n")
        for paper in sorted_papers:
            print(format_paper(paper, args.show_claim))
        return

    # Filter papers
    filtered = filter_papers(
        papers,
        status=args.status,
        tags=args.tags,
        year=args.year,
        keyword=args.keyword
    )

    # Display results
    if not filtered:
        print("❌ No papers match the criteria")
        return

    print(f"📚 Found {len(filtered)} paper(s)\n")
    for paper in filtered:
        print(format_paper(paper, args.show_claim))


if __name__ == "__main__":
    main()
