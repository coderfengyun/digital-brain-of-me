---
name: digital-brain
description: "Personal knowledge management system. Use when: user asks about bookmarks, papers, podcasts, contacts, tasks, goals, investment trades, content ideas, weekly review, reading papers, transcribing podcasts, P&L calculation, adding trades, creating modules, or any personal knowledge management task. Also trigger on Chinese phrases like 书签, 论文, 播客, 联系人, 任务, 目标, 交易记录, 内容创意, 周报, 盈亏, 更新交易记录, 写一篇文章, 保存这个链接, 我的目标, 添加论文, 读论文. Use this skill even if the user doesn't explicitly mention 'digital brain' — any request involving personal data management, knowledge capture, or content creation should route here."
---

# Digital Brain

个人数字操作系统：管理数字身份、知识、人脉、目标和投资。

> **本文件定位**：使用 digital-brain 时的操作手册——路由、加载策略、脚本列表、使用规则。修改/扩展系统本身的开发约定见 `CLAUDE.md`。

Module-specific instructions are in each subdirectory's `.md` file. Only load what's needed for the current task.

## When to Activate

Activate this skill when the user:

- Requests content creation (posts, threads, newsletters) - load `identity/voice/style.md` first
- Asks for help with personal brand or positioning
- Needs to look up or manage contacts/relationships
- Wants to capture or develop content ideas
- Requests meeting preparation or follow-up
- Asks for weekly reviews or goal tracking
- Needs to save or retrieve bookmarked resources
- Wants to organize research or learning materials
- Needs to add, read, or manage academic papers
- Wants to transcribe podcast episodes
- Needs to record, import, or analyze investment trades
- Wants to extend the system or create new modules

**Trigger phrases**: "write a post", "my voice", "content ideas", "who is [name]", "prepare for meeting", "weekly review", "save this", "my goals", "add paper", "read paper", "paper reading", "transcribe podcast", "podcast transcript", "交易记录", "investment", "盈亏", "add trade", "import trades", "更新交易记录", "create module", "add module", "extend system"

## Module Overview

```
digital-brain-of-me/
├── identity/     → Voice, brand, values (READ FIRST for content)
├── content/      → Ideas, drafts, posts, calendar
├── knowledge/    → Bookmarks, research, learning
├── papers/       → Academic paper reading and notes
├── podcasts/     → Podcast transcription and notes
├── network/      → Contacts, interactions, intros
├── operations/   → Todos, goals, meetings, metrics
├── investment/   → Trade journal, broker imports, P&L analysis
└── scripts/      → Automation scripts
```

## Request Routing

| Request | Action |
|---------|--------|
| "Write a post about X" | Read `identity/voice/style.md` → Draft → Match voice patterns |
| "Prepare for meeting with Y" | Look up in `network/contacts/contacts.jsonl` → Get `network/relationships/interactions.jsonl` → Summarize |
| "What should I create?" | Run `scripts/content_ideas.py` → Check `content/ideas/ideas.jsonl` |
| "Add contact Z" | Append to `network/contacts/contacts.jsonl` with full schema |
| "Weekly review" | Run `scripts/weekly_review.py` → Present insights |
| "Save this bookmark" | Append to `knowledge/bookmarks/bookmarks.jsonl` |
| "Add a task" | Append to `operations/tasks/tasks.jsonl` with priority |
| "Track a goal" | Update `operations/goals/goals.yaml` with progress |
| "Add paper to read" | Run `scripts/add_paper.py "URL"` → Create paper folder |
| "Read this paper" | Read `papers/PAPERS.md` → Guide through 2-phase reading → Update status |
| "Show unread papers" | Read `papers/papers.jsonl`, filter entries where `notes` is empty |
| "Transcribe this podcast" | Run `scripts/transcribe_podcast.py` with RSS or audio file |
| "Add trade" / "交易记录" / "更新交易记录" / "盈亏" | Read `investment/INVESTMENT.md` for usage instructions |
| "Create new module" | Read `module-toolkit/MODULE_CREATION_GUIDE.md` → Guide through phases |
| "Check module integration" | Run `module-toolkit/check_module_integration.py <module> <keyword>` |

