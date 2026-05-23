# Claude Code Configuration

## Language
- User communicates in Chinese, respond in Chinese when appropriate

## Permissions
- Allow all file read/write/edit operations within this project
- When the user provides a web URL or需要将网页内容转成 Markdown，统一使用 Chrome MCP（navigate_page + take_snapshot），不使用 WebFetch 或 agent-browser

## Conventions
- 流程图只保存 Mermaid 源代码（.mmd 文件），不保存生成的图片

## Python Environment
- 包管理使用 **uv**（`pyproject.toml` + `uv.lock`）
- 执行 Python 脚本统一用 `uv run <script.py>`，**不使用系统 `python3`**
- 首次 clone 或新机器：`bash setup.sh`（自动安装 uv → 下载 Python 3.13 → 创建 .venv → 安装依赖）
- 新增依赖：`uv add <package>`（自动更新 pyproject.toml + uv.lock）

---

# Digital Brain - Development Guide

> **本文件定位**：digital-brain 系统的操作指南和开发约定——模块导航、文件格式、数据 schema、模块创建流程、设计原则。

## Module Navigation

用户请求涉及数据操作时，直接读取对应模块入口文件了解格式和操作方式：

| 请求类型 | 入口文件 |
|---------|---------|
| 内容创作（写文章、post） | 先读 `identity/voice/style.md`，再看 `content/CONTENT.md` |
| 内容创意 | 运行 `scripts/content_ideas.py` 或读 `content/ideas/ideas.jsonl` |
| 书签/链接保存 | `knowledge/KNOWLEDGE.md` |
| 任务管理 | `operations/OPERATIONS.md` |
| 目标跟踪 | `operations/goals/goals.yaml` |
| 周记/周报 | `weekly-review/WEEKLY-REVIEW.md` |
| 添加外部来源（论文/文章/研报/播客） | `sources/SOURCES.md`（注册后路由到对应 skill，输出到领域目录） |

**关键规则**：内容创作类任务必须先读 `identity/voice/style.md` 再动笔。

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
  "output": "investment/作者/文章主题/notes.md | knowledge/ai/文章主题/notes.md"
}
```

- `source` — URL or local file path in `sources/` directory (file inputs use `sources/{id}.ext`)
- `output` empty = 待处理, filled = 已完成
- `type` 是处理类型，不是内容归属；`paper` 输出到未来最可能被调用的领域目录
- Processing artifacts (downloaded HTML, audio files) live in conventional locations but are NOT tracked in sources.jsonl

Note: Audio/video transcription is handled by the standalone `transcribe` skill, which writes to sources.jsonl for tracking.

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

### Weekly Review

周记为自由格式 Markdown 文件，存放在 `weekly-review/` 目录下。

- 文件命名：`YYYY-MM-DD~MM-DD.md`
- 内容结构：投资、修行&内观、学习、接下来的调整
- 详见 `weekly-review/WEEKLY-REVIEW.md`

### Investment Trades

See `investment/投资日志整理/交易日志汇总表.schema.json` for CSV schema.

## Module Creation

When creating new modules, follow `.claude/skills/module-toolkit/references/MODULE_CREATION_GUIDE.md`:

1. **Requirements Analysis** - Define data model, workflow, and tag system
2. **Core Files Creation** - README, data.jsonl, scripts
3. **Documentation** - Templates, examples, quick start
4. **System Integration** - Update system files:
   - CLAUDE.md (Module Navigation 表 + Data Entry Schemas), README.md
   - knowledge/KNOWLEDGE.md
5. **Cross-Module Integration** - Define data flows and relationships
6. **Quality Assurance** - Test and verify with check script

After creating a module, ALWAYS run:
```bash
python .claude/skills/module-toolkit/scripts/check_module_integration.py <module_name> <keyword>
```

## Context Engineering Principles

本系统的设计理念源自 [The File System Is the New Database](the-file-system-is-the-new-database.md)——核心思想是 context engineering 而非 prompt engineering：不是优化单次提问，而是设计信息架构让 AI 每次都能做出正确决策。

1. **Progressive Disclosure**: CLAUDE.md（路由 + 约定）→ 模块入口 README → 数据文件。简单模块（content, knowledge, operations, weekly-review）由 CLAUDE.md Module Navigation 路由；复杂工作流（paper-reading, investment, transcribe）各自独立 skill
2. **Data/Skill Separation**: 数据目录（`knowledge/ai/`, `knowledge/organizations/`, `investment/`, `sources/`）只存数据 + schema 文档；复杂工作流的指令和脚本在 `.claude/skills/` 下对应目录。`paper-reading` 是处理流程，不是内容归属目录
3. **Append-Only**: Never delete, always add (mark as archived if needed)
4. **Cross-Reference**: Link related data across modules（flat-file relational model）
5. **Voice-First**: Identity always loaded before content generation
6. **Module Separation**: 每个模块独立管理自己的操作细节，CLAUDE.md 只做路由索引
7. **Flat Routing**: 路由表的 Action 列只指向模块入口文件，不展开处理步骤；每个请求直接指向最终处理它的模块，避免中间跳转
8. **Complete Integration**: New modules require updating CLAUDE.md and relevant system files (use guide and checker)

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
- Generate unique IDs for new entries (format: `type-XXX`, e.g., `idea-001`, `paper-YYYYMMDD-XXX`); weekly-review 文件用 `YYYY-MM-DD~MM-DD.md` 命名
- Maintain consistent tagging across modules for better discovery
- **When a digital-brain operation fails or produces unexpected results**，优先修复相关模块的设计/指令
