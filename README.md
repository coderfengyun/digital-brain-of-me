# Digital Brain - Personal Knowledge Management System

A structured, AI-assisted knowledge management system for managing your personal brand, content creation, learning, relationships, and productivity.

Inspired by [Agent Skills for Context Engineering](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering/tree/main/examples/digital-brain-skill).

## 🧠 What is This?

Your Digital Brain is a file-based system that helps you:

- **Capture** ideas, bookmarks, contacts, and tasks
- **Organize** information into clear, queryable structures
- **Generate** insights through automated analysis
- **Create** content backed by your accumulated knowledge
- **Maintain** relationships and track your goals

## 📁 Structure

```
digital-brain-of-me/
├── identity/          # Your personal brand and voice
│   ├── brand/        # Profile, values, expertise
│   └── voice/        # Writing style and principles
├── content/          # Content creation pipeline
│   ├── ideas/        # Content ideas (JSONL)
│   ├── drafts/       # Work in progress (Markdown)
│   └── published/    # Published content log (JSONL)
├── knowledge/        # Learning and research
│   ├── bookmarks/    # Saved links (JSONL)
│   ├── research/     # Deep research notes (Markdown)
│   └── learning/     # Courses, books, skills (YAML)
├── network/          # Relationship management
│   ├── contacts/     # Professional network (JSONL)
│   └── relationships/ # Interactions log (JSONL)
├── operations/       # Goals and productivity
│   ├── goals/        # Yearly/quarterly/monthly goals (YAML)
│   ├── tasks/        # Action items (JSONL)
│   ├── meetings/     # Meeting notes (JSONL)
│   └── metrics/      # Weekly metrics (JSONL)
└── scripts/          # Automation tools
    ├── weekly_review.py    # Generate weekly summary
    ├── content_ideas.py    # Suggest what to write
    ├── stale_contacts.py   # Who to reconnect with
    └── idea_to_draft.py    # Expand ideas into drafts
```

## 🚀 Quick Start

### 1. Set Up Your Identity

Edit your profile and voice:

```bash
# Your personal brand
open identity/brand/profile.yaml

# Your writing style
open identity/voice/style.md

# Your principles
open identity/voice/principles.md
```

### 2. Start Capturing Information

#### Add a Content Idea

```bash
echo '{"id": "idea-002", "title": "How to build a digital brain", "description": "Share my setup and workflow", "tags": ["productivity", "AI"], "status": "new", "created_at": "2026-02-26", "priority": "high"}' >> content/ideas/ideas.jsonl
```

#### Save a Bookmark

```bash
echo '{"id": "bm-002", "url": "https://example.com/article", "title": "Great article on PKM", "description": "Personal knowledge management strategies", "tags": ["productivity", "learning"], "saved_at": "2026-02-26", "category": "article"}' >> knowledge/bookmarks/bookmarks.jsonl
```

#### Add a Contact

```bash
echo '{"id": "contact-002", "name": "Jane Smith", "relationship": "colleague", "tags": ["AI", "research"], "met_at": "2026-02-26", "last_contact": "2026-02-26", "notes": "Met at AI conference, works on LLM agents", "links": {"twitter": "@janesmith", "linkedin": "", "email": "jane@example.com"}}' >> network/contacts/contacts.jsonl
```

#### Add a Task

```bash
echo '{"id": "task-002", "title": "Write blog post about digital brain", "description": "", "status": "todo", "priority": "high", "created_at": "2026-02-26", "due_date": "2026-03-05", "tags": ["content", "writing"], "related_goal": ""}' >> operations/tasks/tasks.jsonl
```

### 3. Use Automation Scripts

#### Generate Weekly Review

```bash
python scripts/weekly_review.py
```

#### Get Content Ideas

```bash
python scripts/content_ideas.py
```

#### Find Stale Contacts

```bash
python scripts/stale_contacts.py
```

#### Turn Idea into Draft

```bash
python scripts/idea_to_draft.py idea-002
```

## 🤖 Using with Claude Code

This system includes a Claude Code skill for AI-assisted knowledge management.

### Skill Location

The skill is defined in `.claude/skills/digital-brain/`

### How to Use

When working with Claude Code, you can say things like:

