# Lessons from Building Claude Code: How We Use Skills

> 作者：Thariq (@trq212)，Anthropic Claude Code 团队
> 来源：X (Twitter) Article
> 原文链接：https://x.com/trq212/status/2033949937936085378
> 发布时间：2026-03-18

---

## What are Skills?

如果你对 skills 不熟悉，建议阅读 [官方文档](https://code.claude.com/docs/en/skills) 或观看 [Skilljar 课程](https://anthropic.skilljar.com/introduction-to-agent-skills)。

关于 skills 的一个常见误解是它们"只是 markdown 文件"，但最有趣的部分是：**它们不仅仅是文本文件，而是文件夹**，可以包含脚本、资源、数据等，agent 可以发现、探索和操作这些内容。

在 Claude Code 中，skills 有 [丰富的配置选项](https://code.claude.com/docs/en/skills#frontmatter-reference)，包括注册动态 hooks。最有趣的 skills 是创造性地使用这些配置选项和文件夹结构的。

## Types of Skills（技能类型）

整理完所有 skills 后，我们发现它们聚集为几个反复出现的类别。最优秀的 skill 可以完全归入其中一类；较为复杂的则跨越多个类别。

### 1. Library & API Reference（库和 API 参考）

解释如何正确使用库、CLI 或 SDK 的技能。可以是内部库或 Claude Code 有时难以处理的常见库。通常包含参考代码片段文件夹和常见问题清单。

示例：
- billing-lib — 内部计费库：边缘情况、潜在风险等
- internal-platform-cli — 内部 CLI 包装器的每个子命令及使用示例
- frontend-design — 让 Claude 在你的设计系统中表现更好

### 2. Product Verification（产品验证）

描述如何测试或验证代码是否正常工作的技能。通常与 playwright、tmux 等外部工具配合使用。

**验证技能对确保 Claude 输出的正确性非常有用。值得让工程师花一周时间来使验证技能变得出色。**

考虑让 Claude 录制输出视频以便查看测试内容，或在每个步骤上对状态实施程序化断言。

示例：
- signup-flow-driver — 在无头浏览器中运行注册 → 邮箱验证 → 新手引导，每步有断言
- checkout-verifier — 用 Stripe 测试卡驱动结账，验证发票状态
- tmux-cli-driver — 需要 TTY 的交互式 CLI 测试

### 3. Data Fetching & Analysis（数据获取与分析）

连接到数据与监控堆栈的技能。可能包含凭证获取库、仪表板 ID，以及常见数据获取工作流说明。

示例：
- funnel-query — 加入哪些事件看注册→激活→付费，及规范 user_id 表
- cohort-compare — 比较两个群体的留存/转化率，标记显著差异
- grafana — 数据源 UIDs、集群名称、问题→仪表板查找表

### 4. Business Process & Team Automation（业务流程与团队自动化）

将重复工作流自动化为一个命令的技能。通常是简单指令但可能依赖其他 skills 或 MCPs。将之前结果存储在日志文件中可帮助模型保持一致。

示例：
- standup-post — 聚合 ticket tracker、GitHub 活动和 Slack → 格式化的站会汇报
- create-\<ticket-system\>-ticket — 强制 schema（有效枚举值、必填字段）+ 创建后工作流
- weekly-recap — 合并的 PR + 关闭的 ticket + 部署 → 格式化的周报

### 5. Code Scaffolding & Templates（代码脚手架与模板）

为代码库中特定功能生成框架样板的技能。可与脚本组合使用。当脚手架有自然语言需求且无法纯靠代码覆盖时特别有用。

示例：
- new-\<framework\>-workflow — 用你的注解搭建新服务/工作流/处理器
- new-migration — 你的迁移文件模板加常见问题
- create-app — 预配置 auth、日志和部署的新内部应用

### 6. Code Quality & Review（代码质量与审查）

在组织内强制代码质量并帮助审查代码的技能。可以包含确定性脚本或工具以获得最大健壮性。可能作为 hooks 或 GitHub Action 的一部分自动运行。

示例：
- adversarial-review — 生成一个全新视角的子 agent 来批评，实施修复，迭代直到问题退化为吹毛求疵
- code-style — 强制代码风格，尤其是 Claude 默认做不好的风格
- testing-practices — 关于如何写测试和测试什么的指导

### 7. CI/CD & Deployment

帮助你在代码库中获取、推送和部署代码的技能。可能引用其他 skills 来收集数据。

示例：
- babysit-pr — 监控 PR → 重试不稳定 CI → 解决合并冲突 → 开启自动合并
- deploy-\<service\> — 构建 → 冒烟测试 → 渐进流量切换（错误率比较）→ 回归时自动回滚
- cherry-pick-prod — 隔离 worktree → cherry-pick → 冲突解决 → 使用模板的 PR

### 8. Runbooks

接收症状（Slack 线程、告警或错误签名），进行多工具调查，并生成结构化报告的技能。

示例：
- \<service\>-debugging — 将症状映射到工具→查询模式（高流量服务）
- oncall-runner — 获取告警 → 检查常见嫌疑 → 格式化发现
- log-correlator — 给定请求 ID，从所有相关系统拉取匹配日志

### 9. Infrastructure Operations（基础设施运维）

执行例行维护和运维程序的技能——部分涉及需要保护措施的破坏性操作。让工程师更容易在关键操作中遵循最佳实践。

示例：
- \<resource\>-orphans — 查找孤立 pods/volumes → 发到 Slack → 浸泡期 → 用户确认 → 级联清理
- dependency-management — 组织的依赖审批工作流
- cost-investigation — "为什么存储/出口费用飙升"，包含具体 bucket 和查询模式

---

## Tips for Making Skills（技能制作技巧）

Anthropic 最近发布了 [Skill Creator](https://claude.com/blog/improving-skill-creator-test-measure-and-refine-agent-skills) 以简化技能创建。

### Don't State the Obvious（不要陈述显而易见的事）

Claude Code 对你的代码库了解很多，Claude 对编码也了解很多。如果你发布的 skill 主要是关于知识的，**重点关注能让 Claude 跳出常规思维的信息**。

[前端设计 skill](https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md) 是一个好例子——它通过与客户迭代来改善 Claude 的设计品味，避免 Inter 字体和紫色渐变等"经典模式"。

### Build a Gotchas Section（构建"坑"章节）

任何 skill 中信号最强的内容就是 Gotchas 部分。应该从 Claude 使用你的 skill 时常见的失败点中积累。理想情况下，随着时间推移不断更新。

### Use the File System & Progressive Disclosure（利用文件系统和渐进式呈现）

Skill 是一个文件夹，不仅仅是 markdown 文件。**把整个文件系统当作上下文工程和渐进式呈现的形式**。告诉 Claude 你的 skill 里有什么文件，它会在适当时候读取。

最简单的渐进式呈现：指向其他 markdown 文件供 Claude 使用（如 `references/api.md`）。也可以在 `assets/` 中包含模板文件供复制使用。

### Avoid Railroading Claude（避免过度约束 Claude）

Claude 通常会尽量遵循你的指令，因为 Skills 高度可重用，所以要**小心不要在指令中过于具体**。给 Claude 需要的信息，但给它适应情况的灵活性。

### Think through the Setup（考虑设置流程）

某些 skill 可能需要用户提供上下文来设置。好的模式是在 skill 目录中存储一个 `config.json` 文件。如果配置未设置，agent 可以询问用户。如果想让 agent 展示结构化的多选题，可以让 Claude 使用 AskUserQuestion 工具。

### The Description Field Is For the Model（描述字段是给模型的）

当 Claude Code 启动会话时，它会构建所有可用 skill 及其描述的列表。Claude 扫描这个列表来判断"这个请求有没有对应的 skill？"**描述字段不是摘要——是触发条件。**

### Memory & Storing Data（记忆与数据存储）

有些 skill 可以通过在其中存储数据来实现记忆形式。可以是简单的追加文本日志或 JSON 文件，也可以复杂到 SQLite 数据库。

例如 standup-post skill 可能保存一个 standups.log，Claude 下次运行时读取自己的历史，知道昨天以来发生了什么变化。

**注意**：skill 目录中的数据在升级 skill 时可能被删除，应存储在稳定文件夹中。目前提供 `${CLAUDE_PLUGIN_DATA}` 作为每个插件的稳定数据目录。

### Store Scripts & Generate Code（存储脚本与生成代码）

你能给 Claude 的最强大工具之一就是代码。给 Claude 脚本和库，让它把轮次花在**组合**上——决定下一步做什么，而不是重建样板代码。

例如数据科学 skill 中可以有一组获取数据的辅助函数，Claude 可以即时生成脚本来组合这些功能做更高级的分析。

### On Demand Hooks（按需 Hooks）

Skills 可以包含仅在 skill 被调用时激活、持续到会话结束的 hooks。用于更有主见的 hooks——不想一直运行，但有时极其有用。

示例：
- `/careful` — 通过 Bash 的 PreToolUse 匹配器阻止 rm -rf、DROP TABLE、force-push、kubectl delete。只在操作生产环境时需要
- `/freeze` — 阻止不在特定目录中的任何编辑/写入。调试时有用："我想加日志但总是意外'修复'不相关的东西"

---

## Distributing Skills（分发技能）

分享 skills 有两种方式：

1. **将 skills 提交到仓库**（`./.claude/skills` 下）
2. **制作插件**，通过 Claude Code [插件市场](https://code.claude.com/docs/en/plugin-marketplaces)分发

小团队、少量仓库时，提交到仓库效果好。但每个提交的 skill 都会给模型上下文增加一点内容。**随着规模扩大，内部插件市场可以让团队自行选择安装哪些 skills。**

### Managing a Marketplace（管理市场）

没有集中的团队来决定，而是有机地寻找最有用的 skills。如果你有想让人试用的 skill，可以上传到 GitHub sandbox 文件夹并在 Slack 推广。获得关注后，可以提 PR 移入市场。

**警告**：创建坏的或冗余的 skills 很容易，所以发布前需要有某种审核方法。

### Composing Skills（组合技能）

你可能需要互相依赖的 skills。例如文件上传 skill + CSV 生成 skill。依赖管理目前未内置于市场或 skills 中，但**可以按名称引用其他 skills，模型会在已安装时调用它们**。

### Measuring Skills（衡量技能）

使用 PreToolUse hook 记录公司内的 skill 使用情况（[示例代码](https://gist.github.com/ThariqS/24defad423d701746e23dc19aace4de5)）。可以找到受欢迎的或触发不足的 skills。

---

## Conclusion

Skills 是 agent 极其强大、灵活的工具，但仍处于早期阶段。把这些当作有用技巧的合集，而非权威指南。最好的理解方式是动手实验。大多数 skill 始于几行文字和一个坑，随着 Claude 遇到新的边缘情况而不断改进。
