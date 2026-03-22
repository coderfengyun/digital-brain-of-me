# Claude Code Configuration

## Language
- User communicates in Chinese, respond in Chinese when appropriate

## Permissions
- Allow all file read/write/edit operations within this project
- When the user provides a web URL or需要将网页内容转成 Markdown，统一使用 Chrome MCP（navigate_page + take_snapshot），不使用 WebFetch 或 agent-browser

## Conventions
- 流程图只保存 Mermaid 源代码（.mmd 文件），不保存生成的图片

---

# Digital Brain - Claude Instructions

This is a Digital Brain personal operating system. When working in this project:

## Core Rules

1. **Always read identity/voice/style.md before writing any content** - Match the user's authentic voice
2. **Append to JSONL files, never overwrite** - Preserve history
3. **Update timestamps** when modifying tracked data
4. **Cross-reference modules** - Knowledge informs content, network informs operations
5. **Update all references when moving/renaming files** - Search entire repo for references to the old path and update them

## Quick Reference

- **Writing content**: Read `identity/voice/style.md` first, then create drafts in `content/drafts/`
- **Looking up contacts**: Search `network/contacts/contacts.jsonl`, check `network/relationships/interactions.jsonl` for history
- **Content ideas**: Check `content/ideas/ideas.jsonl`, run `scripts/content_ideas.py`
- **Task management**: Use `operations/tasks/tasks.jsonl`, align with `operations/goals/goals.yaml`
- **Weekly review**: Run `scripts/weekly_review.py`
- **Investment trades**: Use `investment/投资日志整理/scripts/` for trade journal management and P&L calculation

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
| "Add paper to read" | Run `add_paper.py "URL"` → Create paper folder |
| "Read this paper" | Guide through 2-phase reading → Update status |
| "Show unread papers" | Read `papers/papers.jsonl`, filter entries where `notes` is empty |
| "Transcribe this podcast" | Run `transcribe_podcast.py` with RSS or audio file |
| "Add trade" / "交易记录" | Use `investment/投资日志整理/scripts/write_trade_journal.py add` |
| "Import trades from Binance" | Run `fetch_binance_trades.py` → `write_trade_journal.py import-binance` |
| "Calculate P&L" / "盈亏" | Run `investment/投资日志整理/scripts/calc_pnl.py` |
| "Create new module" | Open `module-toolkit/MODULE_CREATION_GUIDE.md` → Guide through 6 phases |
| "Extend the system" | Follow module creation process → Update system files |
| "Check module integration" | Run `check_module_integration.py <module> <keyword>` |

## Module Loading Strategy

Use **progressive disclosure**:

1. **Always Load** (L1):
   - `identity/brand/profile.yaml`
   - `identity/voice/style.md`

2. **Load on Content Tasks** (L2):
   - `content/ideas/ideas.jsonl`
   - `content/published/published.jsonl`
   - `knowledge/bookmarks/bookmarks.jsonl`
   - `papers/papers.jsonl` (if paper-related)
   - `podcasts/podcasts.jsonl` (if podcast-related)

3. **Load on Network Tasks** (L2):
   - `network/contacts/contacts.jsonl`
   - `network/relationships/interactions.jsonl`

4. **Load on Operations Tasks** (L2):
   - `operations/tasks/tasks.jsonl`
   - `operations/goals/goals.yaml`
   - `operations/metrics/weekly.jsonl`

5. **Load on Investment Tasks** (L2):
   - `investment/INVESTMENT.md`
   - `investment/投资日志整理/交易日志汇总表.csv`
   - `investment/投资日志整理/交易日志汇总表.schema.json`

6. **Load on Demand** (L3):
   - Individual draft files
   - Research notes
   - Paper notes (`paper-YYYYMMDD-XXX.md`)
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

### Adding Papers

```json
{
  "id": "paper-YYYYMMDD-XXX",
  "url": "https://arxiv.org/...",
  "source": "",
  "notes": ""
}
```

