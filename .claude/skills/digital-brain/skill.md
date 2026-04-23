---
name: digital-brain
description: "Personal knowledge management system. Use when: user asks about bookmarks, tasks, goals, content ideas, weekly review, or any personal knowledge management task. Also trigger on Chinese phrases like 书签, 任务, 目标, 内容创意, 周报, 写一篇文章, 保存这个链接, 我的目标. Handles: content creation (with voice/identity), bookmarks, task tracking, goal management, weekly reviews, and source registration/routing. Note: paper reading, investment operations, podcast transcription, and module creation are handled by their own dedicated skills."
---

# Digital Brain

个人数字操作系统：管理数字身份、知识、目标。

> **本文件定位**：使用 digital-brain 时的操作手册——路由、加载策略、脚本列表、使用规则。修改/扩展系统本身的开发约定见 `CLAUDE.md`。

## When to Activate

Activate this skill when the user:

- Requests content creation (posts, threads, newsletters) - load `identity/voice/style.md` first
- Asks for help with personal brand or positioning
- Wants to capture or develop content ideas
- Asks for weekly reviews or goal tracking
- Needs to save or retrieve bookmarked resources
- Wants to organize research or learning materials
- Wants to add a new external source (routes to appropriate skill)
**Trigger phrases**: "write a post", "my voice", "content ideas", "weekly review", "save this", "my goals", "add source"

**Not handled here** (dedicated skills):
- Paper reading → `paper-reading` skill
- Investment operations → `investment` skill
- Podcast transcription → `podcast-transcribe` skill
- Module creation / system extension → `module-toolkit` skill

## Module Overview

```
digital-brain-of-me/
├── sources/      → 外部输入注册表
├── identity/     → Voice, brand, values (READ FIRST for content)
├── content/      → Ideas, drafts, posts, calendar
├── knowledge/    → Bookmarks, research, learning, web-clippings
│   └── papers/   → Paper reading notes (data only)
├── operations/   → Todos, goals, meetings, metrics
├── investment/   → Trade journal + research (data only)
└── scripts/      → Automation scripts
```

## Request Routing

| Request | Action |
|---------|--------|
| "Write a post about X" | Read `identity/voice/style.md` |
| "What should I create?" | Run `scripts/content_ideas.py` |
| "Weekly review" | Run `scripts/weekly_review.py` → Present insights |
| "Save this bookmark" | Append to `knowledge/bookmarks/bookmarks.jsonl` |
| "Add a task" | Append to `operations/tasks/tasks.jsonl` with priority |
| "Track a goal" | Update `operations/goals/goals.yaml` with progress |
| "Add source" / URL / 文件 | Read `sources/SOURCES.md`（判断类型后路由到对应 skill） |
| "Create new module" | → `module-toolkit` skill |
| "Check module integration" | → `module-toolkit` skill |

## Module Loading Strategy

Use **progressive disclosure**:

1. **Load on Content Creation Tasks** (L2):
   - `identity/brand/profile.yaml`
   - `identity/voice/style.md`
   - `content/ideas/ideas.jsonl`
   - `content/published/published.jsonl`
   - `knowledge/bookmarks/bookmarks.jsonl`

2. **Load on Source Registration** (L2):
   - `sources/SOURCES.md`（统一入口：注册、类型判断、路由到对应 skill）

3. **Load on Operations Tasks** (L2):
   - `operations/tasks/tasks.jsonl`
   - `operations/goals/goals.yaml`
   - `operations/metrics/weekly.jsonl`

4. **Load on Demand** (L3):
   - Individual draft files
   - Research notes
   - Meeting records

## Automation Scripts

`scripts/`:

- `weekly_review.py` - Weekly productivity summary
- `content_ideas.py` - Content suggestions from bookmarks
- `idea_to_draft.py <idea-id>` - Expand idea into draft

## Usage Rules

1. **Voice First**: Always read `identity/voice/style.md` before any content generation
2. **Append Only**: Never delete from JSONL files - mark as `"status": "archived"` instead
3. **Update Timestamps**: Set `updated_at` field when modifying tracked data
4. **Cross-Reference**: Knowledge informs content, papers inspire ideas

## Gotchas

操作失败时，优先修复相关模块的设计/指令。如果是跨模块的、暂时无法通过设计消除的问题，临时记到 [gotchas.md](gotchas.md)，修复后删除。

## References

Data directories:
- [Sources](./sources/SOURCES.md) — 外部输入注册表
- [Identity](./identity/voice/principles.md)
- [Content](./content/CONTENT.md)
- [Knowledge](./knowledge/KNOWLEDGE.md)
- [Papers](./knowledge/papers/PAPERS.md) — data only, workflow in `paper-reading` skill
- [Operations](./operations/OPERATIONS.md)
- [Investment](./investment/INVESTMENT.md) — data only, workflow in `investment` skill
- Module Toolkit — workflow in `module-toolkit` skill (`.claude/skills/module-toolkit/`)