- "Add a content idea about AI agents"
- "Save this article to my bookmarks: https://example.com"
- "I met John at the conference, add him as a contact"
- "What should I write about next?"
- "Generate my weekly review"
- "Who should I reach out to?"
- "Turn idea-003 into a draft"

Claude will automatically:
- Read your identity files to understand your voice
- Add entries in the correct format
- Cross-reference related information
- Run automation scripts
- Provide insights and suggestions

## 🎯 Design Principles

### 1. Progressive Disclosure
Only load information needed for the current task. Not all modules are relevant all the time.

### 2. Append-Only Data
JSONL files preserve history. New entries are appended, never deleted. This maintains a complete record over time.

### 3. Module Separation
Five independent domains (Identity, Content, Knowledge, Network, Operations) that can be used independently or together.

### 4. Voice-First
Your identity module is always loaded first to ensure AI assistance matches your personal brand and style.

## 📝 File Format Guide

### JSONL (JSON Lines)
Used for: bookmarks, contacts, tasks, interactions, metrics

**Why**: Append-only, preserves history, easy to parse, AI-friendly

**Example**:
```json
{"id": "bm-001", "url": "...", "title": "...", "tags": ["tag1"], "saved_at": "2026-02-26"}
{"id": "bm-002", "url": "...", "title": "...", "tags": ["tag2"], "saved_at": "2026-02-26"}
```

### YAML
Used for: profile, goals, learning progress

**Why**: Hierarchical data, human-readable, good for nested structures

**Example**:
```yaml
yearly_goals:
  - goal: "Launch my side project"
    status: "in_progress"
    progress: 60
```

### Markdown
Used for: drafts, research notes, style guide

**Why**: Easy to write, version-controllable, supports rich formatting

## 🔄 Typical Workflows

### Content Creation Workflow

1. **Capture**: Log idea in `content/ideas/ideas.jsonl`
2. **Research**: Save related bookmarks in `knowledge/bookmarks/`
3. **Draft**: Run `idea_to_draft.py` to create structured draft
4. **Write**: Edit draft in `content/drafts/`
5. **Publish**: Log to `content/published/published.jsonl`
6. **Update**: Mark original idea as "published"

### Weekly Review Workflow

1. **Generate**: Run `weekly_review.py`
2. **Reflect**: Review accomplishments and metrics
3. **Plan**: Update goals in `operations/goals/goals.yaml`
4. **Reach Out**: Check `stale_contacts.py` for relationships to maintain
5. **Create**: Use `content_ideas.py` for next week's content

### Relationship Maintenance Workflow

1. **Meet Someone**: Add to `network/contacts/contacts.jsonl`
2. **Follow Up**: Log interaction in `network/relationships/interactions.jsonl`
3. **Stay in Touch**: Regularly run `stale_contacts.py`
4. **Update**: Keep `last_contact` current

## 🛠️ Customization

### Add Custom Scripts

Create new Python scripts in `scripts/` for custom analysis:

```python
#!/usr/bin/env python3
import json
from pathlib import Path

def load_jsonl(filepath):
    records = []
    with open(filepath, 'r') as f:
        for line in f:
            if line.strip():
                records.append(json.loads(line))
    return records

# Your custom logic here
```

### Add New Modules

Create new directories for domain-specific knowledge:

```bash
mkdir -p projects/active projects/archived
```

### Extend Data Schemas

Add new fields to JSONL entries as needed. The format is flexible.

## 🌟 Best Practices

1. **Be Consistent**: Use tags consistently across modules
2. **Update Regularly**: Keep `last_contact` dates current
3. **Link Related Items**: Reference IDs across modules (e.g., link tasks to goals)
4. **Review Weekly**: Run weekly review to maintain awareness
5. **Backup**: This is plain text - commit to git regularly
6. **Start Small**: Don't fill everything at once, grow organically
7. **Use AI Assistance**: Let Claude help with data entry and analysis

## 📚 Learn More

- [Original Digital Brain Skill](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering/tree/main/examples/digital-brain-skill)
- [Context Engineering Tweet](https://x.com/koylanai/status/2025286163641118915)

## 📄 License

MIT License - Feel free to adapt this system for your own needs.

---

**Built with**: Claude Code, Python, Markdown, JSONL, YAML
**Maintained by**: You!