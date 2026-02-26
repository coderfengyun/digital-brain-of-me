# Digital Brain - Claude Instructions

This is a Digital Brain personal operating system. When working in this project:

## Core Rules

1. **Always read identity/voice/style.md before writing any content** - Match the user's authentic voice
2. **Append to JSONL files, never overwrite** - Preserve history
3. **Update timestamps** when modifying tracked data
4. **Cross-reference modules** - Knowledge informs content, network informs operations

## Quick Reference

- **Writing content**: Read `identity/voice/style.md` first, then create drafts in `content/drafts/`
- **Looking up contacts**: Search `network/contacts/contacts.jsonl`, check `network/relationships/interactions.jsonl` for history
- **Content ideas**: Check `content/ideas/ideas.jsonl`, run `scripts/content_ideas.py`
- **Task management**: Use `operations/tasks/tasks.jsonl`, align with `operations/goals/goals.yaml`
- **Weekly review**: Run `scripts/weekly_review.py`

## File Conventions

- `.jsonl` files: One JSON object per line, append-only
- `.md` files: Human-readable, freely editable
- `.yaml` files: Configuration and structured data
- Template entries in README files: Reference formats, don't modify

## When User Asks To...

| Request | Action |
|---------|--------|
| "Write a post about X" | Read `voice/style.md` → Draft → Match voice patterns |
| "Prepare for meeting with Y" | Look up contact → Get interactions → Summarize |
| "What should I create?" | Run `content_ideas.py` → Check ideas.jsonl |
| "Add contact Z" | Append to `contacts.jsonl` with full schema |
| "Weekly review" | Run `weekly_review.py` → Present insights |
| "Save this bookmark" | Append to `bookmarks/bookmarks.jsonl` |
| "Add a task" | Append to `tasks/tasks.jsonl` with priority |
| "Track a goal" | Update `goals/goals.yaml` with progress |

## Module Loading Strategy

Use **progressive disclosure**:

1. **Always Load** (L1):
   - `identity/brand/profile.yaml`
   - `identity/voice/style.md`

2. **Load on Content Tasks** (L2):
   - `content/ideas/ideas.jsonl`
   - `content/published/published.jsonl`
   - `knowledge/bookmarks/bookmarks.jsonl`

3. **Load on Network Tasks** (L2):
   - `network/contacts/contacts.jsonl`
   - `network/relationships/interactions.jsonl`

4. **Load on Operations Tasks** (L2):
   - `operations/tasks/tasks.jsonl`
   - `operations/goals/goals.yaml`
   - `operations/metrics/weekly.jsonl`

5. **Load on Demand** (L3):
   - Individual draft files
   - Research notes
   - Meeting records

## Data Entry Best Practices

### Adding Content Ideas

```json
{
  "id": "idea-XXX",
  "title": "Descriptive title",
  "description": "Brief description",
  "tags": ["tag1", "tag2"],
  "status": "new",
  "created_at": "YYYY-MM-DD",
  "priority": "high|medium|low"
}
```

### Adding Bookmarks

```json
{
  "id": "bm-XXX",
  "url": "https://...",
  "title": "Resource title",
  "description": "What this is about",
  "tags": ["tag1", "tag2"],
  "saved_at": "YYYY-MM-DD",
  "category": "article|video|tool|paper|documentation"
}
```

### Adding Contacts

```json
{
  "id": "contact-XXX",
  "name": "Full Name",
  "relationship": "colleague|mentor|client|friend|acquaintance",
  "tags": ["tag1", "tag2"],
  "met_at": "YYYY-MM-DD",
  "last_contact": "YYYY-MM-DD",
  "notes": "Context about this person",
  "links": {
    "twitter": "",
    "linkedin": "",
    "email": "",
    "website": ""
  }
}
```

### Logging Interactions

```json
{
  "id": "interaction-XXX",
  "contact_id": "contact-XXX",
  "date": "YYYY-MM-DD",
  "type": "meeting|email|call|message|event",
  "summary": "What you discussed",
  "follow_up": "Any action items"
}
```

### Adding Tasks

```json
{
  "id": "task-XXX",
  "title": "Task description",
  "description": "Detailed description",
  "status": "todo|in_progress|done|blocked",
  "priority": "high|medium|low",
  "created_at": "YYYY-MM-DD",
  "due_date": "YYYY-MM-DD",
  "tags": ["tag1", "tag2"],
  "related_goal": "goal reference"
}
```

## Automation Scripts

Run these to generate insights:

- `python scripts/weekly_review.py` - Weekly productivity summary
- `python scripts/content_ideas.py` - Content suggestions from bookmarks
- `python scripts/stale_contacts.py` - Identify people to reconnect with
- `python scripts/idea_to_draft.py <idea-id>` - Expand idea into draft

## Voice Consistency Checklist

Before generating any content, verify:

1. ✅ Read `identity/voice/style.md`
2. ✅ Checked `identity/brand/profile.yaml` for topic alignment
3. ✅ Reviewed similar content in `content/published/published.jsonl`
4. ✅ Applied voice patterns (tone, vocabulary, structure)
5. ✅ Maintained authenticity and brand positioning

## Context Engineering Principles

This system follows these principles:

1. **Progressive Disclosure**: Load only what's needed for current task
2. **Append-Only**: Never delete, always add (mark as archived if needed)
3. **Cross-Reference**: Link related data across modules
4. **Voice-First**: Identity always loaded before content generation
5. **Historical Analysis**: Past data informs future decisions

## Error Prevention

❌ **DON'T**:
- Delete entries from JSONL files
- Overwrite existing data without reading first
- Generate content without reading voice.md
- Modify template entries
- Break JSONL format (one object per line)

✅ **DO**:
- Append new entries to JSONL files
- Update timestamps when modifying
- Read identity files before content creation
- Cross-reference related data
- Preserve complete history

---

**Remember**: This is a personal operating system. Maintain the user's authentic voice, preserve their data history, and help them build intentional systems for content, relationships, and productivity.
