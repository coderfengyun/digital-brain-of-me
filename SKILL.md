---
name: digital-brain
description: This skill should be used when the user asks to "write a post", "check my voice", "look up contact", "prepare for meeting", "weekly review", "track goals", "add paper", "read paper", "create module", "add module", or mentions personal brand, content creation, network management, academic paper reading, system extension, or voice consistency.
version: 1.0.0
---

# Digital Brain

A structured personal operating system for managing digital presence, knowledge, relationships, and goals with AI assistance. Designed for founders building in public, content creators growing their audience, and tech-savvy professionals seeking AI-assisted personal management.

**Important**: This skill uses progressive disclosure. Module-specific instructions are in each subdirectory's `.md` file. Only load what's needed for the current task.

## When to Activate

Activate this skill when the user:

- Requests content creation (posts, threads, newsletters) - load identity/voice.md first
- Asks for help with personal brand or positioning
- Needs to look up or manage contacts/relationships
- Wants to capture or develop content ideas
- Requests meeting preparation or follow-up
- Asks for weekly reviews or goal tracking
- Needs to save or retrieve bookmarked resources
- Wants to organize research or learning materials
- Needs to add, read, or manage academic papers
- Wants to extend the system or create new modules

**Trigger phrases**: "write a post", "my voice", "content ideas", "who is [name]", "prepare for meeting", "weekly review", "save this", "my goals", "add paper", "read paper", "paper reading", "create module", "add module", "extend system"

## Core Concepts

### Progressive Disclosure Architecture

The Digital Brain follows a three-level loading pattern:

| Level | When Loaded | Content |
|-------|-------------|---------|
| **L1: Metadata** | Always | This SKILL.md overview |
| **L2: Module Instructions** | On-demand | `[module]/README.md` files |
| **L3: Data Files** | As-needed | `.jsonl`, `.yaml`, `.md` data |

### File Format Strategy

Formats chosen for optimal agent parsing:

- **JSONL** (`.jsonl`): Append-only logs - ideas, posts, contacts, interactions
- **YAML** (`.yaml`): Structured configs - goals, values, circles
- **Markdown** (`.md`): Narrative content - voice, brand, calendar, todos
- **XML** (`.xml`): Complex prompts - content generation templates

### Append-Only Data Integrity

JSONL files are **append-only**. Never delete entries:
- Mark as `"status": "archived"` instead of deleting
- Preserves history for pattern analysis
- Enables "what worked" retrospectives

## Detailed Topics

### Module Overview

```
digital-brain-of-me/
├── identity/     → Voice, brand, values (READ FIRST for content)
├── content/      → Ideas, drafts, posts, calendar
├── knowledge/    → Bookmarks, research, learning, papers
├── network/      → Contacts, interactions, intros
├── operations/   → Todos, goals, meetings, metrics
└── scripts/      → Automation scripts
```

### Identity Module (Critical for Content)

**Always read `identity/voice/style.md` before generating any content.**

Contains:
- `voice/style.md` - Tone, style, vocabulary, patterns
- `voice/principles.md` - Core beliefs and principles
- `brand/profile.yaml` - Positioning, audience, content pillars

### Content Module

Pipeline: `ideas.jsonl` → `drafts/` → `published.jsonl`

- Capture ideas immediately to `ideas/ideas.jsonl`
- Develop in `drafts/` using templates
- Log published content to `published/published.jsonl` with metrics

### Network Module

Personal CRM with relationship tiers:
- `colleague` - Professional connections
- `mentor` - Guidance and advice
- `client` - Business relationships
- `friend` - Personal relationships
- `acquaintance` - Casual connections

### Operations Module

Productivity system with priority levels:
- **high**: Do today, blocking
- **medium**: This week, important
- **low**: This month, valuable

## Practical Guidance

### Content Creation Workflow

```
1. Read identity/voice/style.md (REQUIRED)
2. Check identity/brand/profile.yaml for topic alignment
3. Reference content/published/published.jsonl for successful patterns
4. Draft matching voice attributes
5. Log to published.jsonl after publishing
```

### Pre-Meeting Preparation

```
1. Look up contact: network/contacts/contacts.jsonl
2. Get history: network/relationships/interactions.jsonl
3. Check pending: operations/tasks/tasks.jsonl
4. Generate brief with context
```

### Weekly Review Process

```
1. Run: python scripts/weekly_review.py
2. Review metrics in operations/metrics/weekly.jsonl
3. Check stale contacts: scripts/stale_contacts.py
4. Update goals progress in operations/goals/goals.yaml
```

## Examples

### Example: Writing a Blog Post

**Input**: "Help me write a post about AI agents"

