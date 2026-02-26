#!/usr/bin/env python3
"""
Idea to Draft Expander

Helps expand a content idea into a structured draft by:
- Creating a draft file from an idea
- Pulling in related bookmarks and research
- Suggesting structure and talking points
"""

import json
import sys
from datetime import datetime
from pathlib import Path

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

def find_related_content(tags):
    """Find bookmarks and research related to tags"""
    bookmarks = load_jsonl('knowledge/bookmarks/bookmarks.jsonl')

    related = []
    for bm in bookmarks:
        bm_tags = set(bm.get('tags', []))
        if bm_tags.intersection(set(tags)):
            related.append(bm)

    return related

def create_draft_from_idea(idea_id):
    """Create a draft markdown file from an idea"""
    ideas = load_jsonl('content/ideas/ideas.jsonl')

    # Find the idea
    idea = None
    for item in ideas:
        if item.get('id') == idea_id:
            idea = item
            break

    if not idea:
        print(f"Error: Idea '{idea_id}' not found")
        return

    # Get related content
    related = find_related_content(idea.get('tags', []))

    # Create draft
    title = idea.get('title', 'Untitled')
    slug = title.lower().replace(' ', '-').replace('/', '-')
    draft_path = f"content/drafts/{slug}.md"

    content = f"""# {title}

**Status**: Draft
**Created**: {datetime.now().strftime('%Y-%m-%d')}
**Tags**: {', '.join(idea.get('tags', []))}
**Original Idea**: {idea_id}

---

## Overview

{idea.get('description', 'Add description here...')}

## Key Points

-
-
-

## Structure

### Introduction

### Main Content

#### Section 1

#### Section 2

#### Section 3

### Conclusion

## Related Resources

"""

    # Add related bookmarks
    if related:
        for bm in related[:5]:
            content += f"\n- [{bm.get('title', 'Untitled')}]({bm.get('url', '#')})"
            if bm.get('description'):
                content += f"\n  {bm.get('description')}"

    content += "\n\n## Notes\n\n"

    # Write draft file
    with open(draft_path, 'w') as f:
        f.write(content)

    print(f"Draft created: {draft_path}")
    print(f"\nFound {len(related)} related bookmarks to reference")
    print("\nNext steps:")
    print("1. Fill in the key points and structure")
    print("2. Start writing the main content")
    print("3. Review and edit")
    print("4. Publish!")

    # Update idea status
    updated_ideas = []
    for item in ideas:
        if item.get('id') == idea_id:
            item['status'] = 'in_progress'
        updated_ideas.append(item)

    with open('content/ideas/ideas.jsonl', 'w') as f:
        for item in updated_ideas:
            f.write(json.dumps(item) + '\n')

    print(f"\nIdea status updated to 'in_progress'")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python idea_to_draft.py <idea-id>")
        print("\nAvailable ideas:")

        ideas = load_jsonl('content/ideas/ideas.jsonl')
        new_ideas = [i for i in ideas if i.get('status') == 'new']

        if not new_ideas:
            print("  No new ideas available")
        else:
            for idea in new_ideas:
                print(f"  - {idea.get('id')}: {idea.get('title')}")
        sys.exit(1)

    idea_id = sys.argv[1]
    create_draft_from_idea(idea_id)
