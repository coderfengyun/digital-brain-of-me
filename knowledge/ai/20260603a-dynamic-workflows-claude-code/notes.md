# A harness for every task: dynamic workflows in Claude Code

**类型**: 方法

---

## 🗺️ 全局地图

### 一句话摘要
> Claude Code 现在能为每个任务动态生成定制的 JavaScript 工作流（harness），通过多 agent 编排克服单上下文窗口的固有局限，将 Claude Code 从编码工具扩展为通用任务引擎。

### 段落分类

| 章节/段落 | 分类 | 一句话说明 |
|-----------|------|-----------|
| 开头介绍 | [连接] | 从 Claude Code 默认 harness 过渡到动态工作流的引出 |
| Example prompts | [支撑] | 用 8 个示例 prompt 具象化工作流的可能性 |
| How dynamic workflows work | [核心] | 工作流的技术机制——JS 文件 + subagent 编排 + 模型/worktree 选择 |
| Why dynamic workflows | [核心] | 单上下文窗口的三个失效模式（laziness, bias, drift）及工作流如何解决 |
| Dynamic vs static workflows | [核心] | 动态 vs 静态工作流的本质区别——通用 vs 定制 |
| Helpful patterns | [核心] | 六种可组合的 agent 编排模式 |
| Use cases | [支撑] | 十个具体应用场景展开 |
| When not to use | [连接] | token 成本约束和适用边界 |
| Tips | [支撑] | 实用技巧：prompting、/goal+/loop、token budget、保存分享 |

### 结构地图

```
问题: 单上下文窗口在复杂任务中有三种失效模式
↓
观察: 已有专用 harness（Research、Code Review 等）证明了多 agent 编排的价值
↓
方案: 让 Claude 动态生成任务专用的 JS 工作流
├→ 机制: JS 文件 + spawn/coordinate subagents + 模型路由 + worktree 隔离
└→ 六种编排模式: classify-and-act / fan-out / adversarial / generate-filter / tournament / loop-until-done
↓
应用: 迁移重构 / 深度研究 / 验证 / 排序 / 规则遵循 / 根因分析 / 分流 / 探索 / eval / 模型路由
↓
约束: token 成本更高，常规编码任务不需要
```

---

## 📖 核心叙事 (Narrative)

### 为什么需要动态工作流（精读）

Claude Code 默认在单一上下文窗口中既计划又执行。当任务变得长时间、大规模并行、或需要对抗性验证时，会触发三种失效模式：

1. **Agentic laziness** — 在复杂多步任务中提前宣布完成（如安全审查只做了 20/50 条）
2. **Self-preferential bias** — 倾向于偏好自己的输出，无法客观验证
3. **Goal drift** — 经过多轮 compaction 后原始目标细节丢失

动态工作流通过**将任务分解为多个独立 Claude 实例**，每个实例有自己的上下文窗口和聚焦目标，结构性地消除这些问题。

### 技术机制（精读）

- 执行一个 **JavaScript 文件**，内含特殊函数用于 spawn 和 coordinate subagents
- 可使用标准 JS 函数（JSON、Math、Array）处理数据
- 工作流可以决定每个 agent 使用哪个模型（intelligence routing）
- 可以指定 subagent 在独立 worktree 中运行（isolation）
- 中断后恢复 session 可以继续执行

### 动态 vs 静态（精读）

静态工作流（Agent SDK / `claude -p`）需要覆盖所有 edge case，因此天然更通用。动态工作流由 Claude Opus 4.8 实时生成，是为当前具体任务量身定制的 harness。这是模型能力提升带来的范式转变——从"人写通用编排"到"AI 写专用编排"。

### 六种编排模式（精读）

| 模式 | 机制 | 适用场景 |
|------|------|----------|
| Classify-and-act | 分类器 agent 路由到不同行为 | 任务类型不确定时 |
| Fan-out-and-synthesize | 拆分→并行执行→barrier 汇合 | 大量独立子步骤 |
| Adversarial verification | 每个产出配一个对抗验证 agent | 需要客观评判时 |
| Generate-and-filter | 生成→过滤→去重→留最优 | 创意探索 |
| Tournament | N 个 agent 竞争同一任务，两两淘汰 | 方案选优 |
| Loop until done | 循环直到停止条件满足 | 工作量不确定 |

