# RubricEval：面向指令遵循中 LLM 裁判的 Rubric 级元评测基准

作者：Tianjun Pan、Xuan Lin、Wenyan Yang、Qianyu He、Shisong Chen、Licai Qi、Wanqing Xu、Hongwei Feng、Bo Xu、Yanghua Xiao  
机构：复旦大学、东华大学、蚂蚁集团  
原文：arXiv:2603.25133v1，2026-03-26

## 摘要

基于 rubric 的评测已经成为评价大语言模型指令遵循能力的主流范式。尽管被广泛采用，这种 rubric 级评测是否可靠仍不清楚，因此需要元评测。然而，以往元评测主要停留在 response 层，无法衡量 rubric-based evaluation 所依赖的细粒度判断准确性。为弥补这一缺口，我们提出 RubricEval。该基准具有三个特点：（1）首个面向指令遵循的 rubric 级元评测基准；（2）指令和 response 覆盖多个类别与模型来源；（3）包含 3,486 个经过质量控制的实例，并提供更能区分 judge 能力的 Easy/Hard 子集。实验表明，rubric 级判断远未解决：即使被 instruction-following benchmark 广泛用作 judge 的 GPT-4o，在 Hard 子集上也只有 55.97%。就评测范式而言，rubric-level 优于 checklist-level；显式推理能够提高准确率；二者结合还会降低不同 judge 之间的方差。借助本文建立的 rubric taxonomy，我们进一步识别常见失败模式，并为可靠的指令遵循评测给出可执行建议。

## 1 引言

指令遵循是 LLM 的基础能力，因为它直接影响任务完成质量和用户体验。因此，可靠评测指令遵循同样重要。

一个核心问题是：如何可靠地评价 LLM 的 instruction-following 行为？IFEval 等规则方法具有可扩展性和高精度，但只适用于少量可验证约束。为了处理包含复杂语义约束的开放式指令，InfoBench、CFBench、ComplexBench、IOPO 等近期工作将指令拆成细粒度 rubric，再让 LLM judge 验证每一条 rubric。虽然这套方法已广泛用于评测，但单条 rubric 的误判会经由聚合传播，并影响模型训练、self-evolving 和 benchmark 计分，因此 judge 的可靠性至关重要。

对 LLM judge 进行元评测已不可或缺，但现有 instruction-following meta-evaluation 存在三个问题：

1. **粒度太粗**：只在 response 层判断整体质量，和现代 rubric-based evaluation 不匹配，也无法衡量细粒度判断能力。
2. **指令覆盖有限**：指令较简单、类型单一，难以反映不同真实场景。
3. **缺少真实失败**：依赖合成或人工挑选的错误，而非模型真实生成的 response，可能无法反映实际 judge 表现。

为此，我们提出 RubricEval。它在 rubric 层直接评 judge，使用多样的真实模型 response，并通过带人工验证的多阶段流程获得可靠参考标签。具体任务是：给定 instruction、response 和目标 rubric，候选 judge 判断 response 是否满足该 rubric；再把预测与高置信参考标签比较。

RubricEval 包含四类指令下的 3,486 个 rubric-level judgment instances，其中 Easy 2,034 个、Hard 1,452 个。本文贡献包括：首个指令遵循 rubric-level meta-evaluation benchmark；可扩展的 Rubric Arbitration Framework（RAF）；以及对 judge、评测协议和 rubric 失败类型的系统分析。

## 2 相关工作

### 指令遵循 benchmark 与评测

IFEval 等早期 benchmark 依靠规则验证可检验约束，之后 Multi-IF、CELLO 和 IFBench 扩展到多语言、真实场景和更多约束类型。这类方法客观，但局限于可验证规则。另一条路线由 InfoBench 代表：把指令拆成若干问题，让 LLM judge 做细粒度验证。ComplexBench 再结合规则和模型评测以提高可靠性。Rubric-level judgment 也被用于 RL reward，但这些判断本身的可靠性一直缺少系统研究。

### LLM judge 的元评测

RewardBench 2、JudgeBench、JETTS 和 VerifyBench 分别从 preference pair、困难 response pair、test-time selection 和 reasoning verifier 等角度评 judge。在 instruction following 中，LLMBar 是首个 meta-evaluation benchmark，它构造一条遵循指令的 response 与一条存在细微偏离的 response；ReIFE 则扩展到更多 judge 配置。但这些工作都只在 response 层评 judge。RubricEval 补上了 rubric-level 的空白。