- `url` - Original URL or local filename
- `source` - Local source document path (e.g., `paper-YYYYMMDD-XXX/paper.html`)
- `notes` - Reading notes path (e.g., `paper-YYYYMMDD-XXX/notes.md`)
- Reading status: `notes` empty = unread, `notes` filled = completed

Or use the script:
```bash
python scripts/add_paper.py "URL"
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
- `python scripts/add_paper.py "URL"` - Add paper to reading list
- `python scripts/transcribe_podcast.py --rss "URL" --count 1` - Transcribe podcast from RSS feed
- `python scripts/transcribe_podcast.py --audio file.mp3 --title "Title" --show "Show"` - Transcribe local audio
- `python investment/投资日志整理/scripts/write_trade_journal.py add --品种 BTC --操作 买入 --价格 76653 --数量 0.00391 --金额 299.71 --币种 USD --日期 2025-04-07` - Add trade record
- `python investment/投资日志整理/scripts/write_trade_journal.py import-binance /tmp/binance.csv` - Import Binance trades
- `python investment/投资日志整理/scripts/calc_pnl.py` - Calculate investment P&L
- `python module-toolkit/check_module_integration.py <module> <keyword>` - Verify module integration completeness

## Voice Consistency Checklist

Before generating any content, verify:

1. Read `identity/voice/style.md`
2. Checked `identity/brand/profile.yaml` for topic alignment
3. Reviewed similar content in `content/published/published.jsonl`
4. Applied voice patterns (tone, vocabulary, structure)
5. Maintained authenticity and brand positioning

## Module Creation

When creating new modules, follow the complete guide in `module-toolkit/MODULE_CREATION_GUIDE.md`:

### 6-Phase Process

1. **Requirements Analysis** (30 min) - Define data model, workflow, and tag system
2. **Core Files Creation** (2-3 hours) - README, data.jsonl, scripts
3. **Documentation** (2-3 hours) - Templates, examples, quick start
4. **System Integration** (1-2 hours) - Update system files:
   - SKILL.md, CLAUDE.md, README.md
   - knowledge/KNOWLEDGE.md
   - `.claude/skills/digital-brain/skill.md`
   - `.claude/skills/digital-brain/instructions.xml`
5. **Cross-Module Integration** (1-2 hours) - Define data flows and relationships
6. **Quality Assurance** (1 hour) - Test and verify with check script

### Integration Verification

After creating a module, ALWAYS run:
```bash
python module-toolkit/check_module_integration.py <module_name> <keyword>
```

This checks that all system files have been properly updated with sufficient references.

### Common Pitfalls

Most commonly missed files:
1. `.claude/skills/digital-brain/skill.md`
2. `.claude/skills/digital-brain/instructions.xml`
3. Multiple sections in CLAUDE.md

## Context Engineering Principles

本系统的设计理念源自 [The File System Is the New Database](the-file-system-is-the-new-database.md)——核心思想是 context engineering 而非 prompt engineering：不是优化单次提问，而是设计信息架构让 AI 每次都能做出正确决策。

1. **Progressive Disclosure**: Load only what's needed for current task（三级加载：L1 路由 → L2 模块指令 → L3 数据文件）
2. **Append-Only**: Never delete, always add (mark as archived if needed)
3. **Cross-Reference**: Link related data across modules（flat-file relational model）
4. **Voice-First**: Identity always loaded before content generation
5. **Historical Analysis**: Past data informs future decisions
6. **Complete Integration**: New modules require updating all system files (use guide and checker)

## Error Prevention

**DON'T**:
- Delete entries from JSONL files
- Overwrite existing data without reading first
- Generate content without reading voice.md
- Modify template entries
- Break JSONL format (one object per line)
- Move/rename files without searching for and updating all references

**DO**:
- Append new entries to JSONL files
- Update timestamps when modifying
- Read identity files before content creation
- Cross-reference related data
- Preserve complete history
- Search repo with `grep -r "filename"` before moving/renaming files, then update all references

---

**Remember**: This is a personal operating system. Maintain the user's authentic voice, preserve their data history, and help them build intentional systems for content, relationships, and productivity.
