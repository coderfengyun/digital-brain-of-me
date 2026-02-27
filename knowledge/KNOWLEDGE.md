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

### papers/ (now at top-level)
Systematic academic paper reading with narrative-driven approach. See [../papers/PAPERS.md](../papers/PAPERS.md) for details.

**Format:**
- `papers.jsonl`: Paper metadata (title, authors, status, tags)
- `paper-YYYYMMDD-XXX.md`: Detailed reading notes focusing on narrative, evidence, and critical thinking

## Usage Tips

- Tag bookmarks consistently for easy retrieval
- Link research notes to related bookmarks using bookmark IDs
- Link papers to related bookmarks and research notes using IDs
- Regularly review and consolidate learning materials
- Use research notes to synthesize information from multiple sources
- When reading papers, focus on understanding the narrative first, then verify with data

## Extending the Knowledge Module

Want to add new knowledge types? Follow the [Module Creation Guide](../module_operation/MODULE_CREATION_GUIDE.md).

Examples of modules you could add:
- **courses/**: Track online courses and MOOCs
- **podcasts/**: Save podcast episodes with notes
- **videos/**: Technical talks and tutorials
- **tools/**: Software tools and utilities you use
- **snippets/**: Code snippets and recipes

After creating a new module, verify integration:
```bash
python module_operation/check_module_integration.py <module_name> <keyword>
```