## Module Loading Strategy

Use **progressive disclosure**:

1. **Always Load** (L1):
   - `gotchas.md` (check known pitfalls before any operation)

2. **Load on Content Creation Tasks** (L2):
   - `identity/brand/profile.yaml`
   - `identity/voice/style.md`
   - `content/ideas/ideas.jsonl`
   - `content/published/published.jsonl`
   - `knowledge/bookmarks/bookmarks.jsonl`

3. **Load on Paper Tasks** (L2):
   - `papers/PAPERS.md` + `papers/papers.jsonl`

4. **Load on Podcast Tasks** (L2):
   - `podcasts/PODCASTS.md` + `podcasts/podcasts.jsonl`

5. **Load on Network Tasks** (L2):
   - `network/contacts/contacts.jsonl`
   - `network/relationships/interactions.jsonl`

6. **Load on Operations Tasks** (L2):
   - `operations/tasks/tasks.jsonl`
   - `operations/goals/goals.yaml`
   - `operations/metrics/weekly.jsonl`

7. **Load on Investment Tasks** (L2):
   - `investment/INVESTMENT.md`
   - `investment/投资日志整理/交易日志汇总表.csv`
   - `investment/投资日志整理/交易日志汇总表.schema.json`

8. **Load on Module Creation / Integration Tasks** (L2):
   - `module-toolkit/MODULE-TOOLKIT.md`
   - `module-toolkit/MODULE_CREATION_GUIDE.md` (if creating a new module manually)

9. **Load on Demand** (L3):
   - Individual draft files
   - Research notes
   - Paper notes (`paper-YYYYMMDD-XXX.md`)
   - Meeting records

## Automation Scripts

`scripts/`:

- `weekly_review.py` - Weekly productivity summary
- `content_ideas.py` - Content suggestions from bookmarks
- `stale_contacts.py` - Identify people to reconnect with
- `idea_to_draft.py <idea-id>` - Expand idea into draft
- `add_paper.py "URL"` - Add paper to reading list
- `transcribe_podcast.py` - Transcribe podcasts from RSS or local audio

`investment/投资日志整理/scripts/`:

- `write_trade_journal.py` - Add, import, migrate, and validate trade records
- `fetch_binance_trades.py` - Fetch trades from Binance API
- `fetch_futu_trades.py` - Fetch trades from Futu OpenD API
- `fetch_cms_trades.py` - Fetch trades from 招商证券 via Chrome MCP
- `calc_pnl.py` - FIFO-based P&L calculation

`module-toolkit/`:

- `check_module_integration.py <module> <keyword>` - Verify module integration

## Usage Rules

1. **Voice First**: Always read `identity/voice/style.md` before any content generation
2. **Append Only**: Never delete from JSONL files - mark as `"status": "archived"` instead
3. **Update Timestamps**: Set `updated_at` field when modifying tracked data
4. **Cross-Reference**: Knowledge informs content, network informs operations, papers inspire ideas
5. **Log Interactions**: Always log meetings/calls to `interactions.jsonl`
6. **Narrative First**: For papers, extract narrative structure before diving into data details

## Gotchas

When an operation fails or produces unexpected results, append the lesson to [gotchas.md](gotchas.md).

## References

- [Identity Module](./identity/voice/principles.md)
- [Content Module](./content/CONTENT.md)
- [Knowledge Module](./knowledge/KNOWLEDGE.md)
- [Papers Module](./papers/PAPERS.md)
- [Network Module](./network/NETWORK.md)
- [Operations Module](./operations/OPERATIONS.md)
- [Investment Module](./investment/INVESTMENT.md)
- [Module Creation Guide](./module-toolkit/MODULE_CREATION_GUIDE.md)
