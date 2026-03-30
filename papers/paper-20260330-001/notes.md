# 一个从执行到记忆的完整 Agent Harness: gstack + Compound Engineering

**类型**: 方法

---

## 📖 核心叙事 (Narrative)

### 一句话概括
> Agent 工作流不仅需要 plan-execute-review 的完整流程，更需要「知识积累」机制——gstack 负责决策和测试，Compound Engineering 负责执行、审查和记忆，二者组合构成完整的 harness 架构。

### 叙事结构

```
问题: Agent 每次 session 结束后，调试经验和项目知识散落在各个对话里，下次再踩同样的坑
↓
观察: Anthropic 提出了 harness 架构（Planner → Coder → Evaluator → 跨 session 桥接），
      但其 progress file 只是线性备忘录，只服务相邻两个 session
↓
假设: 如果把跨 session 桥接从「备忘录」升级为「可搜索的知识库」，agent 就能实现指数级积累
↓
方法: 用 Anthropic harness 框架评估三个 Claude Code skills 组合——
      gstack（决策+QA）、Superpowers（全流程但无记忆）、CE（全流程+知识积累）
↓
验证: CE 的 /ce:compound 并行 spawn 3 个 agent 提取经验、写入 docs/solutions/，
      未来所有 /ce:plan 的 learnings-researcher 都能搜到历史知识
↓
结论: gstack + CE 组合覆盖 harness 全部角色（决策、规划、执行、审查、知识），
      Superpowers 被 CE 完全替代，compound 是关键差异化维度
```

---

## 📊 数据证据层 (Evidence)

| 论点 | 创新点 | 支撑数据 | 数据来源 | 说服力评估 |
|------|--------|----------|----------|------------|
| Anthropic harness 架构有效 | 4 角色分离：Planner、Coder、Evaluator、跨 session 桥接 | **例子**: Anthropic 用此架构让 agent 自主开发完整 claude.ai 克隆，200+ 可验证 feature；generator-evaluator 分离"效果显著提升" | Anthropic 工程博客 (2025.11 + 2026.03) | ⭐⭐⭐ 强——有 Anthropic 自身实践背书，但未给出对比数据 |
| gstack 做对了 Planner + Evaluator | /plan-ceo-review（产品视角）+ /plan-eng-review（架构视角）+ /qa（浏览器实测） | **例子**: /qa 打开浏览器跑 staging URL，像真实用户一样测试，对应 Anthropic 所说 "dramatically improved performance" | gstack 源码 + Anthropic 博客引用 | ⭐⭐ 中——gstack 功能描述准确，但"dramatically improved"是引用 Anthropic 而非 gstack 自身数据 |
| Superpowers 流程有但深度不够 | 对比 CE 在 Plan、Review、知识积累三个维度的差距 | **例子**: Plan 方面——Superpowers 在当前 context 直接写 plan，CE 并行 spawn research agent 搜历史经验、扫 codebase pattern、读 git history；Review 方面——Superpowers 2 个 reviewer（spec+quality），CE spawn 6-15 个专项 reviewer（correctness, security, performance, testing, maintainability, adversarial 等） | 作者使用经验 + CE 源码分析 | ⭐⭐ 中——功能对比清晰，但缺少 "更深" 带来的实际效果量化 |
| CE /ce:compound 解决知识积累 | 从线性备忘录→可搜索知识库；3 agent 并行提取+去重 | **例子**: 修了一个 edge runtime 兼容性 bug → compound 记录 → 三周后类似 runtime 问题 → plan 阶段 agent 自动翻出历史解法；文档结构：Problem → What Didn't Work → Solution → Prevention，带 YAML frontmatter 按 category 分目录 | CE 源码分析 + 作者使用经验 | ⭐⭐ 中——架构设计合理，举例有说服力，但无规模化使用数据 |
| compound 不应自动化 | 信噪比考量：低价值 session compound 会污染知识库 | **例子**: 改 typo、调 CSS、跑 migration 不产生新知识，自动 compound 会降低 learnings-researcher 搜索质量；作者提出 "compound janitor" 方案——每天 end of day 扫 git diff 和 conversation，筛选有价值的 session 批量 compound | 作者推理 + CE 源码（/lfg 不含 compound） | ⭐⭐ 中——逻辑自洽，janitor 方案有创意但尚未实现 |

---

## 🤔 批判性思考 (Critical Thinking)

| 问题 | 分析 |
|------|------|
| 核心假设及失效场景 | **假设**: 知识积累（compound）是 agent harness 的关键缺失环节，补上后 agent 能实现 "self-improving"。<br>**失效场景**: 1) 项目规模小、重复问题少时，compound 的投入产出比可能不高；2) docs/solutions/ 知识库随时间膨胀，搜索质量可能退化（作者自己也暗示了这一点）；3) LLM 的 context window 持续增长，跨 session 桥接的需求可能被根本性地减弱 |
| 关键局限 | - 全文基于作者个人使用体验，没有 A/B 测试或多人对比数据<br>- "更深"的评价维度（6-15 reviewer vs 2 reviewer）隐含一个假设：更多 reviewer = 更好，但未验证增加的 reviewer 是否真的捕获了更多 bug<br>- gstack + CE 的组合隐含工具绑定到 Claude Code 生态，迁移成本和可复制性未讨论<br>- Superpowers 的跨工具兼容优势被一笔带过，但对非 Claude Code 用户这可能是决定性因素 |
| 实验充分性 | **缺失验证**: 1) 没有 "有 compound vs 无 compound" 在同一项目上的对比数据；2) 没有 compound 知识库随时间增长后的搜索精度数据；3) 没有 CE 和 Superpowers 在相同任务上的 completion rate / bug rate 对比；4) "compound janitor" 只是设想，未实现 |
