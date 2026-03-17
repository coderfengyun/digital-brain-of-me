# Claude Cowork: The Ultimate Guide for PMs

**Author:** Pawel Huryn (@PawelHuryn)
**Source:** X/Twitter Article
**Published:** 2026-02-22
**URL:** https://x.com/pawelhuryn/status/2025470280945041547
**Engagement:** 58 replies | 450 retweets | 3.6K likes | 11K bookmarks | 1.4M views

---

Anthropic just shipped Claude Cowork for Windows and Intel-based macOS with full feature parity to the version released in January. It's now available on all platforms for Pro, Max, Team, and Enterprise plans.

Everyone's hyping Claude Code. But if you're not a developer, Cowork might be a better default option for everyday tasks -- and almost nobody's talking about it enough.

I'm a former engineer. I can use the terminal just fine. But prototyping aside, I choose Cowork for day-to-day work: analyzing and drafting emails, reorganizing files, preparing contracts, managing invoices, and even configuring my OS.

Same model as Claude Code. Same skill format, same connector types.

Technically, Code can do everything Cowork does. The difference is how you get there. Code needs git worktrees, tmux, and CLI flags. Cowork gives you a simple visual interface.

This guide covers everything you need to know:

1. What Cowork Actually Is
2. Cowork vs. Chat: Why it's a Different Beast
3. Plugins and Skills in Claude Cowork
4. MCPs: Connecting Cowork to Your World
5. Scheduled Tasks
6. A 1-Minute Hack That Makes Claude Desktop 2x More Powerful
7. How to Give Claude Cowork Cross-Session Memory

------

## 1. What Cowork Actually Is

Cowork is not a chat interface with a new skin. It's an autonomous desktop agent built into the Claude Desktop app.

When you open the Cowork tab, you're giving Claude access to a sandboxed Linux VM running on your machine. Inside that sandbox, Claude can write code, execute scripts, create files (Word docs, slide decks, spreadsheets, PDFs), and connect to services like Gmail, GitHub, and Slack (you don't set this up -- Anthropic manages it).

You describe what you need. Cowork plans the work, breaks it into sub-agents that run in parallel, and delivers output as clickable files you can open directly.

A few things that set it apart from Chat:

- **It plans and tracks work.** Give Cowork a complex task and it decomposes it into subtasks, shows you the plan, and works through it step by step. You can watch progress in real time and steer mid-task. Chat doesn't do this.
- **It coordinates parallel work.** Cowork can spawn sub-agents -- independent Claude instances that each get their own context -- to work on different parts of a task simultaneously.
- **It creates real files.** Not an artifact. Actual .docx, .pptx, .xlsx, and .pdf files delivered to the folder you granted access to.
- **It's sandboxed -- but not entirely.** Cowork runs in a VM, so it can't touch your OS or files outside the folder you shared. But inside that folder, it has full read/write/delete access.
- **It connects to your tools.** Gmail, GitHub, Slack, Google Drive, and more via built-in connectors. Plus any custom tool via MCP servers.

------

## 2. Cowork vs. Chat: Why it's a Different Beast

Many of you already use Claude Chat in the Desktop app. You might be wondering: what does Cowork add?

Chat is for conversations. Cowork is for workflows.

In short, Cowork adds what matters for getting real work done: sub-agent coordination that handles parallel work, task decomposition, and files delivered directly to your folder instead of chat artifacts.

------

## 3. Plugins and Skills in Claude Cowork

When Anthropic unveiled AI tools automating legal and financial research in early 2026, legacy software stocks dropped $285 billion in a single day. Investors saw AI agents moving into the application layer -- legal, sales, marketing, finance -- and repriced the entire software sector.

The plugins sitting in your Cowork sidebar are part of what triggered that reaction. Here's how they work.

### What Are Skills?

Skills are reusable instruction manuals that teach Claude how to approach specific, repeatable tasks. Say "create a Word doc" and the docx skill loads. You can also trigger skills explicitly -- type / in Cowork for autocomplete.

The format works across Claude ecosystem and third-party tools like Cursor, Windsurf, and Codex CLI.

