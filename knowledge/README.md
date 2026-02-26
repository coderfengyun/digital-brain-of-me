# Knowledge Module

This module organizes your learning materials, bookmarks, and research.

## Structure

### bookmarks/
Save interesting links and resources in `bookmarks.jsonl`.

**Format:**
```json
{
  "id": "bm-XXX",
  "url": "https://...",
  "title": "Resource title",
  "description": "Brief description",
  "tags": ["tag1", "tag2"],
  "saved_at": "YYYY-MM-DD",
  "category": "article|video|tool|paper|documentation"
}
```

### research/
Deep research notes on specific topics. Create separate markdown files for each research area.

### learning/
Track courses, books, and skills you're developing in `courses.yaml`.

## Usage Tips

- Tag bookmarks consistently for easy retrieval
- Link research notes to related bookmarks using bookmark IDs
- Regularly review and consolidate learning materials
- Use research notes to synthesize information from multiple sources
