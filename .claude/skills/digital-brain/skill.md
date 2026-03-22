---
description: "Use when: user asks about bookmarks, papers, podcasts, contacts, tasks, goals, investment trades, content ideas, weekly review, reading papers, transcribing podcasts, P&L calculation, adding trades, creating modules, or any personal knowledge management task."
---

# Digital Brain Skill

## Core Capabilities

This skill helps you manage seven key areas plus system extension:

1. **Identity** - Personal brand, voice, and values
2. **Content** - Ideas, drafts, and publishing pipeline
3. **Knowledge** - Bookmarks, research, and learning materials
4. **Papers** - Academic paper reading with narrative-driven approach
5. **Podcasts** - Podcast transcription via RSS feed or local audio (whisper.cpp)
6. **Network** - Contacts and relationship management
7. **Operations** - Goals, tasks, meetings, and metrics
8. **Investment** - Trade journal, broker imports (Binance/Futu), and FIFO-based P&L analysis
9. **Module Toolkit** - Create new modules and extend functionality

## Commands

When invoked with `/digital-brain`, Claude will help you:

- Add and organize content ideas
- Log bookmarks and research
- Add and read academic papers with narrative-driven approach
- Transcribe podcast episodes from RSS feeds or local audio files
- Track contacts and interactions
- Manage tasks and goals
- Generate weekly reviews
- Suggest content ideas from your knowledge base
- Identify contacts to reconnect with
- Expand ideas into structured drafts
- Record investment trades manually or import from brokers
- Calculate realized and floating P&L across all positions
- Create new modules to extend the system
- Verify module integration completeness

## Data Formats

- **JSONL**: Append-only logs (bookmarks, contacts, tasks, etc.)
- **YAML**: Structured configuration (goals, learning progress)
- **Markdown**: Narrative content (drafts, research notes)
- **CSV**: Tabular data with schema validation (investment trades)

## Automation Scripts

Eight Python scripts in `scripts/`:

1. `weekly_review.py` - Generate weekly productivity review
2. `content_ideas.py` - Suggest content from knowledge base
3. `stale_contacts.py` - Find contacts to reconnect with
4. `idea_to_draft.py` - Expand idea into structured draft
5. `add_paper.py` - Add academic papers to reading list
6. `transcribe_podcast.py` - Transcribe podcasts from RSS or local audio

**Investment scripts** in `investment/投资日志整理/scripts/`:
- `write_trade_journal.py` - Add, import, migrate, and validate trade records
- `fetch_binance_trades.py` - Fetch trades from Binance API
- `fetch_futu_trades.py` - Fetch trades from Futu (placeholder)
- `calc_pnl.py` - FIFO-based P&L calculation and report generation

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

### Transcribing a podcast
"Transcribe this podcast from RSS: https://example.com/feed.xml"

### Transcribing a local audio file
"Transcribe this audio file: ~/Downloads/episode.mp3"

### Adding an investment trade
"Add a BTC buy trade: 0.00391 at $76653 on 2025-04-07"

### Calculating investment P&L
"Calculate my investment P&L"

### Creating a new module
"I want to create a projects module to track my side projects"

### Verifying module integration
"Check if the papers module is properly integrated"

## Gotchas

Read [gotchas.md](gotchas.md) before operating on digital-brain data. When an operation fails or produces unexpected results, append the lesson there.

## Design Principles

- **Progressive disclosure**: Load only what's needed
- **Append-only**: Preserve history
- **Module separation**: Independent domains
- **Voice-first**: Maintain personal brand consistency
