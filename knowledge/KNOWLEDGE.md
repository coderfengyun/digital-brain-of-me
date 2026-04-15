# Knowledge Module

This module organizes bookmarks, research notes, and learning materials.

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

### web-clippings/
Saved web pages converted to Markdown for offline reading.

## Sub-Modules

- **papers/** - Paper reading notes. See [papers/PAPERS.md](papers/PAPERS.md). Workflow in `paper-reading` skill.

## Related Top-Level Modules

- **investment/** - Investment trade journal. See [../investment/INVESTMENT.md](../investment/INVESTMENT.md)

## Usage Tips

- Tag bookmarks consistently for easy retrieval
- Link research notes to related bookmarks using bookmark IDs
- Regularly review and consolidate learning materials

## Extending

Want to add new knowledge types? Follow the [Module Creation Guide](../module-toolkit/MODULE_CREATION_GUIDE.md).
