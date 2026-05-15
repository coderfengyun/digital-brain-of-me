# Testing Agent Skills Systematically with Evals

**类型**: 方法
**来源**: [OpenAI Developers Blog](https://developers.openai.com/blog/eval-skills)
**作者**: Dominik Kundel, Gabriel Chua
**日期**: 2026-01-22

---

## 全局地图

### 一句话摘要
> 用 eval（prompt → 捕获运行 → 检查 → 评分）替代"感觉更好了"的直觉，将 agent skill 的迭代变成可测量、可回归、可持续改进的工程流程。

### 段落分类

| 章节/段落 | 分类 | 一句话说明 |
|-----------|------|-----------|
| 开头：skill 迭代的困境 | [连接] | 背景：改了 skill 不知道是变好还是只是变了 |
| 1. Define success | [核心] | 在写 skill 之前定义可测量的成功标准（四类目标） |
| 2. Create the skill | [支撑] | 示例 skill：setup-demo-app 的具体结构 |
| 3. Manually trigger | [核心] | 手动触发暴露隐含假设（触发/环境/执行三类假设） |
| 4. Small prompt set | [核心] | 10-20 个 prompt 的 CSV 覆盖四类触发场景 |
| 5. Deterministic graders | [核心] | 用 `codex exec --json` 捕获 JSONL trace，写确定性检查 |
| 6. Rubric-based grading | [核心] | 用 `--output-schema` 做模型辅助的定性评估 |
| 7. Extending evals | [支撑] | 成熟后扩展：命令计数、token 预算、构建检查、运行时烟雾测试 |
| 8. Key takeaways | [连接] | 总结五条要点 |

### 结构地图

```
问题: 迭代 agent skill 时无法区分"变好了"还是"变了"
↓
方法: 用 eval 流程替代直觉判断
├→ Step 1: 定义成功标准（outcome/process/style/efficiency 四类）
├→ Step 2: 创建 skill（name/description 是触发的关键信号）
├→ Step 3: 手动触发暴露隐含假设（触发/环境/执行）
├→ Step 4: 小型 prompt 集（10-20 个，显式/隐式/上下文/负控制）
├→ Step 5: 确定性 grader（codex exec --json → JSONL trace → 规则检查）
└→ Step 6: 定性 grader（codex exec --output-schema → 结构化评分）
↓
扩展: 命令计数/token 预算/构建检查/运行时烟雾测试/仓库清洁度/权限回归
↓
核心循环: 每次手动修复 → 变成一个新的 eval case → skill 持续改进
```

---

## 核心叙事

### 从"vibes"到"proof"的范式转换

文章的核心主张是：**skill 本质上是 prompt，应该用评估 prompt 的方式来评估 skill**。eval 的定义被精确表述为：

> prompt → captured run (trace + artifacts) → small set of checks → score you can compare over time

### 四类成功标准

在写 skill 之前先定义"成功"：
- **Outcome goals** — 任务完成了吗？应用能运行吗？
- **Process goals** — 智能体调用了 skill 并遵循了预期步骤吗？
- **Style goals** — 输出遵循了你要求的约定吗？
- **Efficiency goals** — 没有 thrashing（不必要的命令或过度 token 消耗）？

### 三类隐含假设

手动触发 skill 时要寻找的三类隐含假设：
- **触发假设** — "set up a quick React demo" 应该触发但没触发；"add Tailwind styling" 不该触发却触发了
- **环境假设** — 假设在空目录运行，假设 npm 可用且被偏好
- **执行假设** — 跳过 `npm install`（假设依赖已装），在 Vite 项目创建前就配置 Tailwind

### 四类 prompt 测试用例

10-20 个 prompt 的 CSV，覆盖：
1. **显式调用**（test-01）— 直接 `$setup-demo-app`，验证直接触发不被打破
2. **隐式调用**（test-02）— 描述 skill 的目标场景但不提名字，测试 name/description 信号强度
3. **上下文调用**（test-03）— 带领域噪声的提示，测试在真实场景中的鲁棒性
4. **负控制**（test-04）— 不应触发的场景，捕获 false positive

### 两层 grading 架构

**Layer 1: 确定性检查**
- 用 `codex exec --json` 输出 JSONL 结构化事件流
- 检查 `command_execution` 事件：是否运行了 `npm install`？
- 检查文件系统：`package.json` 是否存在？
- 优势：**确定性、可调试** — 打开 JSONL 就能看到每步发生了什么

**Layer 2: 模型辅助的 rubric 评分**
- 用 `codex exec --output-schema` 约束输出为 JSON Schema
- 第二次 codex exec **只读检查**已生成的仓库
- Schema 包含 `overall_pass`、`score`(0-100)、per-check results
- 解决确定性检查无法覆盖的定性需求（组件结构、样式约定、Tailwind 配置方式）

### 核心循环

> Every manual fix is a signal. Turn it into a test so the skill keeps getting it right.

每次手动修复（补 `npm install`、改 Tailwind 配置、调触发描述）→ 加入 CSV 作为新 eval case → skill 持续进化。

---

## 数据证据层

| 论点 | 创新点 | 支撑数据 | 数据来源 | 说服力评估 |
|------|--------|----------|----------|------------|
| Skill 应该像 prompt 一样被 eval | 将 agent skill eval 定义为 prompt→trace→checks→score | **例子**: `codex exec --json` 输出 JSONL 事件流，每个 `command_execution` 都可追溯 | 文章代码示例 | 中高 — 框架清晰，但缺乏大规模实证 |
| 10-20 个 prompt 就够了 | 小而有针对性的 prompt 集优于大规模 benchmark | **例子**: 4 个测试用例覆盖 explicit/implicit/contextual/negative 四类场景 | 文章 CSV 示例 | 中 — 经验性建议，未给出充分性论证 |
| 两层 grading 互补 | 确定性检查 + 模型辅助 rubric | **例子**: Layer 1 检查 `npm install` 是否执行；Layer 2 用 `--output-schema` 评分组件结构和 Tailwind 配置方式 | 文章代码示例 | 高 — 分层设计合理，确定性优先 + 模型兜底 |
| name/description 是触发的关键 | skill 的 name 和 description 决定了是否/何时被注入 context | **例子**: "set up a quick React demo" 应该触发但可能不触发；"add Tailwind styling" 不该触发可能触发 | 文章三类假设 | 高 — 直接来自 Codex 内部机制 |

---

## 批判性思考

| 问题 | 分析 |
|------|------|
| 核心假设及失效场景 | **假设**: skill 的行为可以被分解为一组离散的、可检查的步骤和产出。**失效场景**: 当 skill 的价值在于创造性判断（如"设计一个好的 API"）而非确定性流程时，确定性检查和 rubric 评分都会退化为 proxy metrics，无法捕捉真正的质量差异。文章选择的 `setup-demo-app` 示例恰好是最适合 eval 的类型（脚手架类、确定性强），但 skill 越偏向判断性/创造性，这套方法的适用性越弱。 |
| 关键局限 | - 两层 grading 中 Layer 2（模型辅助）本身依赖 LLM，引入了评估者自身的不确定性和成本。当 eval 需要大量运行时，每次 Layer 2 都是一次完整的 Codex 调用<br>- 文章完全没讨论 eval 的成本模型：每次 `codex exec` 的 token/时间成本、CI 中的频率上限<br>- 缺乏对 flaky eval 的讨论——agent 行为本身有随机性，同一 prompt 多次运行可能产生不同结果 |
| 实验充分性 | 缺失验证: 文章是一篇实践指南而非实验论文，没有给出任何定量结果（如：使用这套 eval 流程后，skill 的回归率下降了 X%；或 10 个 prompt 的覆盖率与 50 个的对比）。所有建议都是经验性的，"10-20 个 prompt 够了"缺乏充分性论证。 |

### 与我的 digital-brain skill 系统的关联

这篇文章对我的 skill 开发有直接的实践价值：

1. **skill-creator 中的 eval 功能**：我的 `skill-creator` skill 已经有 eval 能力，但这篇文章的四类 prompt 测试用例（explicit/implicit/contextual/negative）比我当前的 eval 设计更系统化。特别是**负控制**用例——测试 skill 不应该触发的场景——是一个我还没有充分覆盖的方向。

2. **两层 grading 架构可迁移**：对于我的 `paper-reading` skill，Layer 1 可以检查"sources.jsonl 是否更新了"、"notes.md 是否包含必要结构"；Layer 2 可以评估笔记的叙事质量。

3. **"每次手动修复变成一个 eval case"的循环**：这与我在 `feedback` memory 中记录修正的模式类似，但更机械化——不是记住"下次别这样"，而是直接写成一个自动化检查。

---

## 关键洞察

- **Eval = prompt → trace → checks → score** — 这个四步定义是理解 agent skill 评估的最小完整框架
- **确定性优先，模型兜底** — 先用文件检查/命令检查覆盖能覆盖的，只有定性需求才引入模型辅助评分
- **四类 prompt 测试用例** — explicit / implicit / contextual / negative control，确保触发精度和召回的平衡
- **name/description 是 skill 的触发门控** — 模糊或过载的描述会导致 skill 不触发或误触发，这是 eval 要首先覆盖的
- **每次手动修复 = 一个新的 eval case** — 构建从失败到改进的飞轮，让 skill 的质量单调递增
