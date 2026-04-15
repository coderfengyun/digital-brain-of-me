# Papers — 论文阅读笔记

论文/文章的阅读笔记和源文件存放目录。

阅读流程由 `paper-reading` skill 驱动，元数据注册在 `sources/sources.jsonl`。

## Structure

```
knowledge/papers/
├── paper-YYYYMMDD-XXX/    # Individual paper folder
│   ├── notes.md           # Reading notes
│   └── source.*           # Source document (paper.html | source.md | source.pdf)
└── PAPERS.md              # This file
```

模板和示例文件在 `.claude/skills/paper-reading/`（TEMPLATE-*.md, EXAMPLE.md）。

## Data Schema

Paper metadata lives in `sources/sources.jsonl` (type: `"paper"`).

```json
{
  "id": "paper-YYYYMMDD-XXX",
  "type": "paper",
  "source": "https://arxiv.org/abs/... | sources/paper-XXX.pdf",
  "title": "Paper title",
  "tags": [],
  "added_at": "YYYY-MM-DD",
  "output": "knowledge/papers/paper-YYYYMMDD-XXX/notes.md"
}
```

### Reading Status
- `output` empty = Not read yet
- `output` filled = Reading completed