## 3 RubricEval

### 3.1 任务定义

在 rubric-based instruction-following evaluation 中，judge 接收 instruction `x`、response `y` 和 rubric `r`，输出二值判断 `j`：

```text
j = IF_Rubric_Judge(x ⊕ y ⊕ r),  j ∈ {0, 1}
```

`1` 表示 response 满足 rubric，`0` 表示不满足；rubric 是从 instruction 分解出的一个具体标准。

### 3.2 数据收集

我们覆盖 Constrained、Compositional、Multi-turn 和 System 四类指令，并尽量从多个 benchmark 收集 instruction 和对应 rubric，以降低单一来源偏差。所有 rubric 均由人类编写或验证。

为增加 response 多样性，每条 instruction 随机分配给开源模型池中的一个模型生成回答。过去工作常通过 instruction-response 错配合成失败，效率虽高但不真实；本文保留模型原始回答，让错误自然发生，从而捕获实际失败模式。

### 3.3 标签标注

判断 response 是否满足某条 rubric 往往具有主观性，response 或 rubric 的歧义也会产生边界案例，完全人工标注难以扩展。因此本文设计了自动化、高置信的标签框架。

#### 3.3.1 人工标注集

我们从 LLM judges 发生分歧的样本中抽取 506 个 instruction-response-rubric 三元组，保证其非平凡性。两名标注员独立判断，冲突通过讨论解决；正负标签保持平衡。

#### 3.3.2 Rubric Arbitration Framework

我们先在人工参考集上比较候选 judge，最终选取 GPT-4.1、Claude-Sonnet-4.5、Gemini-2.5-Flash 和 DeepSeek-v3.2-exp 作为四个 base judges。

四个 judge 全票一致时，准确率为 96.6%，κ=0.93；但对于争议样本，多数投票只有 69.5%，κ=0.39，最佳单 judge o3 也只有 79.9%，κ=0.60。加入两个 meta-judges 阅读 base judges 的理由并仲裁后，争议样本准确率升至 85.4%，κ=0.69。

RAF 是一个重可靠性、轻覆盖率的三级流程：

1. **粗粒度过滤**：四个 base judges 一次评价某个 instruction-response pair 的完整 checklist；只让有争议的 rubric 进入后续流程。
2. **细粒度重评**：四个 base judges 分别对每条争议 rubric 单独判断并给出理由；全票一致者形成 RubricEval-Easy。
3. **Meta-judge 仲裁**：仍有分歧的 rubric 交给 o3 和 DeepSeek-R1；二者同意者形成 RubricEval-Hard，其余丢弃。

### 3.4 人工验证

我们从最终数据的不同子集和指令类型中随机抽取 160 个实例，由两名标注员独立判断并讨论分歧。Human-RAF agreement 为 85.0%，Cohen’s κ=0.702，说明 RAF 与人类判断具有 substantial agreement，可作为元评测的近似 ground truth。

### 3.5 数据统计

最终 benchmark 包含 1,989 条 instruction 和 3,486 个 rubric-level instances，其中 Easy 2,034 个、Hard 1,452 个。

为了分析不同类型 rubric 的 judge 表现，我们建立四个高层维度、13 个细类：

- **Content**：Content Inclusion、Content Exclusion、Topic Scope；
- **Form**：Quantity Limit、Format Structure、Ordering Sequence；
- **Quality**：Quality Requirements、Conditional Logic、Task Completion；
- **Style**：Style Tone、Language Linguistics、Multi-turn Coherence、Role Persona。

分布呈长尾形态，与真实任务的自然分布相符。

## 4 实验

### 4.1 实验设置

Rubric judgment 是二分类任务；考虑类别不平衡，报告 Balanced Accuracy 和 Macro F1。评测时要求 judge 先给理由，再输出最终判断，以更充分体现其评测能力。被测 judge 覆盖不同家族、规模的开源和闭源模型，并分别在 Easy 与 Hard 上报告结果。

### 4.2 主要结果

Easy 上，小型开源模型约为 65% BAcc，Qwen3-235B 和 gpt-oss-120b 接近 90%。Hard 上，即使商业模型也很困难：GPT-4o 只有 55.97%，Claude-Sonnet-4.5 为 55.65%。这说明 rubric-level judging 远未解决；在 benchmark 或 rubric-based RL 中直接采用小型开源 judge，可能产生噪声甚至误导性信号，GPT-4o 也可能引入系统偏差。

