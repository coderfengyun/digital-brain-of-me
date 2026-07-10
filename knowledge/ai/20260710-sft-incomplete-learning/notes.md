# Why Supervised Fine-Tuning Fails to Learn

**类型**: 方法 / 系统实证  
**论文**: Why Supervised Fine-Tuning Fails to Learn: A Systematic Study of Incomplete Learning in Large Language Models  
**作者**: Chao Xue, Yao Wang, Mengqiao Liu, Di Liang, et al.  
**来源**: https://arxiv.org/abs/2604.10079  
**版本**: arXiv v4, 2026-04-24; ACL 2026 Main

---

## 🗺️ 全局地图

### 一句话摘要
这篇论文把 SFT 之后模型仍然答不对训练样本本身的现象定义为 Incomplete Learning Phenomenon (ILP)，并主张：这些未学会样本不是随机噪声，而来自五类不同根因，必须先做样本级诊断，再选择 CPT、冲突分桶、重采样或自适应 epoch 等对应干预。

### 段落分类

| 章节/段落 | 分类 | 一句话说明 |
|-----------|------|-----------|
| Abstract + Introduction | [核心] | 定义 ILP：SFT 收敛后，模型仍不能稳定复现一部分监督训练样本。 |
| Related Works | [连接] | 把 ILP 与 SFT 稳定性、数据质量、灾难性遗忘、machine unlearning 区分开。 |
| 3.1 Unlearned Sample Detection | [核心] | 用训练集回测、sample-level evaluation、一致性评估、robust detection 找出未学会样本。 |
| 3.2 Unlearned Sample Processing | [核心] | 建立五类归因：预训练知识缺口、基座与 SFT 冲突、SFT 内部冲突、left-side forgetting、训练不足。 |
| Table 1 / Table 2 | [核心] | 给出 CPT 与其他策略在 Qwen、LLaMA 上的主要效果。 |
| Appendix A-E | [支撑] | 展开五类归因的实验设置、算法和消融结果。 |
| Appendix F OLMo2 | [核心] | 用开放模型 OLMo2-7B 检验知识缺口/冲突，并暴露 CPT 对广义 benchmark 的负面 trade-off。 |
| Conclusion / Limitations | [核心] | 总结 ILP 的诊断价值，也承认冲突检测、外部知识质量、算力成本是主要局限。 |

### 结构地图

```
问题: SFT 收敛不等于训练样本被真正内化
↓
观察: 未学会样本在训练集回测中持续存在，且不是随机分布
↓
定义: ILP = post-SFT failure to internalize supervised instances
↓
诊断:
├─ Base model 缺少前置知识
├─ Base model 高置信错误与 SFT 标签冲突
├─ SFT 数据内部有相似输入/矛盾标签
├─ 顺序训练导致早期数据被覆盖，即 left-side forgetting
└─ 稀有/复杂模式没有得到足够优化
↓
干预验证:
├─ 知识缺口/基座冲突 → 检索外部知识 + CPT + SFT
├─ SFT 内部冲突 → 删除错误样本 + 冲突样本分桶
├─ 左侧遗忘 → 全局 shuffle + 动态重采样
└─ 训练不足 → progressive epoch increment + early stopping
↓
结论: SFT 需要从 aggregate performance 转向 sample-level learning diagnosis
```

---

## 📖 核心叙事 (Narrative)

作者反对一个常见默认假设：只要 SFT loss 收敛、整体 benchmark 变好，训练数据中的监督信号就已经被模型学会了。论文说，不是这样。模型会在自己的 SFT 训练集上仍然稳定答错某些样本，这些样本构成 ILP。

ILP 的关键不在“泛化失败”，而在“训练内化失败”。这点很重要：它不是 held-out set 上表现差，也不是 OOD，也不是灾难性遗忘，而是模型已经见过这些监督样本，训练后仍然没有把它们变成可稳定调用的能力或知识。

论文的框架是诊断优先。先用 post-SFT evaluation 找出 unlearned samples，再逐个问：这个样本是因为基座模型根本没有相关知识？还是基座有强但错误的 prior？是 SFT 标签之间互相打架？还是训练顺序让早期样本被后来的梯度覆盖？或者只是复杂/长尾样本训练轮数不够？

