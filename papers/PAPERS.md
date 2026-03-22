# Papers - Academic Paper Reading

Systematic academic paper reading with a narrative-driven approach. Focus on understanding the **story** each paper tells, then verify with **supporting data**.

## Structure

```
papers/
├── papers.jsonl           # Paper metadata (append-only)
├── paper-YYYYMMDD-XXX/    # Individual paper folder
│   ├── notes.md           # Reading notes
│   └── source.*           # Source document (paper.html | source.md | source.pdf)
├── TEMPLATE-METHOD.md     # Method paper template
├── TEMPLATE-NARRATIVE.md  # Narrative paper template
├── TEMPLATE-SURVEY.md     # Survey paper template
├── TEMPLATE-THEORY.md     # Theory paper template
└── PAPERS.md              # This file
```

## Data Schema

Each entry in `papers.jsonl`:

```json
{
  "id": "paper-YYYYMMDD-XXX",
  "url": "https://arxiv.org/abs/...",
  "source": "",
  "notes": ""
}
```

### Fields
- `url` - Original URL or local filename
- `source` - Local source document path (ONE of: `paper.html` | `source.md` | `source.pdf`)
- `notes` - Reading notes path (e.g., `"paper-YYYYMMDD-XXX/notes.md"`)

### Reading Status
- `notes` empty = Not read yet
- `notes` filled = Reading completed

## Paper Note Templates

根据论文类型选择对应模板：

| 类型 | 模板 | 适用场景 | 判断标准 |
|------|------|----------|----------|
| 方法 | [TEMPLATE-METHOD.md](TEMPLATE-METHOD.md) | 提出新方法、实验验证 | 有实验、有 baseline 对比、有定量结果 |
| 叙事 | [TEMPLATE-NARRATIVE.md](TEMPLATE-NARRATIVE.md) | 案例研究、故事性文章 | 以时间线或事件为主线，重在讲述过程 |
| 综述 | [TEMPLATE-SURVEY.md](TEMPLATE-SURVEY.md) | 领域综述、文献回顾 | 梳理多篇工作，分类总结，指出趋势 |
| 理论 | [TEMPLATE-THEORY.md](TEMPLATE-THEORY.md) | 数学证明、理论分析 | 核心是定理/命题及其证明 |

**默认选择**: 不确定时使用「方法」模板

<a id="reading-workflow"></a>
## Reading Workflow

**Critical Rules**:
- ALWAYS obtain source document locally before reading
- ALWAYS read from local source, NOT from web fetch
- ALWAYS choose the appropriate template based on paper type (see Paper Note Templates)
- ALWAYS update `papers.jsonl` after each phase

### Phase 0: Obtain Source Document

**Process**:
1. For arxiv papers: Download HTML to `paper-YYYYMMDD-XXX/paper.html`
2. For provided documents: Save to `paper-YYYYMMDD-XXX/source.md` or `source.pdf`
3. Update `source` field in papers.jsonl with the path

### Phase 1: Extract Narrative (1-2 hours)

**Goal**: Understand the story the paper tells

**Process**:
1. Read the full paper thoroughly
2. Write narrative structure as vertical flow with arrows:
   ```
   问题: ...
   ↓
   观察: ...
   ↓
   假设: ...
   ↓
   方法: ...
   ↓
   验证: ...
   ↓
   结论: ...
   ```

### Phase 2: Critical Analysis (30-60 min)

**Goal**: Validate claims with evidence and think critically

**Process**:
1. Create evidence table with columns: 论点 | 创新点 | 支撑数据 | 数据来源 | 说服力评估
2. For each claim: identify innovation, find supporting data, source, and assess credibility
   - **支撑数据填写规则**: 优先使用定量数据；若论点无明确数据支撑，使用 `**例子**: 具体场景描述` 格式记录论文中的示例
3. Complete critical thinking section with 3 core questions
4. Update `notes` field in papers.jsonl with notes.md path

## Usage

### Adding Papers

**CLI**:
```bash
python scripts/add_paper.py "https://arxiv.org/abs/xxxx"
```

**Manual**:
1. Create folder `paper-YYYYMMDD-XXX/`
2. Download source document to the folder
3. Append entry to `papers.jsonl` with id, url, source path, and empty notes
4. After reading, create `notes.md` and update the notes field

## Further Reading

- **[EXAMPLE.md](EXAMPLE.md)** - Example: Attention Is All You Need