| Judge | Easy BAcc（如有） | Hard BAcc | Hard Macro F1 |
|---|---:|---:|---:|
| Qwen3-235B | 89.87 | 63.85 | 55.44 |
| gpt-oss-120b | 89.55 | 75.89 | 72.48 |
| GPT-4o | 84.41 | 55.97 | 49.68 |
| o3-mini | 87.17 | 70.24 | 61.99 |
| GPT-5.1 | — | 72.28 | 68.23 |
| o3 | — | 84.81 | 79.10 |
| Claude-Sonnet-4.5 | — | 55.65 | 48.41 |
| Gemini-3-Flash | — | 79.93 | 76.92 |
| Gemini-3-Pro | — | 83.04 | 79.51 |

同一模型从 Easy 到 Hard 均显著下降：GPT-4o 下降 28.4pp（84.41→55.97），Qwen3-235B 下降 26.0pp，gpt-oss-120b 也下降 13.7pp。这验证了两级构造确实能区分难度。

Compositional instruction 通常最难，因为 judge 必须正确解析逻辑结构并将每条 rubric 对齐到 response 的具体部分；Multi-turn 相对容易，可能因为对话历史提供了额外线索。Constrained 和 System 难度居中。

## 5 分析

### 5.1 评测范式是否重要

本文从两个轴比较四种协议：粒度上，checklist-level 一次评完整 rubric 列表，rubric-level 每条 rubric 单独调用；推理上，比较直接判断与先生成理由。

Rubric-level 在两个模型和所有指令类型上均优于 checklist-level。开启 reasoning 后，rubric-level 的 Qwen/GPT BAcc 为 77.38%/82.17%，checklist-level 仅 69.90%/70.44%，相差 7–12pp。

显式 reasoning 也稳定提高准确率：rubric-level 下 Qwen 和 GPT 分别提高 8.4pp、6.7pp；checklist-level 下分别提高 9.0pp、7.0pp。

### 5.2 取舍

Checklist-level 迫使 judge 在一次调用中验证多条标准，增加认知负担和漏项风险；rubric-level 隔离每个决策，减少相互干扰。Reasoning 则迫使 judge 用证据支撑结论，而不是凭直觉判断。

但二者都有成本：逐 rubric 评测需要为每条标准单独调用，显著增加延迟和费用；reasoning 又增加输出 token。因此存在 reliability-efficiency trade-off。采用 checklist-level direct verdict 虽便宜，却可能牺牲可靠性。

### 5.3 Judge 间分析

以 CFBench 为例，我们让 GPT-4o、Qwen3-235B 和 GPT-5.1 在四种协议下评价同一批 Qwen2.5-7B response。最基础的 checklist-level 无 reasoning 设置中，CSR 得分从 55% 到 80%，judge 间相差 25pp；改为 rubric-level + reasoning 后，范围缩至 62%–74%，差距降到 12pp。更细粒度并加入推理，可以提高准确率和一致性，但无法消除 judge 能力差异。

### 5.4 错误分析

多数 judge 在 Topic Scope、Format Structure、Quality Requirements、Task Completion 和 Role Persona 上表现较弱。这些 rubric 通常要求严格核对证据，或本身具有较强主观性。

Format Structure 和 Role Persona 对所有 judge 都难：前者提示格式验证可能更适合规则方法；后者缺少清楚的正确边界。Topic Scope、Quality Requirements 和 Task Completion 也往往不是非黑即白。

模型之间存在特定偏差。GPT-4o 在 Form 上只有 67.0%，Ordering/Sequence 更低至 61.3%；Qwen3 在 Multi-turn Coherence 上达到 91.0%；gpt-oss 整体最均衡，但 Role Persona 仍然较弱。

## 6 结论

RubricEval 是首个面向指令遵循的 rubric-level meta-evaluation benchmark，覆盖四类指令并提供 Easy/Hard 子集。RAF 用于规模化生成高置信标签。实验表明，即使 GPT-4o、Claude-Sonnet-4.5 等常用 judge 也难以处理 Hard rubric。Rubric-level 优于 checklist-level，显式 reasoning 能提高准确率，二者结合还能提高不同 judge 之间的一致性。Rubric taxonomy 则揭示了具体失败模式，为后续 judge 开发和 benchmark 设计提供方向。

