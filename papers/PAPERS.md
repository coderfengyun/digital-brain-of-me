# Papers - Academic Paper Reading

Systematic academic paper reading with a narrative-driven approach. Focus on understanding the **story** each paper tells, then verify with **supporting data**.

## Structure

```
papers/
├── papers.jsonl           # Paper metadata (append-only)
├── paper-YYYYMMDD-XXX/    # Individual paper folder
│   ├── notes.md           # Reading notes
│   ├── paper.html         # Downloaded HTML version
│   └── paper.pdf          # Downloaded PDF (optional)
├── TEMPLATE.md            # Note template
└── PAPERS.md              # This file
```

## Data Schema

Each entry in `papers.jsonl`:

```json
{
  "id": "paper-YYYYMMDD-XXX",
  "url": "https://arxiv.org/abs/...",
  "html": "",
  "notes": ""
}
```

### Fields
- `url` - Original paper URL
- `html` - Local HTML version path (e.g., `"paper-YYYYMMDD-XXX/paper.html"`)
- `notes` - Reading notes path (e.g., `"paper-YYYYMMDD-XXX/notes.md"`)

### Reading Status
- `notes` empty = Not read yet
- `notes` filled = Reading completed

## Paper Note Structure

Each `paper-*.md` contains:

1. **Metadata** - Title only
2. **Narrative Layer**
   - Core narrative (text)
   - Narrative structure (arrow-connected flow)
3. **Evidence Layer** - Table of claims and supporting data (optional: key figure/table interpretations)
4. **Critical Thinking** - Bullet-point core questions and evaluation

## Reading Workflow

### Phase 0: Download Paper

**Process**:
1. Download HTML version of the paper to `paper-YYYYMMDD-XXX/paper.html`
2. Update `html` field in papers.jsonl with the path
3. Save PDF if needed for reference

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
3. Complete critical thinking section with 3 core questions
4. Update `notes` field in papers.jsonl with notes.md path

## Usage

### Adding Papers

**CLI** (using scripts):
```bash
python scripts/add_paper.py "Title" "URL" --tags "nlp,transformer" --year 2024
```

**Manual**:
1. Create folder `paper-YYYYMMDD-XXX/`
2. Copy TEMPLATE.md to `paper-YYYYMMDD-XXX/notes.md`
3. Download paper HTML to the folder
4. Append entry to `papers.jsonl` with id, url, html path, and empty notes


## Integration with Other Modules

**bookmarks → papers**: Discover papers worth deep reading
**papers → research**: Synthesize insights across multiple papers
**papers → ideas**: Paper insights inspire content ideas
**papers → tasks**: Follow-up actions from paper reading
**papers → contacts**: Connect with paper authors

## Further Reading

- **[TEMPLATE.md](TEMPLATE.md)** - Empty note template
- **[EXAMPLE.md](EXAMPLE.md)** - Example: Attention Is All You Need
- **[QUICKSTART.md](QUICKSTART.md)** - 5-minute tutorial
- **[OVERVIEW.md](OVERVIEW.md)** - Design philosophy
- **[INTEGRATION.md](INTEGRATION.md)** - Cross-module workflows
