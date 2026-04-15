# Harness Engineering: Building a Product with 0 Lines of Manually-Written Code

**类型**: 方法

---

## 叙事线

```
问题: 当工程师不再写代码，如何让 Agent 可靠地构建和维护复杂软件？
↓
约束: 5个月内用 Codex 从空仓库构建内部产品，0 行手写代码
↓
发现: 早期瓶颈不是 AI 能力不足，而是环境欠规格化（underspecified）
↓
方法: 人设计环境/意图/反馈循环，Agent 执行全部代码
↓
核心机制:
  - AGENTS.md 作为目录而非百科全书（progressive disclosure）
  - 仓库知识作为唯一真相源（repo = system of record）
  - 严格架构约束机械化执行（linters + structural tests）
  - "垃圾回收"机制持续清理 Agent 产生的技术债
↓
结果: ~100万行代码、~1500个PR、3人→7人团队、每人每天3.5个PR
↓
结论: 纪律仍然必需，但体现在 scaffolding 而非代码本身
```

## 证据表

| 论点 | 创新点 | 支撑数据 | 数据来源 | 说服力评估 |
|------|--------|----------|----------|-----------|
| 0行手写代码可以交付产品 | 极端约束验证可行性 | 5个月、~100万行代码、内部日活用户 | OpenAI 内部项目 | 高——真实产品、真实用户 |
| 人均吞吐量随团队增长不降反升 | 反直觉——Brooks's Law 失效 | 3人→7人，3.5 PR/人/天且上升 | 同上 | 高——有具体数字 |
| 大 AGENTS.md 失败 | 四个具体失败模式 | 上下文稀缺、过多指导=无指导、即时腐烂、难以验证 | 实践总结 | 高——每个失败模式都有清晰解释 |
| Agent 可自主完成端到端 feature | 从复现bug→录视频→修复→PR→merge | 11步完整流程 | 同上 | 高——但作者明确说依赖特定仓库工具链 |
| "垃圾回收"取代人工清理 | 从每周五20%时间人工清理→自动化 golden principles 扫描 | 背景 Codex 任务定期扫描、自动开 refactoring PR | 同上 | 中高——理念清晰但缺乏量化对比 |
| 10x 效率提升 | 与手写代码对比 | 估算 1/10 时间 | 作者估算 | 中——自我估算，无对照组 |

## 批判性思考

**1. 这篇文章是 Ralph 方法论的企业级实现**

文中明确提到 "Ralph Wiggum Loop"——他们用 Codex 循环提交PR、自审、回应反馈直到所有 agent reviewer 满意。但比 Ralph 走得更远：不只是单 Agent 循环，而是 Agent-to-Agent review 替代人工 review。这是 Huntley 分级中 Level 8-9 的实际实现。

**2. "环境即代码"是核心方法论**

最深刻的洞察不是"AI写代码"，而是：**工程师的工作从写代码变成设计 Agent 可读的环境**。这包括：
- 知识结构（docs/ 目录 = specs）
- 架构约束（linters = backpressure）
- 可观测性（logs/metrics 暴露给 Agent = 扩展 Agent 感知能力）
- 应用可驱动性（worktree 隔离 + CDP = Agent 可以自己 QA）

**3. 与 Ralph 的关键差异**

| 维度 | Ralph | Harness Engineering |
|------|-------|-------------------|
| 规模 | 单人 + 单 Agent | 7人团队 + 多 Agent 并行 |
| 审查 | 人审查 | Agent-to-Agent 审查 |
| 知识管理 | PROMPT.md + specs 文件 | 结构化 docs/ 目录 + AGENTS.md 作为目录 |
| 技术债 | git reset --hard 重来 | "垃圾回收"Agent 持续清理 |
| 验证 | 类型系统 + 测试 | 自定义 linter + 结构测试 + Agent 驱动 QA |
| 成熟度 | 个人实践 | 企业级工程实践 |

**4. 与 Claude Code 设计的对应关系**

| Harness Engineering | Claude Code |
|--------------------|------------|
| AGENTS.md（目录） | CLAUDE.md |
| docs/ 知识库 | Skills (.md 文件) |
| execution plans | TodoWrite / Task 系统 |
| custom linters（error message = remediation） | 背压机制（类型检查、测试） |
| worktree 隔离 | Agent subagent isolation |
| "doc-gardening" agent | 尚无对应 |
| golden principles | 尚无对应（用户自定义） |

**5. 未回答的问题**

- 这个内部产品是什么？复杂度如何？（文章刻意模糊）
- 100万行代码中有多少是测试/文档/配置？实际业务逻辑占比？
- "no manually-written code" 是否包括 prompt 本身？prompt 的编写难道不是一种"代码"？
- 长期架构一致性如何？作者自己也承认不知道

---

## 关键洞察

- **"给 Agent 一张地图，而非千页手册"**: AGENTS.md 应该是目录（~100行），不是百科全书。Progressive disclosure 让 Agent 按需深入
- **仓库即唯一真相源**: Slack 讨论、Google Docs、人脑中的知识对 Agent 不存在。一切必须沉淀到 repo 中的版本化文档
- **环境欠规格化是真正瓶颈**: 早期慢不是因为 AI 能力不足，而是环境（工具、抽象、结构）不够让 Agent 理解和执行
- **"Agent 挣扎 = 环境缺陷"信号**: 当 Agent 失败时，不是"重试"，而是问"缺什么能力/护栏/文档"，然后让 Agent 自己写修复
- **约束是速度的前提**: 严格的架构分层（Types→Config→Repo→Service→Runtime→UI）+ 机械化执行，是 Agent 高速产出不腐化的关键
- **垃圾回收取代人工清理**: 将"品味"编码为 golden principles，由后台 Agent 持续扫描和修复，而非人工每周花20%时间清理
- **吞吐量改变合并哲学**: 高吞吐环境中，等待比修正更贵；最小化阻塞合并门禁，用后续修复替代事前阻塞
- **明确引用 Ralph Loop**: OpenAI 内部实践直接引用了 Huntley 的 Ralph Wiggum Loop，验证了该模式的影响力
- **"boring" 技术更适合 Agent**: 可组合、API 稳定、训练集中充分表示的技术更容易被 Agent 建模
- **与你的课程生产 Agent 的关系**: 你的 Skills 目录 = 他们的 docs/ 知识库；你的专家反馈循环 = 他们的 Agent-to-Agent review；你的"更远一步"（改进生产系统本身）= 他们的 doc-gardening agent + golden principles 垃圾回收