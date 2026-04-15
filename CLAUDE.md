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

> **本文件定位**：开发/扩展 digital-brain 系统时的约定——文件格式、数据 schema、模块创建流程、设计原则。使用 digital-brain 的操作手册（路由表、加载策略、脚本列表）见 `.claude/skills/digital-brain/skill.md`。

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

### Sources (papers, podcasts)

External inputs that go through a processing pipeline live in `sources/sources.jsonl`. All types share the same schema — source (input) → processing → output (.md).

```json
{
  "id": "paper-YYYYMMDD-XXX | pod-YYYYMMDD-XXX",
  "type": "paper | podcast",
  "source": "https://... | sources/paper-XXX.pdf",
  "title": "Title",
  "tags": [],
  "added_at": "YYYY-MM-DD",
  "output": "knowledge/papers/paper-XXX/notes.md"
}
```

- `source` — URL or local file path in `sources/` directory (file inputs use `sources/{id}.ext`)
- `output` empty = 待处理, filled = 已完成
- Processing artifacts (downloaded HTML, audio files) live in conventional locations but are NOT tracked in sources.jsonl

Note: Podcast transcription is handled by the standalone `podcast-transcribe` skill, which writes to sources.jsonl for tracking.

### Bookmarks

Bookmarks don't have a processing pipeline, so they live separately in `knowledge/bookmarks/bookmarks.jsonl`.

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
   - `.claude/skills/digital-brain/skill.md`, CLAUDE.md, README.md
   - knowledge/KNOWLEDGE.md
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

1. **Progressive Disclosure**: Skill description（触发匹配）→ skill.md（操作指令）→ 数据文件。简单模块（content, knowledge, operations）由 `digital-brain` skill 路由；复杂工作流（paper-reading, investment, podcast-transcribe）各自独立 skill
2. **Data/Skill Separation**: 数据目录（`knowledge/papers/`, `investment/`, `sources/`）只存数据 + schema 文档；工作流指令和脚本在 `.claude/skills/` 下对应目录
3. **Append-Only**: Never delete, always add (mark as archived if needed)
4. **Cross-Reference**: Link related data across modules（flat-file relational model）
5. **Voice-First**: Identity always loaded before content generation
6. **Module Separation**: 每个模块独立管理自己的操作细节，上层只做路由
7. **Flat Routing**: skill.md 路由表的 Action 列只写 `Read <模块入口文件>`，不展开处理步骤；每个请求直接指向最终处理它的模块，避免中间跳转
8. **Complete Integration**: New modules require updating all system files (use guide and checker)

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
- **When a digital-brain operation fails or produces unexpected results**，优先修复相关模块的设计/指令；仅当问题跨模块且暂时无法通过设计消除时，临时记到 `.claude/skills/digital-brain/gotchas.md`，修复后删除