### 应用场景（扫读）

- **迁移重构**: Bun 从 Zig 到 Rust 用了 workflow；每个 callsite/模块一个 subagent in worktree + adversarial review
- **深度研究**: /deep-research skill 已内置；fan-out 搜索 → 验证 → 综合报告
- **深度验证**: 一个 agent 识别所有事实声明 → 每个声明分配验证 agent
- **排序**: tournament 或 pairwise comparison（比较判断比绝对打分更可靠）
- **规则遵循**: 每条规则一个 verifier agent + skeptic agent 避免假阳性
- **根因分析**: 从不相交证据（logs/files/data）独立生成假说 → 验证面板
- **大规模分流**: classify + dedup + action；quarantine 模式隔离读取和执行权限
- **探索与品味**: rubric + review agent 判断完成条件；tournament 选优
- **Evals**: worktree 中独立执行 → comparison agents 对比评分
- **模型路由**: classifier agent 预研任务复杂度 → 选择 Sonnet 或 Opus

### 何时不使用（扫读）

Token 成本显著更高。常规编码任务无需 5 个 reviewer 的 panel。问自己："这真的需要更多 compute 吗？"

### 实用技巧（扫读）

- 触发词 "ultracode" 确保生成 workflow
- 搭配 `/goal`（硬完成标准）和 `/loop`（周期运行）
- 可设 token budget（如 "use 10k tokens"）
- 按 "s" 保存，存入 `~/.claude/workflows` 或通过 skill 分发

---

## 📊 数据证据层 (Evidence)

| 论点 | 创新点 | 支撑数据 | 数据来源 | 说服力评估 |
|------|--------|----------|----------|------------|
| 单上下文窗口有三种失效模式 | 将 agent 质量问题结构化为 laziness/bias/drift | **例子**: 安全审查只完成 20/50 条（laziness）；compaction 丢失 "don't do X" 约束（drift） | 文章 "Why dynamic workflows" 章节 | ⭐⭐⭐ 强——与实践经验高度吻合 |
| 动态工作流优于静态工作流 | "AI 写 harness"取代"人写 harness" | **例子**: 静态需覆盖所有 edge case → 通用；动态由 Opus 4.8 实时定制 | "Dynamic vs static" 章节 | ⭐⭐ 中——缺乏定量对比 |
| 六种编排模式可组合 | 将 multi-agent 编排归纳为六种原语 | **例子**: Bun 重写用 fan-out + adversarial；排序用 tournament（pairwise > absolute scoring） | "Helpful patterns" + "Use cases" | ⭐⭐⭐ 强——模式命名清晰、场景覆盖广 |
| 工作流不限于编码任务 | 将 Claude Code 从 IDE agent 扩展为通用任务引擎 | **例子**: 简历排序、商业计划多角度撕裂、Slack 事故根因挖掘 | "Example prompts" 章节 | ⭐⭐ 中——示例丰富但无量化效果 |

---

## 🤔 批判性思考 (Critical Thinking)

| 问题 | 分析 |
|------|------|
| 核心假设及失效场景 | **假设**: 模型足够聪明能写出好的编排 JS，且编排开销 < 质量收益。<br>**失效场景**: (1) 模型生成的工作流有 bug 导致无限循环或资源耗尽；(2) 任务本身简单但被过度编排，token 浪费 10x；(3) 用户无法理解/调试动态生成的 JS 工作流 |
| 关键局限 | - 无定量数据证明"动态 > 静态"在各场景的 token 效率和质量优势<br>- 对工作流可靠性（中断恢复、错误处理）的讨论很浅<br>- 未讨论安全隔离——workflow 中 subagent 的权限边界如何设定<br>- "ultracode" 触发词的存在暗示模型并非总能自主判断何时需要 workflow |
| 与已有知识的关系 | 本文是 harness engineering 系列的最新演进。之前读过的 autoharness、harness-engineering、gstack 都在讲"如何设计好的 agent 编排"，本文的创新是**让模型自己设计编排**——从 meta-harness 到 self-harness。六种模式与之前 agent-skill-design-patterns 的 pattern 有对应，但更聚焦于多 agent 协调而非单 agent 技能设计。 |
