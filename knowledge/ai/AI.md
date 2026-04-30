# AI Knowledge

本目录存放 AI 相关的长期知识材料，包括 agent engineering、context engineering、AI 产品设计、developer tools、persona、认知模拟和 AI 时代的工作方式变化。

## Structure

```text
knowledge/ai/
├── AI.md
└── 文章主题/
    ├── source.md | paper.html
    └── notes.md
```

## 归档规则

- 长文、论文、thread 使用 `paper-reading` skill 处理
- 元数据登记在 `sources/sources.jsonl`
- `output` 指向本目录下的主题笔记，例如 `knowledge/ai/autoharness/notes.md`
- 目录按文章或主题命名，优先使用稳定、可读、短小的英文 slug
- 文章重点若是组织管理而非 AI 机制，放到 `knowledge/organizations/`

## Scope

- AI agents、Claude Code、skills、harness、workflow、coding agents
- Context engineering、memory、knowledge base、文件系统即数据库
- AI 产品形态、Generative UI、人机协作界面
- Developer tools for AI：Git、Cursor、代码索引、安全、工程工具链
- Persona、认知模拟、社会模拟、AI 如何承载人格/经验

## 文章索引

### Context Engineering / Knowledge Systems

- [Everything is Context](./everything-is-context/notes.md) — Agentic File System Abstraction for Context Engineering
- [LLM Knowledge Bases](./llm-knowledge-bases/notes.md) — Karpathy 关于 LLM knowledge bases 的讨论
- [Claude Code Memory 2.0 — AutoDream 功能解读](./claude-code-memory-autodream/notes.md)

### Agents / Skills / Harness

- [Improving Skill-Creator](./improving-skill-creator/notes.md)
- [Design in the Age of AI Agents](./design-in-age-of-ai-agents/notes.md)
- [Harness Engineering](./harness-engineering/notes.md)
- [Claude Cowork: The Ultimate Guide for PMs](./claude-cowork-for-pms/notes.md)
- [Lessons from Building Claude Code](./lessons-from-building-claude-code/notes.md)
- [Improving AI Skills with autoresearch & evals](./improving-ai-skills-autoresearch-evals/notes.md)
- [5 Agent Skill Design Patterns](./agent-skill-design-patterns/notes.md)
- [Skill 调用 Skill](./skill-calls-skill/notes.md)
- [打造高可靠 AI 助手](./reliable-ai-assistants/notes.md)
- [How to 10x your Claude Skills](./ten-x-claude-skills/notes.md)
- [AutoHarness](./autoharness/notes.md)
- [Agent Harness: gstack + Compound Engineering](./agent-harness-gstack-compound-engineering/notes.md)
- [Scaling Managed Agents](./scaling-managed-agents/notes.md)

### AI Product / Interfaces / Tools

- [Design Without Designing](./design-without-designing/notes.md)
- [How Noah Keeps Generative UI and LLM Conversations in Sync](./generative-ui-llm-sync/notes.md)
- [Secure Codebase Indexing](./secure-codebase-indexing/notes.md)
- [Rethinking Git for the Age of Coding Agents](./rethinking-git-for-coding-agents/notes.md)
- [Agents Over Bubbles](./agents-over-bubbles/notes.md)
- [YC 掌门人 gstack 方法论](./gstack-methodology/notes.md)
- [Harness Design for Long-Running Application Development](./harness-design-long-running-apps/notes.md)

### Cognition / Persona / Simulation

- [Simulating Society Requires Simulating Thought](./simulating-society-requires-simulating-thought/notes.md)
- [LLM Generated Persona is a Promise with a Catch](./llm-generated-persona-promise/notes.md)
- [Why Some Expertise Transfers to AI Personas Easily](./expertise-transfer-to-ai-personas/notes.md)
- [Building Trusted AI in the Enterprise](./building-trusted-ai-in-enterprise/notes.md)
- [Claude's Cycles](./claudes-cycles/notes.md)
- [Ralph Wiggum as a Software Engineer](./ralph-wiggum-software-engineer/notes.md)
- [Everything is a Loop](./everything-is-a-loop/notes.md)

### AI and Organizations

- [From Hierarchy to Intelligence](./from-hierarchy-to-intelligence/notes.md) — AI 替代组织层级的信息路由功能
