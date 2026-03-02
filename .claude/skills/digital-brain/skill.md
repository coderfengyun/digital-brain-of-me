# Digital Brain Skill

A structured knowledge management system for AI-assisted personal productivity.

## Core Capabilities

This skill helps you manage five key areas plus system extension:

1. **Identity** - Personal brand, voice, and values
2. **Content** - Ideas, drafts, and publishing pipeline
3. **Knowledge** - Bookmarks, research, learning materials, and academic papers
4. **Network** - Contacts and relationship management
5. **Operations** - Goals, tasks, meetings, and metrics
6. **Module Toolkit** - Create new modules and extend functionality

## Commands

When invoked with `/digital-brain`, Claude will help you:

- Add and organize content ideas
- Log bookmarks and research
- Add and read academic papers with narrative-driven approach
- Track contacts and interactions
- Manage tasks and goals
- Generate weekly reviews
- Suggest content ideas from your knowledge base
- Identify contacts to reconnect with
- Expand ideas into structured drafts
- Create new modules to extend the system
- Verify module integration completeness

## Data Formats

- **JSONL**: Append-only logs (bookmarks, contacts, tasks, etc.)
- **YAML**: Structured configuration (goals, learning progress)
- **Markdown**: Narrative content (drafts, research notes)

## Automation Scripts

Eight Python scripts in `scripts/`:

1. `weekly_review.py` - Generate weekly productivity review
2. `content_ideas.py` - Suggest content from knowledge base
3. `stale_contacts.py` - Find contacts to reconnect with
4. `idea_to_draft.py` - Expand idea into structured draft
5. `add_paper.py` - Add academic papers to reading list
6. `search_papers.py` - Search and query papers
7. `update_paper_status.py` - Update paper reading status

**Module toolkit**:
- `module-toolkit/check_module_integration.py` - Verify module integration completeness

## Usage Examples

### Adding a content idea
"Add a content idea about AI agents"

### Logging a bookmark
"Save this article about context engineering: https://example.com"

### Adding a contact
"Add John Doe as a colleague, met at AI conference"

### Running weekly review
"Generate my weekly review"

### Getting content suggestions
"What should I write about next?"

### Adding a paper to read
"Add the Attention Is All You Need paper to my reading list"

### Reading a paper
"Guide me through reading this paper with the narrative-driven approach"

### Checking unread papers
"Show me all my unread papers on transformers"

### Creating a new module
"I want to create a projects module to track my side projects"

### Verifying module integration
"Check if the papers module is properly integrated"

## Design Principles

- **Progressive disclosure**: Load only what's needed
- **Append-only**: Preserve history
- **Module separation**: Independent domains
- **Voice-first**: Maintain personal brand consistency