五类归因对应五类信号和干预：

1. **Base Model Knowledge Limitations**: 用 OpenIE 抽取样本中的 subject-predicate-object triplets，再用 BoN sampling 和 pass@N 探测基座模型是否掌握这些知识。若 pass@10 < 0.2 且 BoN-5 Acc < 0.1，就视为知识盲点。干预是检索 WikiData、Google Search、OpenAI-o1 等外部知识，构造增强语料，按 `0.8 general + 0.2 augmented` 做 continued pre-training，然后再 SFT。
2. **Conflicts Between SFT and Base Model**: 如果基座模型对错误答案有高置信度，就说明 SFT 监督信号与模型已有 prior 冲突。干预仍是定向知识增强和 CPT，用权威信息校准内部知识。
3. **Knowledge Conflicts Within SFT Data**: 如果相似样本有矛盾标签，模型接收到的监督信号本身不一致。论文用语义相似度找冲突对，再用 GPT/DeepSeek 判断正确性：错误样本删除，两个都合理但互斥的样本放入不同训练 bucket，避免同一 mini-batch 内互相干扰。
4. **Left-side Forgetting**: 在顺序或拼接式训练中，早期数据被后续数据覆盖。干预是全局 shuffle，加上动态重采样：每隔 K 步检查各数据子集准确率，若某子集下降超过阈值，就临时提高其采样权重。
5. **Insufficient Training**: 固定 epoch 对不同复杂度数据不合适。干预是 progressive epoch increment，从较小 epoch 起，每轮看 validation performance，继续涨到性能不再提升为止。

论文最好的一点，是把 mitigation 当作 causal intervention，而不是卖一个统一算法。比如 CPT 对知识缺口有效，但对顺序遗忘未必是核心解；分桶能处理内部冲突，但解决不了基座没有知识的问题。

---

## 📊 数据证据层 (Evidence)

| 论点 | 创新点 | 支撑数据 | 数据来源 | 说服力评估 |
|------|--------|----------|----------|------------|
| SFT 后仍存在训练样本级未学会现象，且来源异质 | 把 ILP 定义为训练内化失败，而非泛化失败 | 五类未学会现象占比：base knowledge limitations 18.7%，base/SFT conflicts 13.2%，SFT 内部冲突 14.1%，left-side forgetting 17.4%，insufficient training 14.6% | Table 10 | ⭐⭐⭐ 中强。分类清楚，但占比依赖作者的检测规则和 judge。 |
| 基座知识缺口不能靠单纯增加 SFT epoch 解决 | 用 pass@N/BoN 找盲点，再用 CPT 补知识 | MedQA 从 65.3 增加 SFT 到 10 epoch 仅到 66.8；CPT+SFT 到 82.1。TechFAQ 从 68.1 到 69.5，CPT+SFT 到 83.6 | Table 4 | ⭐⭐⭐ 强。对“多训几轮就行”的反例很有力。 |
| CPT 能缓解知识缺口和基座/SFT 冲突 | 把 CPT 作为诊断后的定向知识注入，而不是通用预训练 | 知识密集任务 CPT 后准确率普遍提升：Qwen-7B ARC 68.1→70.9，CommonQA 74.5→76.9，MedMCQA 61.2→63.7；论文正文称 domain benchmark 提升 9.4%-14.1% | Table 1, Section 4.1 | ⭐⭐⭐ 中强。方向一致，但主表与正文口径有差异，需要看实验配置。 |
| 高置信错误代表基座 prior 与 SFT 监督冲突 | 用错误答案 token 概率超过阈值标记 high-confidence error | 冲突率 CPT 后下降：LLaMA2-7B MedMCQA 15.2%→11.2%，Qwen-7B ARC 12.3%→8.8%，Qwen-14B MedMCQA 13.1%→9.6% | Table 6 | ⭐⭐⭐ 中强。能说明冲突减少，但阈值选择影响大。 |
| SFT 数据内部冲突应被隔离，而不是粗暴删除 | 错误样本删除，合理但冲突样本动态分桶 | 完整策略优于 deletion/grouping 单项：Qwen-7B 82.3%→85.1%；仅 deletion 到 83.8，仅 grouping 到 84.5。LLaMA-13B 83.6%→86.5% | Table 8 | ⭐⭐⭐ 强。消融支持“保留有价值冲突样本”的判断。 |
| left-side forgetting 主要伤害早期训练数据 | 全局 shuffle + 动态重采样按准确率下降补样 | 第一段 10% 数据 ROUGE-L 从 0.41→0.53，增益 +29%；中段 +3.5%；最后 10% 轻微下降 -1.6% | Table 11 | ⭐⭐⭐ 中强。现象直观，但是否普遍依赖数据拼接方式。 |
| CPT 对开放模型可能牺牲广义 benchmark | OLMo2-7B 实验展示 targeted knowledge injection 的副作用 | OLMo2 SFT 数据与 Dolma 的总体 non-existence rate 19.3%，conflict rate 14.5%；CPT 后 MMLU -3.5%，AGIEval -2.9%，GPQA -6.8%，MMLU-Multi -8.1% | Table 13, Table 14 | ⭐⭐⭐ 强。这个负结果很重要，防止把 CPT 神化。 |

