# Papers — Legacy Reading Archive

`knowledge/papers/` 不再作为新文章的长期归属目录。

`paper` 现在表示一种长文本处理类型：论文、文章、研报、thread、转录稿都可以使用 `paper-reading` skill 处理。处理结果应输出到真实领域目录，而不是默认放在 `knowledge/papers/`。

## Structure

```
knowledge/papers/
├── paper-YYYYMMDD-XXX/    # Legacy reading folders
│   ├── notes.md
│   └── source.*
└── PAPERS.md              # This file
```

模板和阅读流程在 `.claude/skills/paper-reading/`（TEMPLATE-*.md, EXAMPLE.md）。

## Data Schema

Paper metadata lives in `sources/sources.jsonl` (type: `"paper"`). `output` points to the final domain path.

```json
{
  "id": "paper-YYYYMMDD-XXX",
  "type": "paper",
  "source": "https://arxiv.org/abs/... | sources/paper-XXX.pdf",
  "title": "Paper title",
  "tags": [],
  "added_at": "YYYY-MM-DD",
  "output": "knowledge/ai/autoharness/notes.md | investment/洪灏/半导体超级周期/notes.md"
}
```

### Reading Status
- `output` empty = Not read yet
- `output` filled = Reading completed

## Domain Routing

新文章先判断内容归属，再运行阅读流程：

| 内容类型 | 输出位置 |
|---------|----------|
| 投资、宏观、地缘、能源、货币、资产配置、研报 | `investment/{作者或机构}/{文章主题}/notes.md` |
| AI、agent、context engineering、AI 产品、developer tools、persona | `knowledge/ai/{文章主题}/notes.md` |
| 组织管理、决策机制、协作方式 | `knowledge/organizations/{主题}/notes.md` |
| 课程、书籍、系统学习 | `knowledge/learning/` |
| 尚未成熟的探索性主题 | `knowledge/research/`（临时缓冲） |

`knowledge/papers/` 只保留历史兼容和迁移中的材料。不要把新文章默认放进这里。
