# ResearchRubrics: A Benchmark of Prompts and Rubrics For Evaluating Deep Research Agents

**类型**: 方法
**来源**: arXiv:2511.07685v1 | Scale AI | 2025-11-10
**作者**: Manasi Sharma, Chen Bo Calvin Zhang, Chaithanya Bandi 等 (Scale AI)

---

## 🗺️ 全局地图

### 一句话摘要
> 提出 ResearchRubrics——一个用 2500+ 条人工编写的细粒度评测标准来衡量 Deep Research Agent 质量的基准，发现当前最好的 Agent（Gemini DR）合规率也不超过 68%，主要失败点在隐式推理和多文档综合。

### 段落分类

| 章节 | 分类 | 一句话说明 |
|------|------|-----------|
| Abstract + Introduction | [核心] | 问题定义：DR 评测难，现有 benchmark 不够用；提出 ResearchRubrics |
| Related Work (Table 1) | [连接] | 梳理 14 个现有 benchmark 的短板，定位本文贡献 |
| Section 3.1 数据收集 | [核心] | 三阶段人工流程：Expert1 起草 → Expert2 审核 → Expert3 终审 |
| Section 3.2 复杂度框架 | [核心] | 三轴复杂度：概念广度、逻辑嵌套深度、探索程度 |
| Section 3.3 Rubric 设计 | [核心] | 六类评测维度 + 强制/可选分层 + [-5,5] 权重体系 |
| Section 3.4 评测方法 | [支撑] | LLM-as-judge 三级打分公式，Macro F1 验证 |
| Section 4.1 实验设置 | [支撑] | 评测 OpenAI DR / Gemini DR / Perplexity DR，用 GPT-5/Claude/Gemini 做 judge |
| Section 4.2 主要结果 | [核心] | Gemini DR 最高 67.7%，隐式推理+综合占失败的 45-50% |
| Section 4.3 Human-LLM 对齐 | [支撑] | 二值打分 F1 达 0.72-0.76，三值打分降至 0.53-0.57 |
| Section 4.4 Rubric 设计影响 | [核心] | 加例子 +3-4% 对齐；LLM 自动扩写 rubric 反而 -15-20% |
| Section 4.5 讨论 | [核心] | 失败模式是架构层面限制，而非提示工程问题 |
| Section 5 结论 | [连接] | 从 Abstract 过渡到后续工作方向 |

### 结构地图

```
问题: Deep Research 任务开放、多文档、输出长——现有评测方法不够用
↓
观察: 现有 benchmark 两大缺陷:
  ├→ 依赖静态答案/自动生成 rubric（缺乏人工质控）
  └→ 评测粒度太粗（匹配分、overlap 指标）
↓
方法: ResearchRubrics
  ├→ 数据: 101 个多领域 prompt（三专家流程，非 LLM 生成）
  ├→ 标注: 2593 条 rubric（六类维度，[-5,5] 权重，强制/可选分层）
  ├→ 复杂度框架: 三轴标注（广度/嵌套深度/探索性）
  └→ 评测协议: LLM-as-judge + 三值打分 + Macro F1 验证
↓
验证:
  ├→ 评测 3 个 DR 系统：Gemini DR > OpenAI DR > Perplexity DR
  ├→ Human-LLM 对齐验证（二值 F1: 0.72-0.76）
  └→ Rubric 设计消融（加例子 vs LLM 扩写）
↓
结论: 所有 Agent 合规率 <68%；失败集中于隐式推理/综合；需架构创新
```

---

## 📖 核心叙事 (Narrative)

### 为什么现有 DR 评测不够用

DR 任务的三个特性让评测变难：输出很长、答案多样、依赖动态信息源。现有方案各有缺陷：
- **简单 QA benchmark**（HotpotQA, GAIA）：只验证短答案，无法覆盖多文档综合
- **自动生成 rubric**（DeepResearch Bench, DeepResearch Arena）：有循环论证风险，可能错过领域细节
- **窄域评测**（DeepScholar-Bench, ReportBench）：只评学术写作，不反映真实用户需求

最接近的 ExpertLongBench 虽然也用人工 rubric，但依赖高质量参考答案，限制了 prompt 范围（只能选有标准参考的任务）。ResearchRubrics 不依赖参考答案，直接用 LLM-judge 按 rubric 打分。

### 三轴复杂度框架

这是一个有实用价值的分类工具，把每个 prompt 标注为三维坐标：

**概念广度（Conceptual Breadth）**
- Simple：单领域，1 个信息源
- Moderate：2-5 个子议题，弱耦合
- High：>5 个信息源或跨领域（如 "分析亚洲可再生能源的环境、经济、政治因素"）

**逻辑嵌套深度（Logical Nesting）**
- Shallow：单步推理
- Intermediate：2-3 步依赖推理
- Deep：4+ 步，含 "分析→综合→评估→修订" 层级规划（如 "制定投资策略+压力测试+应急方案"）

**探索程度（Exploration）**
- Low：完全指定，无歧义
- Medium：1-2 个未指定因素
- High：3+ 个关键因素未指定，需要 Agent 自己澄清目标（如 "我想换一个有前景的职业，应该怎么考虑？"）

### Rubric 设计：六类维度 + 强制/可选分层

