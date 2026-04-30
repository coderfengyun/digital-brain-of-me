# Lessons from Building Claude Code: How We Use Skills

**类型**: 叙事

---

## 完整叙事

### 背景

Thariq 是 Anthropic Claude Code 团队成员。Skills 已成为 Claude Code 中最常用的扩展点之一——灵活、易创建、便于分发。但灵活性也带来困惑：什么类型的 skills 值得做？怎么写好？何时分享？

Anthropic 内部已有数百个 skills 在活跃使用。这篇文章是他们从大规模实践中提炼的经验。

### 核心故事

文章的叙事主线是：**Skill 不是 markdown 文件，而是一个"上下文工程"的文件夹系统。**

这个认知翻转是理解全文的关键。大多数人把 skill 理解为"给 AI 的一段提示词"，但 Anthropic 内部的最佳实践表明，真正强大的 skill 是一个包含脚本、资源、数据、配置的完整文件夹，agent 可以发现、探索和操作其中的一切。

围绕这个核心，文章展开了三层结构：

**第一层：9 种技能分类法。** Anthropic 把内部数百个 skills 归纳为 9 类：

| 类别 | 核心作用 | 关键特征 |
|------|---------|---------|
| Library & API Reference | 教 Claude 正确使用库/CLI | 代码片段 + 坑清单 |
| Product Verification | 验证 Claude 输出正确性 | 配合 playwright/tmux |
| Data Fetching & Analysis | 连接数据和监控 | 凭证 + 仪表板 ID |
| Business Process Automation | 自动化重复工作流 | 简单指令 + MCP 依赖 |
| Code Scaffolding & Templates | 生成框架样板 | 脚本可组合 |
| Code Quality & Review | 强制代码质量 | 可作为 hooks/CI 运行 |
| CI/CD & Deployment | 获取/推送/部署代码 | 引用其他 skills |
| Runbooks | 症状→调查→报告 | 多工具协同 |
| Infrastructure Operations | 例行运维 | 需要安全保护措施 |

**最优秀的 skill 完全归入一类；混乱的 skill 跨越多类。** 这个分类法本身就是组织审视自己 skill 覆盖率的工具。

**第二层：8 条制作技巧。** 这是全文信号密度最高的部分：

1. **不要陈述显而易见的事** — Claude 已经知道很多，重点放在让它跳出常规思维的信息上
2. **构建 Gotchas 章节** — 任何 skill 中信号最强的内容，从失败点中积累
3. **利用文件系统做渐进式呈现** — 整个文件夹结构就是上下文工程，告诉 Claude 有什么文件，它会在需要时读取
4. **避免过度约束** — 给信息但给灵活性，因为 skills 是高度可重用的
5. **考虑设置流程** — 用 config.json 存储配置，未设置时让 agent 询问用户
6. **描述字段是给模型的** — 不是摘要，是触发条件
7. **记忆与数据存储** — 用日志文件/JSON/SQLite 让 skill 有记忆，注意用稳定目录 `${CLAUDE_PLUGIN_DATA}`
8. **存储脚本让 Claude 组合** — 给 Claude 辅助函数库，让它花时间在组合而非重建样板

**第三层：分发与管理。** 两种分发方式（仓库提交 vs 插件市场），以及有机的审核流程——先在 sandbox 推广，获得关注后提 PR 进市场。用 PreToolUse hook 埋点衡量 skill 使用。

### 关键转折

**转折一："Skill 是文件夹，不是文件"这个认知改变了一切。**

一旦你把 skill 理解为文件夹，你就可以：在里面放参考代码、放脚本、放模板、放数据、放配置。Claude 会像探索一个小型代码库一样探索你的 skill。这是从"提示词工程"到"上下文工程"的范式跳跃。

**转折二：On Demand Hooks 创造了"模式切换"的可能。**

`/careful` 阻止危险操作，`/freeze` 限制编辑范围——这些不是永远开启的，而是按需激活。这意味着 skills 不仅能增加能力，还能增加约束。这是一种全新的安全模式。

**转折三：验证技能值得花一整周来做。**

