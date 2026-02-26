# Digital Brain Skill

A structured knowledge management system for AI-assisted personal productivity.

## Core Capabilities

This skill helps you manage five key areas:

1. **Identity** - Personal brand, voice, and values
2. **Content** - Ideas, drafts, and publishing pipeline
3. **Knowledge** - Bookmarks, research, and learning materials
4. **Network** - Contacts and relationship management
5. **Operations** - Goals, tasks, meetings, and metrics

## Commands

When invoked with `/digital-brain`, Claude will help you:

- Add and organize content ideas
- Log bookmarks and research
- Track contacts and interactions
- Manage tasks and goals
- Generate weekly reviews
- Suggest content ideas from your knowledge base
- Identify contacts to reconnect with
- Expand ideas into structured drafts

## Data Formats

- **JSONL**: Append-only logs (bookmarks, contacts, tasks, etc.)
- **YAML**: Structured configuration (goals, learning progress)
- **Markdown**: Narrative content (drafts, research notes)

## Automation Scripts

Four Python scripts in `scripts/`:

1. `weekly_review.py` - Generate weekly productivity review
2. `content_ideas.py` - Suggest content from knowledge base
3. `stale_contacts.py` - Find contacts to reconnect with
4. `idea_to_draft.py` - Expand idea into structured draft

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

## Design Principles

- **Progressive disclosure**: Load only what's needed
- **Append-only**: Preserve history
- **Module separation**: Independent domains
- **Voice-first**: Maintain personal brand consistency
