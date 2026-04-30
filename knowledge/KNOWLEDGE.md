# Knowledge Module

This module organizes bookmarks, AI knowledge, organization notes, research notes, and learning materials.

## Structure

### bookmarks/
Save interesting links and resources in `bookmarks.jsonl`.

**Format:**
```json
{
  "id": "bm-XXX",
  "url": "https://...",
  "title": "Resource title",
  "description": "Brief description",
  "tags": ["tag1", "tag2"],
  "saved_at": "YYYY-MM-DD",
  "category": "article|video|tool|paper|documentation"
}
```

### ai/
AI、agent、context engineering、AI 产品、developer tools、persona、认知模拟等内容。长文/论文通过 `paper-reading` skill 处理后，输出到对应主题目录。

### organizations/
组织管理、决策机制、协作方式、公司生产力等内容。与 AI 强相关但重点在 AI 机制的文章，优先放 `ai/`；重点在组织管理的文章放这里。

### research/
Deep research notes on specific topics. This is a temporary incubation area; mature topics should move to a stable domain like `ai/`, `organizations/`, or `investment/`.

### learning/
Track courses, books, and skills you're developing in `courses.yaml`.

### web-clippings/
Saved web pages converted to Markdown for offline reading.

## Sub-Modules

- **ai/** - AI、agent、context engineering、AI 产品和 developer tools。
- **organizations/** - 组织管理、决策机制和协作方式。

## Related Top-Level Modules

- **weekly-review/** - 周记&月结归档. See [../weekly-review/WEEKLY-REVIEW.md](../weekly-review/WEEKLY-REVIEW.md)
- **investment/** - Investment trade journal. See [../investment/INVESTMENT.md](../investment/INVESTMENT.md)

## Usage Tips

- Tag bookmarks consistently for easy retrieval
- Link research notes to related bookmarks using bookmark IDs
- Regularly review and consolidate learning materials
- Weekly review 中的学习记录与 learning/ 模块互相补充

## Extending

Want to add new knowledge types? Follow the [Module Creation Guide](../.claude/skills/module-toolkit/references/MODULE_CREATION_GUIDE.md).