Built-in skills include pdf, docx, pptx, xlsx, canvas-design, algorithmic-art, and skill-creator.

Skills don't all load at once. Claude reads only a short description of each skill (~100 tokens) to decide which ones are relevant, then loads full instructions only when needed. This keeps your context window clean.

### The Cowork Plugin Panel

Cowork has a dedicated Plugins panel that Chat doesn't. You can browse, install, upload, and create plugins from a visual UI.

Each plugin bundles skills with slash commands, for example "Product Management".

### Skill and Plugin Access Across Tools

- Default plugins:
  - Cowork ships with 11 plugins from anthropics/knowledge-work-plugins (productivity, product-management, legal, finance, marketing, data, etc.)
  - Code's marketplace defaults to anthropics/claude-code (developer workflows: agent-sdk-dev, frontend-design, feature-dev, code-review, etc.).
- But you can add any marketplace repo to either tool -- load Code's developer plugins into Cowork, or Cowork's business plugins into Code. Same skill format, fully cross-compatible.
- Note: Cowork and Code Tab have separate, isolated plugin panels. Installing a plugin in one doesn't make it available in the other. Skills uploaded via Claude Desktop settings are shared across Chat, Cowork, and Code Tab.

### Where to Find More Skills and Plugins

Beyond built-in skills and Anthropic's plugins, there's a growing ecosystem worth exploring. All essential sources:

- github.com/anthropics/skills -- Anthropic's official repo. Document skills (docx, xlsx, pptx, pdf) plus creative, technical, and enterprise examples
- github.com/anthropics/knowledge-work-plugins -- Cowork's default plugin registry. The 11 business-role plugins
- github.com/anthropics/claude-code -- Developer-focused workflows. Code's marketplace, open "Plugins"
- claudemarketplaces.com -- A marketplace of marketplaces you can add to Cowork or Code
- github.com/travisvn/awesome-claude-skills -- Community-curated. Battle-tested skills for TDD, debugging, collaboration
- github.com/sickn33/antigravity-awesome-skills -- 868+ universal agentic skills. Role-based bundles: Startup Founder, Marketing & Growth, and more
- skills.sh -- Product strategy frameworks, pricing strategy, launch playbooks, discovery interview guides, PRD generator, analytics, resume optimizer

------

## 4. MCPs: Connecting Cowork to Your World

MCP stands for Model Context Protocol -- the open standard by Anthropic. Each MCP server exposes tools Claude can call.

A custom Gmail MCP gives Claude search_emails, send_email, read_email. The official GitHub MCP gives it create_pull_request, list_issues.

### Three types of MCP connections:

1. **Remote and custom connectors** -- work everywhere including claude.ai in your browser. You add them in "Connectors > Manage connectors".
2. **Extensions** -- how Anthropic packages local MCP servers for one-click install. They show up in both the Extensions panel (to install/remove) and the Connectors panel (to toggle on/off). You manage them in "Settings > Extensions".
3. **Custom MCP servers** -- managed by editing a JSON config. Click "Menu > Developer > App Config File..."

Example content with custom Gmail and Outlook MCPs:

```json
{
  "mcpServers": {
    "gmail": {
      "command": "npx",
      "args": [
        "@gongrzhe/server-gmail-autoauth-mcp"
      ]
    },
    "outlook-assistant": {
      "command": "C:\\nvm4w\\nodejs\\node.exe",
      "args": [
        "C:\\Users\\Dell\\outlook-mcp\\index.js"
      ],
      "env": {
        "USE_TEST_MODE": "false",
        "OUTLOOK_CLIENT_ID": "6c****-**************",
        "OUTLOOK_CLIENT_SECRET": "53**************_**************"
      }
    }
  }
}
```

### Per-Tool Permissions

For every connector, you can set individual tools to Allow (runs automatically), Ask (confirms before running), or Block (never runs). You could allow Claude to search your emails but block it from sending them.

### MCP Config Is Not Shared Across All Tools

Adding an MCP server to Chat makes it available in Cowork and Code Tab, but not Code CLI.

Windows gotcha: If you installed Claude Desktop via the Microsoft Store (MSIX), the "Edit Config" button may open the wrong file.

