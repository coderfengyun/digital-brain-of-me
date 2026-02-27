# Papers - Academic Paper Reading

Systematic academic paper reading with a narrative-driven approach. Focus on understanding the **story** each paper tells, then verify with **supporting data**.

## Structure

```
papers/
├── papers.jsonl           # Paper metadata (append-only)
├── paper-*.md             # Reading notes
└── PAPERS.md              # This file
```

## Data Schema

Each entry in `papers.jsonl`:

```json
{
  "id": "paper-YYYYMMDD-XXX",
  "title": "Paper Title",
  "authors": ["Author 1", "Author 2"],
  "year": 2024,
  "venue": "Conference/Journal",
  "url": "https://arxiv.org/abs/...",
  "pdf_path": "",
  "tags": ["domain", "method", "application"],
  "reading_status": "unread",
  "main_claim": "",
  "added_at": "YYYY-MM-DD",
  "read_at": "",
  "related_papers": []
}
```

### Status Values
- `unread` - Not started
- `reading` - Phase 1 completed (narrative extracted)
- `completed` - Phase 2 completed (data verified)

### Tag Categories
- **Domain**: `nlp`, `cv`, `ml`, `systems`, `hci`, `theory`
- **Method**: `transformer`, `rl`, `diffusion`, `optimization`
- **Application**: `generation`, `understanding`, `reasoning`, `multimodal`

## Paper Note Structure

Each `paper-*.md` contains:

1. **Metadata** - Title, authors, links, dates
2. **Narrative Layer**
   - Core narrative (text)
   - Narrative structure (Mermaid diagram)
3. **Evidence Layer** - Table of claims and supporting data
4. **Critical Thinking** - Evaluation and insights
5. **Related Papers** - Connections to other work

## Reading Workflow

### Phase 1: Extract Narrative (15-30 min)

**Goal**: Understand the story the paper tells

**Process**:
1. Read: Abstract → Intro → Conclusion → Section headers
2. Fill in narrative section and draw Mermaid diagram
3. Update `main_claim` in papers.jsonl
4. Set status to `reading`

### Phase 2: Verify Data (1-2 hours)

**Goal**: Validate claims with evidence

**Process**:
1. For each claim in narrative: find supporting data
2. Fill evidence table with data and credibility assessment
3. Complete critical thinking section
4. Set status to `completed`, update `read_at`

## Usage

### Adding Papers

**CLI** (using scripts):
```bash
python scripts/add_paper.py "Title" "URL" --tags "nlp,transformer" --year 2024
```

**Manual**:
1. Append entry to `papers.jsonl`
2. Create `paper-YYYYMMDD-XXX.md` from template

### Searching Papers

```bash
# Find unread papers
python scripts/search_papers.py --status unread

# Search by tags
python scripts/search_papers.py --tags nlp,transformer

# Full-text search in notes
grep -r "attention mechanism" knowledge/papers/*.md

# View statistics
python scripts/search_papers.py --stats
```

### Updating Status

```bash
# Mark as reading (after Phase 1)
python scripts/update_paper_status.py paper-20260227-001 \
  --status reading \
  --claim "Transformers achieve SOTA with pure attention"

# Mark as completed (after Phase 2)
python scripts/update_paper_status.py paper-20260227-001 --status completed
```

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
