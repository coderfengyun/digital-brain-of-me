# Papers - Academic Paper Reading

Systematic academic paper reading with a narrative-driven approach. Focus on understanding the **story** each paper tells, then verify with **supporting data**.

## Structure

```
papers/
├── papers.jsonl           # Paper metadata (append-only)
├── paper-YYYYMMDD-XXX/    # Individual paper folder
│   ├── README.md          # Reading notes
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
- `notes` - Reading notes path (e.g., `"paper-YYYYMMDD-XXX/README.md"`)

### Reading Status
- `notes` empty = Not read yet
- `notes` filled = Reading completed

## Paper Note Structure

Each `paper-*.md` contains:

1. **Metadata** - Title only
2. **Narrative Layer**
   - Core narrative (text)
   - Narrative structure (Mermaid diagram)
3. **Evidence Layer** - Table of claims and supporting data
4. **Critical Thinking** - Bullet-point core questions and evaluation
5. **Related Papers** - Connections to other work

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
2. Fill in narrative section and draw Mermaid diagram

### Phase 2: Critical Analysis (30-60 min)

**Goal**: Validate claims with evidence and think critically

**Process**:
1. For each claim in narrative: find supporting data
2. Fill evidence table with data and credibility assessment
3. Complete critical thinking section with bullet-point core questions
4. Update `notes` field in papers.jsonl with README.md path

## Usage

### Adding Papers

**CLI** (using scripts):
```bash
python scripts/add_paper.py "Title" "URL" --tags "nlp,transformer" --year 2024
```

**Manual**:
1. Create folder `paper-YYYYMMDD-XXX/`
2. Copy TEMPLATE.md to `paper-YYYYMMDD-XXX/README.md`
3. Download paper HTML to the folder
4. Append entry to `papers.jsonl` with id, url, html path, and empty notes

### Marking as Read

```bash
# Mark as completed (after finishing reading)
python scripts/update_paper_status.py paper-20260227-001 --completed
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