六类评测轴：
1. **显式要求**（Explicit Requirements）：是否回答了 prompt 明确要求的内容
2. **隐式要求**（Implicit Requirements）：专业人士会期待但未明说的内容（如解释一种医疗手术时，好的回答还应提到副作用和费用）
3. **信息综合**（Synthesis）：是否跨多个来源整合，而不是列清单
4. **引用使用**（Use of References）：引用是否准确、相关、真正支持论点
5. **表达质量**（Communication Quality）：清晰、组织、语气
6. **指令遵循**（Instruction Following）：是否遵守显式约束

权重体系：[-5, 5]，|w| ≥ 4 为强制标准，|w| ≤ 3 为可选标准。负权重惩罚常见错误（如事实错误、跑题）。

### 主要实验结果

**整体合规率（Table 5）**

| 系统 | 三值 | 二值 |
|------|------|------|
| Gemini DR | 67.7% | 61.5% |
| OpenAI DR | 66.4% | 59.7% |
| Perplexity DR | 56.6% | 48.7% |

三个系统无一超过 70%。

**失败分布**：隐式推理 + 综合 共占失败的 45-50%。显式检索和表达质量失败率 <20%。模式跨三个系统一致，说明是架构局限而非实现差异。

**复杂度维度的影响**：逻辑嵌套深度对性能的影响最强——超过 4 步推理时，所有系统普遍崩溃。概念广度的影响相对较小。

**强制 vs 可选标准的倒置**：在大多数维度，强制标准驱动失败；但在隐式推理维度，可选标准反而是主要失败源——说明 Agent 能满足基本隐式要求，但无法做到高质量。

**引用 breadth vs accuracy 的权衡**：
- Gemini DR：111 条引用，81% 准确率
- Perplexity DR：31 条引用，90% 准确率

两者都无法同时兼顾。

### Rubric 设计消融（Section 4.4）

关键发现：
- 在 rubric 中加入具体例子（"e.g., 例子1, 例子2"）→ 对齐提升 3-4%（二值）
- LLM 自动扩写/重述 rubric → 对齐**灾难性下降** 15-20%

这反直觉：更详细的描述反而让 judge 模型和人类更难达成共识。原因可能是 LLM 扩写引入了语义漂移和强调偏移。

---

## 📊 数据证据层 (Evidence)

| 论点 | 创新点 | 支撑数据 | 数据来源 | 说服力评估 |
|------|--------|----------|----------|------------|
| 最强 DR Agent 合规率不超过 68% | 提供了最细粒度的多维评测基准 | Gemini DR 67.7%（三值）/61.5%（二值）；OpenAI DR 66.4%/59.7% | Table 5 | ⭐⭐⭐ 强（三个系统一致，跨 judge 模型稳健） |
| 隐式推理+综合是主要失败点 | 将失败分解到 rubric 轴级别 | 两类失败合计占 45-50%；显式检索失败 <20% | Figure 5 | ⭐⭐ 中（失败分解方法合理，但绝对数字依赖 rubric 定义） |
| LLM 扩写 rubric 反而降低评测可靠性 | Rubric 设计消融 | 自动扩写后 F1 下降 15-20%；加例子则提升 3-4% | Table 7 | ⭐⭐⭐ 强（有明确 ablation，三个 DR 系统结果一致） |
| 二值打分比三值打分与人类更对齐 | 打分粒度影响量化 | 二值 Macro F1: 0.72-0.76；三值: 0.53-0.57，差距约 20pp | Table 6 | ⭐⭐⭐ 强（9 位专家标注，303 份响应） |
| 逻辑嵌套深度是最难的复杂度维度 | 三轴复杂度框架的实证验证 | **例子**: Deep 级嵌套（4+ 步推理）时所有系统合规率普遍崩溃；Shallow 任务表现良好 | Figure 6/13 | ⭐⭐ 中（趋势清晰，但"崩溃"的具体数字未给出精确下降幅度） |

---

## 🤔 批判性思考 (Critical Thinking)

| 问题 | 分析 |
|------|------|
| 核心假设及失效场景 | **假设**: 101 个 prompt + 2593 条人工 rubric 能代表"真实 DR 任务"的完整分布<br>**失效场景**: 所有专家都有 STEM 背景（论文明确说明），对人文/法律/医疗等高度专业化领域的覆盖可能存在系统偏差；此外，样本量 101 个 prompt 相对较小，对某些域可能过拟合到少数专家的认知框架 |
| 关键局限 | - **评测者污染**：用 GPT-5/Gemini-2.5-Pro 评测时，Gemini DR 和 GPT DR 与 judge 模型来自同家公司，可能存在隐式偏好对齐<br>- **静态快照**：DR 任务依赖实时信息，benchmark 建成后 rubric 可能与实际最优答案漂移<br>- **规模**：只评测了 3 个商业系统，未覆盖开源 Agent；101 个 prompt 较少（对比 Mind2Web2 的 50 条/任务 rubric，但更多任务数） |
| 实验充分性 | **缺失验证**: (1) 不同领域专家的 rubric 编写者间一致性（IRR）未报告——只知道三专家流程，但不知专家间分歧多大；(2) LLM 扩写 rubric 的 -15-20% 是严重发现，但论文未深入分析"哪类语义漂移"导致失败，难以指导修复；(3) 所有 DR 系统均为黑盒商业产品，无法分解架构因素 |
