# Digital Brain - Personal Knowledge Management System

A structured, AI-assisted knowledge management system for managing your personal brand, content creation, learning, relationships, and productivity.

Inspired by [Agent Skills for Context Engineering](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering/tree/main/examples/digital-brain-skill).

## Structure

```
digital-brain-of-me/
├── sources/          # 外部输入统一管理（source → output）
│   ├── sources.jsonl # 注册表（paper + podcast 元数据）
│   └── *.pdf/*.docx  # 本地文件类输入
├── identity/          # Your personal brand and voice
│   ├── brand/        # Profile, values, expertise
│   └── voice/        # Writing style and principles
├── content/          # Content creation pipeline
│   ├── ideas/        # Content ideas (JSONL)
│   ├── drafts/       # Work in progress (Markdown)
│   └── published/    # Published content log (JSONL)
├── knowledge/        # Learning and research
│   ├── bookmarks/    # Saved links (JSONL)
│   ├── ai/           # AI, agents, context engineering, developer tools
│   ├── organizations/# Organization design, decision-making, collaboration
│   ├── research/     # Temporary research incubation
│   └── learning/     # Courses, books, skills (YAML)
├── weekly-review/    # 周记&月结归档（投资/学习/工作/生活回顾）
├── investment/       # Investment trade journal and P&L analysis
│   ├── 投资日志整理/ # Trade records, scripts, schema
│   └── 作者/文章主题/ # Investment research by author/source
├── operations/       # Goals and productivity
│   ├── goals/        # Yearly/quarterly/monthly goals (YAML)
│   ├── tasks/        # Action items (JSONL)
│   ├── meetings/     # Meeting notes (JSONL)
│   └── metrics/      # Weekly metrics (JSONL)
├── scripts/          # Automation tools
└── .codex/skills/module-toolkit/   # Codex module creation skill (scripts + guides)
```

## Quick Start

1. **Set up identity**: Edit `identity/brand/profile.yaml` and `identity/voice/style.md`
2. **Start capturing**: Add ideas, bookmarks, contacts via JSONL append or scripts
3. **Review past journals**: Browse `weekly-review/` for historical weekly reviews and reflections
4. **Use with Claude Code**: Say things like "add a content idea about X" or "周记"

## Tools

### Markdown Annotator

Use a local browser UI to annotate Markdown files visually:

```bash
npm run annotate:md
```

The tool renders `.md` files and saves comments next to the source file as `*.annotations.json`. See [tools/md-annotator/README.md](tools/md-annotator/README.md).

详细的数据格式、脚本列表和使用指南见 [CLAUDE.md](CLAUDE.md)。
各模块的详细说明见对应目录下的大写 `.md` 文件（如 `sources/SOURCES.md`、`knowledge/KNOWLEDGE.md`、`investment/INVESTMENT.md`、`weekly-review/WEEKLY-REVIEW.md`）。

所有外部输入（论文、文章、研报、播客等）统一通过 [sources/SOURCES.md](sources/SOURCES.md) 管理，遵循 **source → processing → domain output** 模型。`paper` 和 `podcast` 是处理类型，产出物归入对应领域目录。

## Extending the System

See [MODULE_CREATION_GUIDE.md](.codex/skills/module-toolkit/references/MODULE_CREATION_GUIDE.md).

```bash
python .codex/skills/module-toolkit/scripts/check_module_integration.py <module_name> [keyword]
```

## Learn More

- [Original Digital Brain Skill](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering/tree/main/examples/digital-brain-skill)
- [Module Creation Guide](.codex/skills/module-toolkit/references/MODULE_CREATION_GUIDE.md)

## License

MIT License - Feel free to adapt this system for your own needs.

---

**Built with**: Claude Code, Python, Markdown, JSONL, YAML
