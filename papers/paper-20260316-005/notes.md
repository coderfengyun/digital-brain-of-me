# Claude Cowork: The Ultimate Guide for PMs

**类型**: 综述

---

## 领域全景

### 一句话概括
> Claude Desktop 三种模式（Chat / Cowork / Code）的定位差异，以及 Cowork 作为非开发者的日常自主 Agent 如何配置和使用

### 发展脉络

```
Claude Chat: 对话式交互，输出 artifact
↓
Claude Code: 开发者终端 Agent，需要 git/tmux/CLI
↓
Claude Cowork: 桌面自主 Agent，沙盒 VM + 可视化界面 + 真实文件输出
↓
三者共享: 同一模型、同一 skill 格式、同一 connector 类型
```

---

## 方法分类

| 类别 | 代表能力 | 核心思路 | 优势 | 局限 |
|------|---------|----------|------|------|
| Chat | 对话、artifact | 单轮/多轮文本交互 | 简单直接 | 无任务分解、无真实文件 |
| Cowork | 子 Agent 并行、任务分解、真实文件 | 自主桌面 Agent + 沙盒 VM | 可视化、非开发者友好、输出 .docx/.pptx/.xlsx/.pdf | 沙盒内有限、调度任务不可靠 |
| Code | git worktree、终端操作、代码生成 | 开发者 CLI Agent | 最灵活、能力最强 | 需要终端技能 |

---

## 证据表

| 论点 | 创新点 | 支撑数据 | 数据来源 | 说服力评估 |
|------|--------|----------|----------|-----------|
| Cowork 是非开发者的最佳日常工具 | Chat vs Cowork vs Code 三者定位区分 | **例子**: 作者作为前工程师仍选 Cowork 处理邮件/合同/发票/文件管理 | 作者个人经验 | 中——个人偏好，但场景具体 |
| Skill 按需加载保持上下文干净 | ~100 tokens 描述决定是否加载完整指令 | progressive disclosure 机制 | Anthropic 设计 | 高——与 AGENTS.md 目录式设计一致 |
| Cowork 引发 $2850 亿市值下跌 | AI Agent 进入应用层的标志性事件 | 2026 年初法律/金融 AI 工具发布后 legacy software 股价暴跌 | 公开市场数据 | 高——事实性陈述 |
| Desktop Commander 是最高 ROI 操作 | < 1 分钟安装，Chat/Cowork/Code Tab 均可访问全系统 | **例子**: Claude 自动安装 MCP server、重组桌面文件 | 作者演示 | 高——操作简单且效果显著 |
| Scheduled Tasks 不可靠 | 诚实评价 | 作者测试后推荐用 n8n 或 MCP 替代 | 作者实测 | 高——作为作者的诚实评价可信 |

---

## 批判性思考

**1. Skill 系统与我们 digital-brain 的 skill 设计高度一致**

文章描述的 skill 机制——按需加载、~100 tokens 描述、`/` 触发——和我们在 CLAUDE.md + Skills 目录中的设计原则完全一致。这验证了 progressive disclosure 是 Agent 系统的通用模式：
- Anthropic 的 AGENTS.md 目录设计
- OpenAI Harness Engineering 的 docs/ 知识库
- 我们的 Skills .md 文件

**2. 三种模式的真正区别不是能力，是交互范式**

作者反复强调"同一模型、同一 skill 格式、同一 connector 类型"。差异纯粹在于：
- Chat = 对话范式
- Cowork = 任务范式（分解 → 并行 → 交付文件）
- Code = 开发范式（终端 + git + CLI）

这意味着**选择哪种模式取决于你的工作流，而非 AI 能力**。

**3. Memory 部分直接可借鉴**

作者给出的结构化记忆方案几乎就是我们 auto-memory 系统的设计：
- memory.md 作为索引（= 我们的 MEMORY.md）
- domain/{topic}.md 按主题分文件（= 我们的独立 topic 文件）
- 规则：立即写入、不等会话结束、date/what/why 格式

**4. MCP 生态的碎片化问题**

文章列出三种 MCP 连接方式（Remote / Extension / Custom JSON），且配置不跨工具共享（Desktop vs CLI）。这说明 MCP 生态仍在早期整合阶段，开发者需要管理多个配置入口。

**5. 未回答的问题**

- Cowork 的 VM 资源限制是什么？能跑多大的脚本？
- 子 Agent 并行的上限？是否有 token 或并发限制？
- Plugin 跨 Cowork/Code Tab 隔离的设计原因？
- 企业环境中的安全审计能力如何？

---

## 关键洞察

- **Chat = 对话，Cowork = 工作流，Code = 开发**: 三者能力相同，区别在于交互范式和面向的用户群
- **Cowork 的核心差异化: 任务分解 + 子 Agent 并行 + 真实文件输出**: 这是从"聊天工具"到"工作工具"的关键跨越
- **Skill 的 progressive disclosure 是通用模式**: ~100 tokens 描述 → 按需加载完整指令，与 AGENTS.md 目录、docs/ 知识库同一原则
- **Desktop Commander 是 Claude Desktop 的"root 权限"**: < 1 分钟安装，让 Chat/Cowork/Code Tab 均可操作全系统文件和安装 MCP
- **结构化 memory 是跨会话能力的关键**: memory.md 索引 + 主题分文件 + 立即写入规则，几乎零 token 成本
- **MCP 配置碎片化是当前痛点**: 三种连接方式、Desktop vs CLI 配置不互通，生态仍在整合中
- **Scheduled Tasks 不可靠**: 作者诚实推荐 n8n 或 MCP 替代方案
- **Plugin 生态已爆发**: 6+ 个 skill/plugin 来源，868+ 社区 skills，PM 专用 skills.sh
