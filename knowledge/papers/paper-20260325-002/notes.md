# Harness Design for Long-Running Application Development

**类型**: 方法

---

## 核心叙事 (Narrative)

### 一句话概括
> 借鉴 GAN 的对抗思想，用 generator-evaluator 分离架构解决 AI agent 的自评偏差问题，在前端设计和长时自主编程中实现显著质量提升。

### 叙事结构

```
问题: AI agent 在长时编程任务中有两个顽固失败模式——上下文退化和自评偏差
↓
观察: Agent 自评时倾向于给自己打高分，即使输出明显平庸；尤其在设计等主观任务上
↓
假设: 将"做事的 agent"和"评判的 agent"分离，可以打破自评偏差的闭环
↓
方法 v1: GAN 启发的 generator-evaluator 架构（前端设计 → 三 agent 全栈开发）
↓
验证: Retro Game Maker 实验——solo 核心功能不工作 vs harness 产出 16 功能完整应用
↓
简化: 新模型（Opus 4.6）能力提升 → 去掉 sprint 分解，evaluator 改为单次终审
↓
验证 v2: DAW 实验——3h50m/$125 产出浏览器端 DAW，builder 连续运行 2h+ 不丢失连贯性
↓
结论: Harness 的有趣组合空间不会随模型进步缩小，而是移动——工程师要不断找到下一个有效组合
```

---

## 数据证据层 (Evidence)

| 论点 | 创新点 | 支撑数据 | 数据来源 | 说服力评估 |
|------|--------|----------|----------|------------|
| Generator-evaluator 分离提升设计质量 | 借鉴 GAN 对抗思想用于主观评估 | 荷兰博物馆案例：第10轮 evaluator 反馈后 generator 从平面布局跳跃到 3D CSS 空间体验 | 前端设计实验 | ⭐⭐ 中。案例引人注目但仅是单一案例，无系统性定量对比 |
| 完整 harness vs solo 的质量差距 | 三 agent 架构（planner-generator-evaluator） | Solo: 20min/$9，核心功能不工作；Harness: 6hr/$200，16功能完整应用 | Retro Game Maker 实验 | ⭐⭐⭐ 强。有直接对比，质量差异明确（solo游戏不能玩 vs harness可玩） |
| Evaluator 能捕获具体 bug | 独立 QA agent 用 Playwright 真实交互测试 | Sprint 3 的 27 条验收标准；3个具体 bug 示例（fill tool、entity deletion、route ordering） | Evaluator 日志 | ⭐⭐⭐ 强。Bug 描述精确到代码行，可验证 |
| 模型进步允许简化 harness | 根据模型能力动态调整架构复杂度 | V1(Opus 4.5): 需要 sprint 分解 + per-sprint QA；V2(Opus 4.6): 去掉 sprint，builder 连续 2h+ 保持连贯 | DAW 实验 | ⭐⭐ 中。仅两个不同任务的对比，变量未完全控制 |
| Evaluator 的价值随模型能力变化 | evaluator 是条件性组件而非固定组件 | V2 中 QA 仍然捕获了 stub-only 功能、缺失的交互深度等问题 | DAW 实验日志 | ⭐⭐⭐ 强。具体引用了 QA 反馈内容 |
| 自评偏差是可调节的 | 独立 evaluator 比自评更容易调教 | "tuning a standalone evaluator to be skeptical turns out to be far more tractable than making a generator critical of its own work" | 作者工程经验 | ⭐⭐ 中。定性观察，无定量数据 |

---

## 批判性思考 (Critical Thinking)

| 问题 | 分析 |
|------|------|
| 核心假设及失效场景 | 假设: 分离 generator 和 evaluator 能打破自评偏差。<br>失效场景: 如果 evaluator 本身的判断力不足（作者也承认"out of the box, Claude is a poor QA agent"），分离并不自动解决问题——需要大量手动调教。那么关键贡献到底是"分离架构"还是"prompt 调教技巧"？文章对此界限模糊。 |
| 关键局限 | - **成本与可复制性**：$124-200/次，4-6小时运行时间，普通开发者难以承受迭代<br>- **任务类型单一**：仅测试了"从零构建新应用"场景，未涉及维护、重构、多人协作<br>- **Evaluator 调教的可迁移性**：作者花了"several rounds"调教 evaluator 到合理水平，这个过程本身的成本和可复制性未讨论<br>- **Score 非单调递增**：作者承认"I regularly saw cases where I preferred a middle iteration over the last one"，说明 evaluator 的评分与真实质量仍有 gap |
| 实验充分性 | 缺失验证:<br>- 无 ablation study：planner/evaluator/sprint 各自的独立贡献未量化<br>- 无跨任务泛化测试：两个案例（游戏、DAW）都是单一 prompt 的单次运行<br>- 无与其他多 agent 框架的对比（如 AutoGen、CrewAI）<br>- "context anxiety" 概念有趣但未给出定量测量方法 |

---

## 关键收获

1. **Harness 是对模型能力缺口的编码**：每个组件都是一个假设（"模型不能自己做X"），必须随模型升级重新验证。这是一个非常重要的工程心法。

2. **自评偏差是 LLM agent 的系统性问题**：不是个别模型的 bug，而是 LLM 的结构性倾向。分离 evaluator 是一个可行的系统级解决方案。

3. **评估标准比评估架构更重要**：前端实验中，仅靠四条 grading criteria（在第一轮迭代前就生效）已经显著提升了输出质量。这暗示 evaluator 的核心价值不在于"评估"本身，而在于**将模糊的质量标准具体化**。

4. **Sprint contract 模式**：generator 和 evaluator 在实现前先协商"什么算完成"——这是将人类工程实践直接映射到 agent 协作的好例子。

5. **简化原则**：模型进步后应主动剥离不再 load-bearing 的 harness 组件。复杂度不是免费的——每个组件增加延迟、成本和调试难度。