---

## 🤔 批判性思考 (Critical Thinking)

| 问题 | 分析 |
|------|------|
| 核心假设及失效场景 | 假设: 未学会样本可以被可靠地归因到五类机制，并且对应干预的提升能反证该归因。<br>失效场景: 多个机制同时存在时，单一归因可能过于干净；比如一个样本既有知识缺口，也有标签冲突，还可能是长尾复杂样本。 |
| 关键局限 | - 检测链条依赖 OpenIE、语义相似度、GPT/DeepSeek judge、外部检索质量，误差会层层传递。<br>- CPT 的成本很高，对小团队并不一定现实。<br>- OLMo2 结果显示 CPT 会伤害 broader benchmark，说明“补知识”不是免费午餐。<br>- 文中部分数字口径不完全统一，例如正文提到 9.4%-14.1% 的 domain benchmark 提升，而 Table 1 展示的是若干 +1.6 到 +2.8 的准确率点提升，需要核查实验表对应的是不同任务/设置。 |
| 实验充分性 | 论文覆盖 Qwen、LLaMA、OLMo2 和多个领域，范围不错；最有价值的是把负结果也放出来。但还缺少更细的 ablation：不同 CPT 语料比例、不同 high-confidence threshold、不同 judge、不同 batch bucket 数、不同数据顺序下 ILP 占比是否稳定。 |

---

## 对我有用的启发

1. SFT 评估不该只看 validation/benchmark，总要加一个 **training-set replay audit**：训练完以后回测训练样本，找“见过但没学会”的子集。
2. 未学会样本要进入一个诊断队列，而不是统一丢给“多训几轮”。尤其是知识缺口和数据冲突，继续 SFT 大概率只是在浪费梯度。
3. 对 agent/skill/harness 系统也有类比：如果一个 agent 在少数示例上反复失败，要先判断是知识缺失、规则冲突、示例互相矛盾、上下文顺序覆盖，还是训练/提示暴露不足。
4. CPT 的副作用提醒很重要：把局部知识修正塞进模型内部，可能破坏广义能力；很多场景下，RAG/工具/记忆层也许比继续预训练更可控。

## 读后判断

这篇最值得拿走的不是某个算法，而是一个评估视角：**SFT 的失败单位应该从平均指标下沉到样本级学习状态**。如果把模型训练看成“把监督数据压进参数”，ILP 说明压进去的过程并不均匀，某些知识会被挡住、抵抗、冲突、覆盖或遗漏。

我对论文的信任程度是“方向很强，实证有启发，但工具链需要复核”。尤其是用外部 judge 做知识存在/冲突判断，会让诊断框架很有用，也会让它脆弱。真正落地时，我会保留这套 taxonomy，但把每类检测做成可审计的 artifact，而不是只信一个自动标签。
