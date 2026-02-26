#!/usr/bin/env python3
"""
Content Ideas Generator

Suggests content ideas based on:
- Recent bookmarks
- Research notes
- Knowledge gaps in your learning
"""

import json
import random
from pathlib import Path
from collections import Counter

def load_jsonl(filepath):
    """Load JSONL file and return list of records"""
    records = []
    if not Path(filepath).exists():
        return records

    with open(filepath, 'r') as f:
        for line in f:
            if line.strip():
                records.append(json.loads(line))
    return records

def get_trending_tags(records, tag_field='tags', limit=5):
    """Get most common tags from records"""
    tag_counter = Counter()

    for record in records:
        tags = record.get(tag_field, [])
        tag_counter.update(tags)

    return [tag for tag, count in tag_counter.most_common(limit)]

def suggest_content_ideas():
    """Generate content ideas from your knowledge base"""
    print("# Content Ideas Suggestions")
    print("=" * 50)
    print()

    # Load data
    bookmarks = load_jsonl('knowledge/bookmarks/bookmarks.jsonl')
    ideas = load_jsonl('content/ideas/ideas.jsonl')
    published = load_jsonl('content/published/published.jsonl')

    # Get trending topics from bookmarks
    print("## Based on Your Recent Bookmarks:")
    recent_bookmarks = sorted(bookmarks, key=lambda x: x.get('saved_at', ''), reverse=True)[:10]

    for bm in recent_bookmarks[:5]:
        print(f"\n### From: {bm.get('title', 'Untitled')}")
        print(f"  Idea: Write about {', '.join(bm.get('tags', ['this topic']))}")
        print(f"  Angle: Share your perspective on {bm.get('description', 'this concept')}")

    print("\n## Trending Topics in Your Knowledge Base:")
    trending_tags = get_trending_tags(bookmarks)

    for tag in trending_tags:
        print(f"\n### Topic: {tag}")
        related_bookmarks = [bm for bm in bookmarks if tag in bm.get('tags', [])]
        print(f"  You have {len(related_bookmarks)} bookmarks on this topic")
        print(f"  Idea: Create a comprehensive guide or tutorial about {tag}")

    print("\n## Ideas Waiting to Be Written:")
    pending_ideas = [idea for idea in ideas if idea.get('status') == 'new']

    if pending_ideas:
        for idea in sorted(pending_ideas, key=lambda x: x.get('priority', 'medium'), reverse=True)[:5]:
            print(f"\n### {idea.get('title', 'Untitled')}")
            print(f"  Priority: {idea.get('priority', 'medium')}")
            print(f"  Description: {idea.get('description', 'No description')}")
    else:
        print("  No pending ideas. Time to brainstorm!")

    print("\n## Topics You Haven't Covered Yet:")
    published_tags = get_trending_tags(published)
    bookmark_tags = get_trending_tags(bookmarks, limit=10)

    uncovered = set(bookmark_tags) - set(published_tags)

    for tag in list(uncovered)[:5]:
        print(f"  - {tag}")

    print("\n" + "=" * 50)
    print("Pick an idea and start writing!")

if __name__ == '__main__':
    suggest_content_ideas()
