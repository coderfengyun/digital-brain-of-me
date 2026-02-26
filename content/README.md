# Content Module

This module manages your content creation pipeline from ideation to publication.

## Structure

### ideas/
Store new content ideas in `ideas.jsonl` using append-only JSONL format.

**Format:**
```json
{
  "id": "idea-XXX",
  "title": "Idea title",
  "description": "Brief description",
  "tags": ["tag1", "tag2"],
  "status": "new|in_progress|published|archived",
  "created_at": "YYYY-MM-DD",
  "priority": "low|medium|high"
}
```

### drafts/
Active writing projects. Each draft is a separate markdown file.

### published/
Archive of published content in `published.jsonl`.

**Format:**
```json
{
  "id": "post-XXX",
  "title": "Post title",
  "url": "https://...",
  "platform": "blog|twitter|linkedin",
  "published_at": "YYYY-MM-DD",
  "tags": ["tag1", "tag2"],
  "original_idea_id": "idea-XXX"
}
```

## Workflow

1. Add new ideas to `ideas/ideas.jsonl`
2. When ready to write, create a draft in `drafts/`
3. After publishing, log to `published/published.jsonl`
4. Update the original idea status to "published"
