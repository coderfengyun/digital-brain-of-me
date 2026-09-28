# Mira Murati新公司把桥水基金「祖传判断力」炼成AI！GPT、Gemini、Claude全部翻车，错误率暴降30%成本砍1/14

- 微信来源：https://mp.weixin.qq.com/s/qEnkqOhCA_1-eUUTN0DoLg
- 核心原始研究：https://www.bridgewater.com/aia-labs/learning-to-replicate-expert-judgment-in-financial-tasks
- 原始研究标题：Learning to Replicate Expert Judgment in Financial Tasks
- 作者：Sarah Su、Kevin Zhu、Emily Xiao、Rohan Alur、Daniel Kang（Bridgewater AIA Labs）
- 发布日期：2026-06-30

> 获取说明：微信页面可在 Chrome 中正常打开并确认标题，但自动化正文接口持续超时。因此本地来源以该文所报道的桥水 AIA Labs 原始研究为准，并用公开可访问的同题中文报道交叉核对。以下是原始研究正文的结构化摘录，不冒充微信原文逐字存档。

## Investor Judgement

Bridgewater AIA Labs 的目标是构建能够覆盖人类投资者全部活动、达到或超过专家表现的“人工投资者”。当所有投资者都能接触相同信息时，alpha 来自差异化判断与品位，而优秀投资者的判断通常难以清楚表达或直接传授。

文章选择投资分析师最简单、最日常的工作之一作为案例：过滤和处理金融文档，找出与投资决策相关的信息。真正耗费精力的并非阅读本身，而是遍布工作流的小判断：筛选、解释、分段，以及识别信号所在。

研究问题是：能否教会 LLM 金融“品位”？作者主张，专有的投资者判断标签，而不仅是公开金融文本，能够让模型学会这种品位。

## Frontier Model Performance

研究评估了六项来自投资者日常工作流的信息筛选任务，以投资者标签为标准计算准确率，分类任务还计算 F1。

仅给出任务描述时，Gemini、Claude、GPT 的多个版本平均准确率约为 50%。专家随后改写任务说明并调整分类方式；例如，小型 IPO 新闻虽与金融相关，却未必对宏观投资者“有趣”。人工及自动提示优化把准确率提升至 70% 中段，但最佳前沿模型仍低于团队设定的 80% 日常可信门槛。

## Dataset Construction

团队最初从供应商获得非专家标注数据，用它训练的模型仍表现不佳。检查推理轨迹后发现，许多标签本身就是错的。由于专家标注昂贵，团队设计了争议样本验证流程：先让模型学习带噪标签，再将模型判断与原标签不一致的样本交给专家复核，以集中使用专家时间。

## Training Recipe

团队使用 Thinking Machines Lab 的 Tinker 平台，在 Qwen3-235B 上训练。标准 GRPO 加重要性采样损失带来显著提升，但仍未达到 80%。随后加入三项改进：

1. 多任务交错批处理：按任务轮转 batch，相比完全混合 batch，准确率提高 12.1%。
2. 使用带非对称裁剪的 CISPO 损失：相比重要性采样基线，准确率提高 10.1%。
3. 强教师的 on-policy distillation：每 20 步仅在验证准确率创新高时把当前 checkpoint 升格为教师，相比冻结基座教师再提高 3.1%。

## Results and Conclusion

训练模型把平均准确率从最佳前沿模型的 78.2% 提升到 84.7%，即错误数量减少 29.8%；推理单任务成本降低 13.8 倍。桥水认为 84.7% 已足以用于其日常工作。

作者的结论是：前沿模型在简单金融判断任务上受限于公开训练数据，而高质量、由专家判断标注的专有数据，配合定制训练，可以在组织特定任务上得到更准确且更便宜的模型。这种“差异化智能”可能成为企业 AI 的重要形态。
