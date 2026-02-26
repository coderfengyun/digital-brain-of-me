# Digital Brain Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     DIGITAL BRAIN SYSTEM                     │
├─────────────────────────────────────────────────────────────┤
│  AI-Assisted Personal Knowledge Management & Productivity   │
└─────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│   CAPTURE     │    │   ORGANIZE    │    │   GENERATE    │
├───────────────┤    ├───────────────┤    ├───────────────┤
│ • Ideas       │───▶│ • Modules     │───▶│ • Insights    │
│ • Bookmarks   │    │ • Tags        │    │ • Reviews     │
│ • Contacts    │    │ • Links       │    │ • Content     │
│ • Tasks       │    │ • Timelines   │    │ • Suggestions │
└───────────────┘    └───────────────┘    └───────────────┘
```

## Five Core Modules

### 1. Identity Module 🎭

**Purpose**: Define your personal brand and voice

```
identity/
├── brand/
│   └── profile.yaml          # Who you are
└── voice/
    ├── style.md              # How you communicate
    └── principles.md         # What you stand for
```

**Key Concept**: Voice-First Architecture
- Always loaded first by AI assistant
- Ensures consistency across all interactions
- Guides content creation and communication

---

### 2. Content Module ✍️

**Purpose**: Manage content creation pipeline from idea to publication

```
content/
├── ideas/
│   └── ideas.jsonl           # Idea backlog (append-only)
├── drafts/
│   └── *.md                  # Work in progress
└── published/
    └── published.jsonl       # Publication log
```

**Workflow**:
```
IDEA → RESEARCH → DRAFT → EDIT → PUBLISH → LOG
  ↓       ↓         ↓       ↓       ↓       ↓
 new  gathering   writing editing  done  archived
```

**Data Flow**:
1. Capture idea in `ideas.jsonl`
2. Collect related bookmarks from Knowledge module
3. Generate draft with `idea_to_draft.py`
4. Write and edit markdown file
5. Publish externally
6. Log to `published.jsonl`
7. Update idea status to "published"

---

### 3. Knowledge Module 📚

**Purpose**: Organize learning materials and research

```
knowledge/
├── bookmarks/
│   └── bookmarks.jsonl       # Saved links
├── research/
│   └── notes.md              # Deep dives
└── learning/
    └── courses.yaml          # Books, courses, skills
```

**Information Flow**:
```
DISCOVER → SAVE → RESEARCH → SYNTHESIZE → CREATE
   ↓        ↓       ↓           ↓           ↓
  Web   Bookmark  Notes     Insights    Content
        tagging  linking  connecting    ideas
```

**Key Features**:
- Tag-based organization
- Cross-referencing with content ideas
- Historical preservation (append-only)

---

### 4. Network Module 🤝

**Purpose**: Maintain professional relationships

```
network/
├── contacts/
│   └── contacts.jsonl        # People you know
└── relationships/
    └── interactions.jsonl    # Interaction history
```

**Relationship Lifecycle**:
```
MEET → CONNECT → INTERACT → MAINTAIN → DEEPEN
 ↓       ↓         ↓           ↓          ↓
Add   Exchange  Log       Schedule    Collaborate
    first touch         follow-up
```

**Automation**:
- `stale_contacts.py` identifies neglected relationships
- Suggests who to reach out to
- Tracks interaction frequency

---

### 5. Operations Module ⚙️

**Purpose**: Track goals, tasks, and productivity

```
operations/
├── goals/
│   └── goals.yaml            # Hierarchy of goals
├── tasks/
│   └── tasks.jsonl           # Action items
├── meetings/
│   └── meetings.jsonl        # Meeting notes
└── metrics/
    └── weekly.jsonl          # Performance tracking
```

**Goal Hierarchy**:
```
YEARLY GOALS
    ↓
QUARTERLY GOALS
    ↓
MONTHLY GOALS
    ↓
WEEKLY TASKS
    ↓
DAILY ACTIONS
```

**Metrics Tracking**:
- Content published
- Tasks completed
- Meetings attended
- New contacts made
- Learning hours

---

## Data Architecture

### File Format Strategy

| Format | Use Case | Benefits |
|--------|----------|----------|
| **JSONL** | Time-series data (bookmarks, contacts, tasks) | Append-only, preserves history, easy parsing |
| **YAML** | Hierarchical data (goals, profile) | Human-readable, supports nesting |
| **Markdown** | Narrative content (drafts, notes) | Easy editing, version control, rich formatting |

### Append-Only Pattern

**Philosophy**: Never delete, always add

```jsonl
// Old entry - never modified
{"id": "task-001", "status": "todo", "created_at": "2026-01-01"}

// New entry - status change logged
{"id": "task-001", "status": "done", "completed_at": "2026-02-26"}
```

**Benefits**:
- Complete history
- Audit trail
- Time-travel queries
- No data loss

### Cross-Module Linking

**Example**: Content creation workflow

```
content/ideas/ideas.jsonl
{"id": "idea-123", "tags": ["AI", "productivity"]}
           ↓
knowledge/bookmarks/bookmarks.jsonl
{"id": "bm-456", "tags": ["AI", "productivity"]}
           ↓
content/drafts/ai-productivity.md
"See bookmark bm-456 for reference"
           ↓
operations/tasks/tasks.jsonl
{"id": "task-789", "related_goal": "goal-content-creation"}
```

---

## Automation Layer

### Four Core Scripts

#### 1. weekly_review.py
**Input**: All JSONL files
**Output**: Weekly summary
**Purpose**: Track productivity metrics

```python
Tasks → Count completed
Content → Count published
Contacts → Count new
Meetings → Count attended
        ↓
    Metrics JSON