### Where to Find MCP Servers

- github.com/modelcontextprotocol/servers -- Official MCP server repo
- modelcontextprotocol.io/examples -- Official MCP directory
- github.com/punkpeye/awesome-mcp-servers -- Community-curated list
- mcp.so -- MCP server registry with search and install instructions

------

## 5. Scheduled Tasks

Scheduled tasks feature exists but is unreliable in the author's tests. For scheduled automation, n8n or an MCP-based approach will serve you better.

------

## 6. A 1-Minute Hack That Makes Claude Desktop 2x More Powerful

Desktop Commander -- one of the highest-ROI moves, takes < 1 minute:

1. Open Claude Desktop
2. In a chat window click: "+ > Connectors > Manage connectors"
3. Click: "Browse connectors > All > Desktop Commander"
4. Select tools that do not require your approval

The result: Chat, Cowork, and Code Tab can do virtually anything on your laptop including installing MCP servers or accessing any file.

Tips:
- Disable the Claude in Chrome extension when not needed, so Claude doesn't default to web-based actions.
- Consider which actions require your approval. Unlike OpenClaw, none of those tools can take actions on their own. You can also observe what they are doing or disable the connector when not in use.

------

## 7. How to Give Claude Cowork Cross-Session Memory

Two simple steps:

1. Enable Desktop Commander extensions in "Settings > Connectors"
2. Copy this to "Settings > Cowork > Global instructions":

```markdown
## Memory Management

When you discover something valuable for future sessions -- architectural decisions,
bug fixes, gotchas, environment quirks -- immediately append it to {your_folder}/memory.md

Don't wait to be asked. Don't wait for session end.

Keep entries short: date, what, why. Read this file at the start of every session.
```

This costs almost zero tokens and survives crashes, compaction, and new sessions.

### Advanced: Structured Memory

Split into multiple files so Claude loads only what's relevant:

```markdown
## Memory Management

Maintain a structured memory system rooted at .claude/memory/

### Structure

- memory.md -- index of all memory files, updated whenever you create or modify one
- general.md -- cross-project facts, preferences, environment setup
- domain/{topic}.md -- domain-specific knowledge (one file per topic)
- tools/{tool}.md -- tool configs, CLI patterns, workarounds

### Rules

1. When you learn something worth remembering, write it to the right file immediately
2. Keep memory.md as a current index with one-line descriptions
3. Entries: date, what, why -- nothing more
4. Read memory.md at session start. Load other files only when relevant
5. If a file doesn't exist yet, create it

### Maintenance

When I say "reorganize memory":
1. Read all memory files
2. Remove duplicates and outdated entries
3. Merge entries that belong together
4. Split files that cover too many topics
5. Re-sort entries by date within each file
6. Update memory.md index
7. Show me a summary of what changed
```

Example of what Claude Code writes to /memory/tools/docker.md:

```markdown
## Docker

- 2026-02-12: Must use `host.docker.internal` not `localhost` for DB connections from containers -- spent 30 min debugging this
- 2026-02-13: Project Dockerfile needs `--platform=linux/amd64` on M1 Macs or builds silently produce broken images
- 2026-02-13: docker compose v2 uses `docker compose` (no hyphen) -- old scripts with `docker-compose` fail on CI
```

### Bonus: How to Give Claude Code (Tab/CLI) Memory

- For short term memory "Claude forgot what we discussed yesterday":
  - In the Code Tab sessions are visible in the left menu
  - In Claude Code CLI use --continue to continue the previous session
- Paste the same prompt into your Claude Code instructions but replace your custom path with ".claude/memory.md"
- An alternative only for Claude Code (.md format is often more than you need): github.com/thedotmack/claude-mem

```bash
/plugin marketplace add thedotmack/claude-mem
/plugin install claude-mem
```

------

## [Bonus] A Visual Summary: Claude Chat vs. Cowork vs. Code

Download as PDF: https://drive.google.com/file/d/1I1j8QA2_50mvFWe-S3A_YIt8sP8xfvzR/view?usp=sharing

------

Thanks for Reading The Product Compass. Next week: more about Claude Code, creating skills, and dozens of PM plugins and skills.