## 局限

1. RubricEval 只覆盖四类主要 instruction，未覆盖 agent 或领域专用指令。
2. RAF 依赖 LLM judges 和 reasoning models 生成参考标签。虽然与人工验证高度一致，仍可能含噪声；两个 meta-judges 无法达成共识的样本被丢弃，也可能排除了真正最难的案例。
3. 本文只研究最常见的 rubric-level 二值判断，没有覆盖 Likert 量表或 pairwise comparative judgment。

## 附录 A：四类 instruction 定义

- **Constrained**：单轮指令同时包含多条并行约束，如内容、格式和风格；judge 必须独立验证每条约束且不能漏项。
- **Compositional**：约束之间具有选择、链式、合取等逻辑依赖；judge 必须解析拓扑结构并将 rubric 对齐到 response。
- **Multi-turn**：约束跨多个对话轮次累积或变化；judge 需要跟踪上下文和跨轮指代。
- **System**：system prompt 在会话层定义角色、行为或限制；抽象角色遵循通常比具体 JSON 等格式限制更难判断。

## 附录 B：原始 instruction 与 rubric

数据来自 InfoBench-hard、ComplexBench、CFBench、AdvancedIF、StructFlowBench 和 SysBench，共 4,273 条 instruction、20,685 条 rubric，平均每条 instruction 4.84 条 rubric；所有 rubric 均为人工编写或人工验证。

## 附录 C：Rubric-based Evaluation

Rubric-based evaluation 已超出 instruction following，被用于医疗问答（如 HealthBench）、代码生成、摘要等任务。它把复杂整体质量拆成若干细粒度标准，让 LLM judge 分别验证，再聚合成总分。相比 response-level scalar，它更适合主观、多维任务，也提供更可解释的局部反馈和 partial credit，并已被用作训练监督或 reward。

但最终总分依赖每个原子判断的准确性；单条 rubric 的错误会经由聚合传播并污染下游应用。这正是本文要求 rubric-level meta-evaluation 的原因。

## 附录 D：人工集构造

人工参考集来自四个 judge 的分歧样本。两名标注员独立判断并讨论冲突。为扩大数据并保持正负平衡，对 True 样本让 GPT-4.1 最小修改 response 使其违反 rubric；对 False 样本则最小修改使其满足 rubric。所有改写都由人工再次验证。最终包含 253 组原始/改写对，共 506 个 judge instances，正负各 253。

## 附录 E–F：Rubric 聚类与 response 模型池

t-SNE 显示 Multi-turn Coherence、Quantity Limit、Format Structure 等类别形成较紧凑的簇，说明这些 rubric 类型内部存在一致模式。Response 生成模型池覆盖 Qwen、Llama、DeepSeek 等不同家族、参数规模、Dense/MoE 架构以及 Instruct/Thinking 模式。

## 附录 G–H：数据与评测协议分拆

RubricEval 的 3,486 个标签中，Constrained 684、Compositional 240、Multi-turn 1,094、System 1,468。Easy/Hard 上，rubric-level 与 reasoning 的总体优势保持一致；Hard 中所有协议都显著下降。

## 附录 I–L：来源与 taxonomy

来源 benchmark 包括 InfoBench、ComplexBench、CFBench、AdvancedIF、StructFlowBench 和 SysBench。四个 base judges 是 GPT-4.1、Claude-Sonnet-4.5、Gemini-2.5-Flash、DeepSeek-v3.2-exp。Rubric taxonomy 由 GPT-5.1 辅助分类；若来源 benchmark 已有类别，则将其作为提示而非直接照搬。

13 类 rubric 的典型例子包括：是否包含每个目的地的建议停留时间、是否完全避免字母 e、是否至少引用三条线索、是否按发布日期排序、是否保持友好语气、是否使用将来时、是否合并前两轮消息，以及是否符合指定 persona。

## 附录 M–N：案例与评测 prompt

RAF 案例表明，多 judge 理由加 meta-judge 仲裁有时比单个人类标注更客观。最终评测 prompt 要求 judge 只关注给定 rubric，先写简短理由，再严格输出 `YES` 或 `NO`；只有完整、明确满足时才判 YES，未满足或仅部分满足均判 NO。

## 参考文献

参考文献的作者、标题与出版信息保持原文形式，见同目录 [source.md](./source.md) 的 References 部分及 [paper.html](./paper.html)。
