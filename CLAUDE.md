# Claude Code Configuration

## Language
- User communicates in Chinese, respond in Chinese when appropriate

## Permissions
- Allow all file read/write/edit operations within this project
- When the user provides a web URL or需要将网页内容转成 Markdown，统一使用 Chrome MCP（navigate_page + take_snapshot），不使用 WebFetch 或 agent-browser

## Conventions
- 流程图只保存 Mermaid 源代码（.mmd 文件），不保存生成的图片

---

# Digital Brain - Development Guide

> **本文件定位**：开发/扩展 digital-brain 系统时的约定——文件格式、数据 schema、模块创建流程、设计原则。使用 digital-brain 的操作手册（路由表、加载策略、脚本列表）见 `SKILL.md`。

## File Conventions

- `.jsonl` files: One JSON object per line, append-only
- `.md` files: Human-readable, freely editable
- `.yaml` files: Configuration and structured data
- `.csv` files: Tabular data with schema validation (see `.schema.json`)
- Template entries in README files: Reference formats, don't modify

## Data Entry Schemas

各模块数据条目的标准格式。添加新条目时遵循对应 schema。

### Content Ideas

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

### Bookmarks

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

### Papers

```json
{
  "id": "paper-YYYYMMDD-XXX",
  "url": "https://arxiv.org/...",
  "source": "",
  "notes": ""
}
```

- `source` - Local source document path (e.g., `paper-YYYYMMDD-XXX/paper.html`)
- `notes` - Reading notes path (e.g., `paper-YYYYMMDD-XXX/notes.md`)
- Reading status: `notes` empty = unread, `notes` filled = completed

### Contacts

```json
{
  "id": "contact-XXX",
  "name": "Full Name",
  "relationship": "colleague|mentor|client|friend|acquaintance",
  "tags": ["tag1", "tag2"],
  "met_at": "YYYY-MM-DD",
  "last_contact": "YYYY-MM-DD",
  "notes": "Context about this person",
  "links": { "twitter": "", "linkedin": "", "email": "", "website": "" }
}
```

### Interactions

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

### Tasks

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

### Investment Trades

See `investment/投资日志整理/交易日志汇总表.schema.json` for CSV schema.

## Module Creation

When creating new modules, follow `module-toolkit/MODULE_CREATION_GUIDE.md`:

1. **Requirements Analysis** - Define data model, workflow, and tag system
2. **Core Files Creation** - README, data.jsonl, scripts
3. **Documentation** - Templates, examples, quick start
4. **System Integration** - Update system files:
   - SKILL.md, CLAUDE.md, README.md
   - knowledge/KNOWLEDGE.md
   - `.claude/skills/digital-brain/skill.md`
5. **Cross-Module Integration** - Define data flows and relationships
6. **Quality Assurance** - Test and verify with check script

After creating a module, ALWAYS run:
```bash
python module-toolkit/check_module_integration.py <module_name> <keyword>
```

Most commonly missed integration files:
1. `.claude/skills/digital-brain/skill.md`
2. Multiple sections in CLAUDE.md

## Context Engineering Principles

本系统的设计理念源自 [The File System Is the New Database](the-file-system-is-the-new-database.md)——核心思想是 context engineering 而非 prompt engineering：不是优化单次提问，而是设计信息架构让 AI 每次都能做出正确决策。

1. **Progressive Disclosure**: L1 路由（SKILL.md）→ L2 模块指令（各模块 README.md）→ L3 数据文件
2. **Append-Only**: Never delete, always add (mark as archived if needed)
3. **Cross-Reference**: Link related data across modules（flat-file relational model）
4. **Voice-First**: Identity always loaded before content generation
5. **Module Separation**: 每个模块独立管理自己的操作细节，上层只做路由
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
- Generate unique IDs for new entries (format: `type-XXX`, e.g., `idea-001`, `paper-YYYYMMDD-XXX`)
- Maintain consistent tagging across modules for better discovery
- **When a digital-brain operation fails or produces unexpected results**, append the lesson to `.claude/skills/digital-brain/gotchas.md`