"值得让工程师花一周时间来使验证技能变得出色"——这暗示 Anthropic 在内部已经看到，AI agent 的产出质量瓶颈不在生成速度，而在验证能力。投资验证 skill 的 ROI 远超投资生成 skill。

### 结果与意义

这篇文章本质上是 Anthropic 内部 "Skills as Infrastructure" 实践的首次系统性公开。它暗示了几个趋势：

1. **Skills 正在从"个人提示词"进化为"组织知识基建"** — 有分类法、有市场、有衡量体系
2. **Agent 的能力边界由 skills 的质量决定** — 不是模型能力不够，而是给它的上下文和工具不够好
3. **渐进式呈现是 AI 上下文管理的核心设计原则** — 不要一次性灌输所有信息，而是让 agent 按需探索

---

## 关键洞察

- **Skill 是文件夹，不是 markdown 文件**：这是从"提示词工程"到"上下文工程"的范式跳跃，整个文件系统可以作为渐进式呈现的载体
- **9 种分类法是组织 skill 覆盖率的审计工具**：最好的 skill 归入一类，跨越多类的 skill 往往是混乱的
- **Gotchas 章节是任何 skill 中 ROI 最高的内容**：应从 Claude 的实际失败点中积累，不断更新
- **验证 skill 的投资回报远超生成 skill**：AI 产出的瓶颈不在生成速度，而在验证能力
- **描述字段是触发条件，不是摘要**：Claude 用它判断是否调用，所以要写"什么时候触发"而非"这个 skill 做什么"
- **On Demand Hooks 实现了"模式切换"安全模式**：/careful、/freeze 等按需约束是 skill 能力的另一面
- **组合优于重建**：给 Claude 脚本库让它组合，而不是让它每次从零开始写——这是 skill 设计的核心效率原则
- **有机分发 + 数据驱动衡量**：sandbox → 关注 → 市场的路径，配合 PreToolUse hook 埋点追踪使用率
- **`${CLAUDE_PLUGIN_DATA}` 是 skill 持久化的官方方案**：skill 目录中的数据升级时会丢失，必须用稳定目录

---

## 与我的关联

这篇文章直接相关于我正在使用的 digital-brain skill。从中可以借鉴：
- 用 Gotchas 章节记录 Claude 在使用 digital-brain skill 时的常见错误
- 利用文件夹的渐进式呈现结构，而不是把所有指令塞进一个 markdown
- 考虑为 digital-brain skill 添加 config.json 做初始化设置

### 个人阅读心得 (2026-03-19)

1. **Skill.md 之外的文件缺乏约束**：Skill.md 本身有 description 的约束、正文长度的约束，但 Skill 文件夹内的其他文件没有明确约束。估计其他文件内的要求遵循性一般，这里需要摸索 Skill 中其他文件的最佳实践。

2. **Config.json 和 Gotchas 非常好**：这两个是 skill 中最有实操价值的模式。config.json 解决了初始化和个性化配置问题，Gotchas 解决了从失败中积累经验的问题。

3. **数据存储的核心不是文件格式，而是查询能力**：对于 Skill 内部用来做数据存储的文件或 SQLite，文件格式并不重要，最重要的是能够更聚焦地查询和搜索。比如 JSONL 相比 SQLite 的好处是，它可以在整个 JSONL 里全文检索，而不需要指定列名。如果给 JSONL 配一组某个 Skill 专用的方法脚本，效果将会更好——这与文章中"Store Scripts & Generate Code"的建议高度一致。

4. **建立 Skill Market 是不错的选择**：官方文档已提供插件市场方案 (https://code.claude.com/docs/en/plugin-marketplaces)，可以作为团队或社区分发 skills 的基础设施。

5. **组合使用 Skill 的入口模式**：可以考虑有一个入口 Skill 来串联其他的功能性 Skill。这与文章中"Composing Skills"部分的思路一致——通过名称引用其他 skills，模型会自动调用已安装的 skills。目前 digital-brain 的 Skill.md 本身就扮演了这个入口角色。
