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
│   ├── papers/       # Paper reading notes
│   ├── research/     # Deep research notes (Markdown)
│   └── learning/     # Courses, books, skills (YAML)
├── investment/       # Investment trade journal and P&L analysis
│   ├── 投资日志整理/ # Trade records, scripts, schema
│   └── *.md          # Investment research notes
├── operations/       # Goals and productivity
│   ├── goals/        # Yearly/quarterly/monthly goals (YAML)
│   ├── tasks/        # Action items (JSONL)
│   ├── meetings/     # Meeting notes (JSONL)
│   └── metrics/      # Weekly metrics (JSONL)
├── scripts/          # Automation tools
└── .claude/skills/module-toolkit/  # Module creation skill (scripts + guides)
```

## Quick Start

1. **Set up identity**: Edit `identity/brand/profile.yaml` and `identity/voice/style.md`
2. **Start capturing**: Add ideas, bookmarks, contacts via JSONL append or scripts
3. **Use with Claude Code**: Say things like "add a content idea about X" or "weekly review"

详细的数据格式、脚本列表和使用指南见 [CLAUDE.md](CLAUDE.md)。
各模块的详细说明见对应目录下的大写 `.md` 文件（如 `sources/SOURCES.md`、`knowledge/papers/PAPERS.md`、`investment/INVESTMENT.md`）。

所有外部输入（论文等）统一通过 [sources/SOURCES.md](sources/SOURCES.md) 管理，遵循 **source → processing → output** 模型。播客转录由独立的 `podcast-transcribe` skill 处理，产出物归入对应内容目录。

## Extending the System

See [MODULE_CREATION_GUIDE.md](.claude/skills/module-toolkit/references/MODULE_CREATION_GUIDE.md).

```bash
python .claude/skills/module-toolkit/scripts/check_module_integration.py <module_name> [keyword]
```

## Learn More

- [Original Digital Brain Skill](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering/tree/main/examples/digital-brain-skill)
- [Module Creation Guide](.claude/skills/module-toolkit/references/MODULE_CREATION_GUIDE.md)

## License

MIT License - Feel free to adapt this system for your own needs.

---

**Built with**: Claude Code, Python, Markdown, JSONL, YAML