```

#### 2. content_ideas.py
**Input**: Bookmarks + Published content
**Output**: Content suggestions
**Purpose**: Generate writing ideas

```python
Bookmarks → Extract tags
         → Find trending topics
         → Identify gaps
         → Suggest ideas
```

#### 3. stale_contacts.py
**Input**: Contacts + Interactions
**Output**: Reconnection list
**Purpose**: Relationship maintenance

```python
Contacts → Calculate days since last contact
        → Prioritize by relationship type
        → Generate outreach list
```

#### 4. idea_to_draft.py
**Input**: Idea ID
**Output**: Markdown draft
**Purpose**: Kickstart writing

```python
Idea → Find related bookmarks
    → Generate structure
    → Create draft file
    → Update idea status
```

---

## AI Integration

### Claude Code Skill Architecture

```
User Request
     ↓
Claude Code
     ↓
Load Identity Module (Voice-First)
     ↓
Parse Intent
     ↓
┌────────────────────────────────┐
│  Operation Router              │
├────────────────────────────────┤
│ • add-idea → content module    │
│ • add-bookmark → knowledge     │
│ • add-contact → network        │
│ • add-task → operations        │
│ • weekly-review → run script   │
└────────────────────────────────┘
     ↓
Execute Operation
     ↓
Update JSONL/YAML/MD files
     ↓
Provide Feedback
```

### Progressive Context Loading

**Principle**: Only load what's needed

**Example - Content Task**:
```xml
<on-content-task>
  <load>identity/voice/style.md</load>
  <load>content/ideas/ideas.jsonl</load>
  <load>knowledge/bookmarks/bookmarks.jsonl</load>
  <reason>Need voice + ideas + research</reason>
</on-content-task>
```

**Example - Network Task**:
```xml
<on-network-task>
  <load>network/contacts/contacts.jsonl</load>
  <load>network/relationships/interactions.jsonl</load>
  <reason>Need contact database + history</reason>
</on-network-task>
```

---

## Design Patterns

### 1. Separation of Concerns

Each module is independent:
- Can be used alone
- Can be removed without breaking others
- Has its own README

### 2. Progressive Disclosure

Load data incrementally:
- Don't load all modules at once
- Load based on current task
- Keeps context clean

### 3. Voice-First

Identity always loaded:
- Ensures brand consistency
- Guides AI responses
- Maintains personal style

### 4. Tag-Based Discovery

Consistent tagging enables:
- Cross-module queries
- Related content discovery
- Trend analysis

### 5. Time-Based Organization

Chronological data structure:
- Easy to review by period
- Supports analytics
- Natural for humans

---

## Extension Points

### Adding Custom Modules

```bash
mkdir -p custom-module/data
echo "# Custom Module" > custom-module/README.md
```

Update `.claude/skills/digital-brain/instructions.xml`:
```xml
<module name="custom">
  <path>custom-module/</path>
  <purpose>Your custom purpose</purpose>
</module>
```

### Adding Custom Scripts

```python
#!/usr/bin/env python3
"""
Custom analysis script
"""
import json
from pathlib import Path

def load_jsonl(filepath):
    # Standard loader
    records = []
    with open(filepath, 'r') as f:
        for line in f:
            if line.strip():
                records.append(json.loads(line))
    return records

def custom_analysis():
    # Your logic here
    data = load_jsonl('path/to/data.jsonl')
    # Analyze and output
    pass

if __name__ == '__main__':
    custom_analysis()
```

### Extending Data Schemas

JSONL is flexible - just add fields:

```jsonl
// Original
{"id": "task-001", "title": "Task"}

// Extended
{"id": "task-002", "title": "Task", "estimate_hours": 2, "category": "dev"}
```

---

## Performance Considerations

### File Sizes

**Small files** (< 1MB):
- Read entire file
- Process in memory
- Fast operations

**Large files** (> 1MB):
- Stream processing
- Use `head_limit` in queries
- Consider archiving old entries

### Backup Strategy

**Daily**:
```bash
git add -A
git commit -m "Daily brain backup"
git push
```

**Weekly**:
```bash
tar -czf brain-backup-$(date +%Y%m%d).tar.gz \
  identity/ content/ knowledge/ network/ operations/
```

---

## Security & Privacy

### Sensitive Data

**DO NOT commit**:
- Passwords or API keys
- Private personal information
- Confidential work details

**Use .gitignore**:
```
# Sensitive files
identity/private/
network/contacts/private.jsonl
*.secret.md
```

### Data Ownership

- All data is local files
- No external services required
- You own everything
- Easy to backup and migrate

---

## Future Enhancements

### Potential Additions

1. **Timeline View**: Chronological visualization
2. **Graph Database**: Relationship mapping
3. **Search Engine**: Full-text search across modules
4. **Mobile App**: Mobile data capture
5. **Sync Service**: Multi-device synchronization
6. **Analytics Dashboard**: Visual metrics
7. **AI Chat Interface**: Conversational data entry
8. **Calendar Integration**: Meeting auto-import
9. **Browser Extension**: One-click bookmarking
10. **API Server**: Programmatic access

### Community Extensions

Share your scripts and modules:
- Custom automation scripts
- Domain-specific modules
- Integration connectors
- Visualization tools

---

## Philosophy

> "Your brain is for having ideas, not holding them."
> — David Allen, Getting Things Done

**Digital Brain achieves this by**:
1. **Capture everything** → Append-only logs
2. **Organize automatically** → Tag-based system
3. **Synthesize with AI** → Claude Code integration
4. **Act on insights** → Automation scripts
5. **Maintain continuity** → Never lose data

---

**Built on**: File systems, not databases
**Powered by**: AI assistance, not manual labor
**Focused on**: Your productivity, not productivity theater
