# Claude Code Configuration

## Language
- User communicates in Chinese, respond in Chinese when appropriate

## Permissions
- Allow all file read/write/edit operations within this project
- When the user provides a web URL or需要将网页内容转成 Markdown，统一使用 Chrome MCP（navigate_page + take_snapshot），不使用 WebFetch 或 agent-browser

## Conventions
- 流程图只保存 Mermaid 源代码（.mmd 文件），不保存生成的图片

## Multi-Component Design

当一个软件任务需要组合多个组件（库、框架、服务、工具）协作完成时，在确定方案前必须先完成以下梳理：

1. **设计协作方式**：明确各组件之间的配合模式（数据流向、调用关系、职责边界）
2. **反推组件要求**：从协作方式推导出对每个组件的具体要求（需要提供什么 API/能力/数据格式）
3. **验证可行性**：检查每个组件是否能满足这些要求（查文档、读源码、确认版本支持）
4. **识别缺口**：如有组件无法满足要求，明确指出缺口并提出替代方案（换组件 or 调整协作方式）

先把这个分析呈现给用户，确认后再执行。

## Environment & Dependencies

项目的所有依赖通过 `bash setup.sh` 一键安装，新机器从零开始只需 `git clone && bash setup.sh`。

**设计原则**：
- 项目可在任意新机器上零配置复现，`setup.sh` 是唯一入口
- 每类依赖有明确的管理工具，lockfile 保证跨机器一致性
- 已安装的依赖自动跳过，脚本幂等安全

**依赖分层**：

| 层级 | 管理方式 | 配置文件 |
|------|---------|---------|
| Python 包 | uv | `pyproject.toml` + `uv.lock` |
| Node.js 包 | npm | `package.json` |
| 系统工具 | brew / apt | `setup.sh` 中声明 |
| 模型文件 | curl 下载 | `setup.sh` 中声明 |

**日常操作**：
- 执行 Python 脚本：`uv run <script.py>`（不使用系统 `python3`）
- 新增 Python 依赖：`uv add <package>`
- 新增系统工具依赖：在 `setup.sh` 的"系统工具"段落添加检测+安装逻辑

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
