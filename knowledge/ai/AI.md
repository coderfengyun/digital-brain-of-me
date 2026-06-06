# AI Knowledge

本目录存放 AI 相关的长期知识材料，包括 agent engineering、context engineering、AI 产品设计、developer tools、persona、认知模拟和 AI 时代的工作方式变化。

## Structure

```text
knowledge/ai/
├── AI.md
└── YYYYMMDD-文章主题/
    ├── source.md | paper.html
    └── notes.md
```

## 归档规则

- 长文、论文、thread 使用 `paper-reading` skill 处理
- 元数据登记在 `sources/sources.jsonl`
- `output` 指向本目录下的主题笔记，例如 `knowledge/ai/20260327a-autoharness/notes.md`
- 目录命名格式 `YYYYMMDD-slug`（发布日期前缀 + 英文短标题），同日多篇追加字母
- 文章重点若是组织管理而非 AI 机制，放到 `knowledge/organizations/`

## Scope

- AI agents、Claude Code、skills、harness、workflow、coding agents
- Context engineering、memory、knowledge base、文件系统即数据库
- AI 产品形态、Generative UI、人机协作界面
- Developer tools for AI：Git、Cursor、代码索引、安全、工程工具链
- Persona、认知模拟、社会模拟、AI 如何承载人格/经验

## 文章索引

### Context Engineering / Knowledge Systems

- [Everything is Context](./20260302-everything-is-context/notes.md) — Agentic File System Abstraction for Context Engineering
- [LLM Knowledge Bases](./20260407c-llm-knowledge-bases/notes.md) — Karpathy 关于 LLM knowledge bases 的讨论
- [Claude Code Memory 2.0 — AutoDream 功能解读](./20260407a-claude-code-memory-autodream/notes.md)

### Agents / Skills / Harness

- [Improving Skill-Creator](./20260310-improving-skill-creator/notes.md)
- [Design in the Age of AI Agents](./20260316b-design-in-age-of-ai-agents/notes.md)
- [Harness Engineering](./20260316d-harness-engineering/notes.md)
- [Claude Cowork: The Ultimate Guide for PMs](./20260316a-claude-cowork-for-pms/notes.md)
- [Lessons from Building Claude Code](./20260318-lessons-from-building-claude-code/notes.md)
- [Improving AI Skills with autoresearch & evals](./20260324b-improving-ai-skills-autoresearch-evals/notes.md)
- [5 Agent Skill Design Patterns](./20260324a-agent-skill-design-patterns/notes.md)
- [Skill 调用 Skill](./20260325c-skill-calls-skill/notes.md)
- [打造高可靠 AI 助手](./20260327b-reliable-ai-assistants/notes.md)
- [How to 10x your Claude Skills](./20260327d-ten-x-claude-skills/notes.md)
- [AutoHarness](./20260327a-autoharness/notes.md)
- [Agent Harness: gstack + Compound Engineering](./20260330-agent-harness-gstack-compound-engineering/notes.md)
- [Scaling Managed Agents](./20260416-scaling-managed-agents/notes.md)

### AI Product / Interfaces / Tools

- [Design Without Designing](./20260323-design-without-designing/notes.md)
- [How Noah Keeps Generative UI and LLM Conversations in Sync](./20260331b-generative-ui-llm-sync/notes.md)
- [Secure Codebase Indexing](./20260327c-secure-codebase-indexing/notes.md)
- [Rethinking Git for the Age of Coding Agents](./20260421-rethinking-git-for-coding-agents/notes.md)
- [Agents Over Bubbles](./20260331a-agents-over-bubbles/notes.md)
- [YC 掌门人 gstack 方法论](./20260325a-gstack-methodology/notes.md)
- [Harness Design for Long-Running Application Development](./20260325b-harness-design-long-running-apps/notes.md)

### Cognition / Persona / Simulation

- [Simulating Society Requires Simulating Thought](./20260304-simulating-society-requires-simulating-thought/notes.md)
- [LLM Generated Persona is a Promise with a Catch](./20260305b-llm-generated-persona-promise/notes.md)
- [Why Some Expertise Transfers to AI Personas Easily](./20260305a-expertise-transfer-to-ai-personas/notes.md)
- [Building Trusted AI in the Enterprise](./20260306-building-trusted-ai-in-enterprise/notes.md)
- [Claude's Cycles](./20260309-claudes-cycles/notes.md)
- [Ralph Wiggum as a Software Engineer](./20260316e-ralph-wiggum-software-engineer/notes.md)
- [Everything is a Loop](./20260316c-everything-is-a-loop/notes.md)

### AI and Organizations

- [From Hierarchy to Intelligence](./20260407b-from-hierarchy-to-intelligence/notes.md) — AI 替代组织层级的信息路由功能

### Engineering Practices / Vibe Coding

- [OpenAI Realtime Voice Architecture](./20260506a-openai-realtime-voice-architecture/notes.md)
- [Vibe Coding vs Agentic Engineering](./20260506b-vibe-coding-vs-agentic-engineering/notes.md)
- [Interaction Models](./20260512-interaction-models/notes.md)
- [Coding Will Eat All Knowledge Work](./20260515a-coding-will-eat-all-knowledge-work/notes.md)
- [Eval Agent Skills](./20260515b-eval-agent-skills/notes.md)
- [Harness Engineering (LatentSpace)](./20260515c-harness-engineering-latentspace/notes.md)
- [Harness Engineering (OpenAI)](./20260515d-harness-engineering-openai/notes.md)
- [Canvas & Agentic UI](./20260526-canvas-agentic-ui/notes.md)
- [Dynamic Workflows in Claude Code](./20260603a-dynamic-workflows-claude-code/notes.md)
- [Research Rubrics Benchmark](./20260603b-research-rubrics-benchmark/notes.md)