**Process**:
1. Read `identity/voice/style.md` → Extract voice attributes
2. Check `identity/brand/profile.yaml` → Confirm topic alignment
3. Reference `content/published/published.jsonl` → Find similar successful posts
4. Draft post matching voice patterns
5. Suggest adding to `content/ideas/ideas.jsonl` if not publishing immediately

**Output**: Post draft in user's authentic voice with platform-appropriate format.

### Example: Contact Lookup

**Input**: "Prepare me for my call with Sarah Chen"

**Process**:
1. Search `network/contacts/contacts.jsonl` for "Sarah Chen"
2. Get recent entries from `network/relationships/interactions.jsonl`
3. Check `operations/tasks/tasks.jsonl` for pending items with Sarah
4. Compile brief: role, context, last discussed, follow-ups

**Output**: Pre-meeting brief with relationship context.

### Example: Academic Paper Reading

**Input**: "I want to read the Attention Is All You Need paper"

**Process**:
1. Run `scripts/add_paper.py` to add paper to reading list
2. Open generated `paper-YYYYMMDD-XXX.md` note file
3. Guide user through Phase 1: Extract narrative (15-30 min)
   - Read abstract, intro, conclusion
   - Fill in core narrative section
   - Draw Mermaid structure diagram
4. Update status to "reading" with main claim
5. Later guide through Phase 2: Verify data (1-2 hours)
   - Find supporting evidence for each claim
   - Fill data evidence table
   - Complete critical thinking section
6. Update status to "completed"

**Output**: Structured paper notes with narrative, evidence, and critical analysis.

### Example: Creating a New Module

**Input**: "I want to create a contacts module to track my professional network"

**Process**:
1. Open `module_operation/MODULE_CREATION_GUIDE.md` for complete checklist
2. Guide user through 6-phase creation process:
   - Phase 1: Requirements analysis (30 min)
   - Phase 2: Core files creation (2-3 hours)
   - Phase 3: Documentation (2-3 hours)
   - Phase 4: System integration (1-2 hours) - update 8 files
   - Phase 5: Cross-module integration (1-2 hours)
   - Phase 6: Quality assurance (1 hour)
3. Create necessary files:
   - `knowledge/contacts/README.md`
   - `knowledge/contacts/contacts.jsonl`
   - `scripts/add_contact.py`, `scripts/search_contacts.py`
4. Update system integration files:
   - SKILL.md, AGENT.md, ARCHITECTURE.md, EXAMPLES.md
   - README.md, knowledge/KNOWLEDGE.md
   - `.claude/skills/digital-brain/skill.md`
   - `.claude/skills/digital-brain/instructions.xml`
5. Run verification: `python module_operation/check_module_integration.py contacts contact`
6. Create COMPLETION_REPORT.md documenting the module

**Output**: Fully integrated new module ready for production use.

## Guidelines

1. **Voice First**: Always read `identity/voice/style.md` before any content generation
2. **Append Only**: Never delete from JSONL files - archive instead
3. **Update Timestamps**: Set `updated_at` field when modifying tracked data
4. **Cross-Reference**: Knowledge informs content, network informs operations, papers inspire ideas
5. **Log Interactions**: Always log meetings/calls to `interactions.jsonl`
6. **Preserve History**: Past content in `published.jsonl` informs future performance
7. **Narrative First**: For papers, extract narrative structure before diving into data details
8. **Complete Integration**: New modules require updating 8 system files - use module_operation/MODULE_CREATION_GUIDE.md and check_module_integration.py

## Integration

This skill integrates context engineering principles:

- **context-fundamentals** - Progressive disclosure, attention budget management
- **memory-systems** - JSONL for persistent memory, structured recall
- **tool-design** - Scripts in `scripts/` follow tool design principles
- **context-optimization** - Module separation prevents context bloat

## References

Internal references:
- [Identity Module](./identity/voice/principles.md) - Voice and brand details
- [Content Module](./content/CONTENT.md) - Content pipeline docs
- [Knowledge Module](./knowledge/KNOWLEDGE.md) - Learning and research
- [Papers Module](./papers/PAPERS.md) - Academic paper reading
- [Network Module](./network/NETWORK.md) - CRM documentation
- [Operations Module](./operations/OPERATIONS.md) - Productivity system
- [Module Creation Guide](./module_operation/MODULE_CREATION_GUIDE.md) - How to extend the system

External resources:
- [Agent Skills for Context Engineering](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering)
- [Original Digital Brain Skill](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering/tree/main/examples/digital-brain-skill)

---

## Skill Metadata

**Created**: 2026-02-26
**Based On**: [Digital Brain Skill by Murat Can Koylan](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering/tree/main/examples/digital-brain-skill)
**Version**: 1.0.0
