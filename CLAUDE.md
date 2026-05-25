# Digital Brain

本文件以项目文件夹结构为核心，描述每个目录的职责和入口。

## 项目结构

```
digital-brain-of-me/
├── identity/          用户身份与表达风格
├── content/           内容创作（想法、草稿、成品）
├── knowledge/         知识库（书签、学习笔记、研究）
├── investment/        投资研究与交易记录
├── sources/           外部来源注册表（论文、播客、文章）
├── operations/        任务、目标、会议、指标
├── weekly-review/     周记
├── labs/              进行中的探索性项目
├── scripts/           通用脚本工具
├── work-standard/     工作标准与示例
├── env/               环境与依赖管理
├── .claude/skills/    复杂工作流的指令和脚本
└── *.md               设计文档与方法论
```

## 各目录说明

| 目录 | 职责 | 入口文件 |
|------|------|---------|
| `identity/` | 用户身份定义与表达风格 | `identity/voice/style.md`（内容创作前必读） |
| `content/` | 创意 → 草稿 → 发布的完整内容流程 | `content/CONTENT.md` |
| `knowledge/` | 书签、学习笔记、AI/组织研究等知识沉淀 | `knowledge/KNOWLEDGE.md` |
| `investment/` | 投资研究、交易日志、盈亏计算 | `investment/INVESTMENT.md`（复杂工作流由 `.claude/skills/investment/` 驱动） |
| `sources/` | 外部来源（论文、播客、文章）注册表 | `sources/SOURCES.md`（注册后路由到对应 skill） |
| `operations/` | 任务管理、目标跟踪、会议记录、指标 | `operations/OPERATIONS.md` |
| `weekly-review/` | 周记 | `weekly-review/WEEKLY-REVIEW.md`（文件命名：`YYYY-MM-DD~MM-DD.md`） |
| `labs/` | 进行中的探索性技术实验 | 每个子目录含 README |
| `scripts/` | 通用脚本工具 | 用 `uv run` 执行 |
| `work-standard/` | 工作标准、对话示例、参考文章 | 直接读取目录内文件 |
| `env/` | 环境与依赖管理（setup.sh、依赖分层、日常操作） | `env/ENV.md` |

### 根目录文档

| 文件 | 用途 |
|------|------|
| `the-file-system-is-the-new-database.md` | 系统设计哲学（context engineering、progressive disclosure） |
| `multi-component-design.md` | 多组件协作设计方法论（涉及多组件集成时读此文档） |

---

## 约束

以下规则始终生效。

### 语言
- 用户用中文交流，用中文回复

### 权限
- 当用户提供 web URL 或需要将网页内容转成 Markdown，统一使用 Chrome MCP（navigate_page + take_snapshot），不使用 WebFetch 或 agent-browser

### 格式
- 流程图只保存 Mermaid 源代码（.mmd 文件），不保存图片
- JSONL 文件：一行一个 JSON 对象，只追加不删除
- 唯一 ID 格式：`type-XXX`（如 `idea-001`, `paper-YYYYMMDD-XXX`）
- 跨模块保持一致的 tagging

### 操作纪律
- 写之前先读（不覆盖已有数据）
- 生成内容前先读 `identity/voice/style.md`
- 移动/重命名文件前 `grep -r "filename"` 搜索并更新所有引用
- 操作失败时优先修复相关模块的设计/指令

