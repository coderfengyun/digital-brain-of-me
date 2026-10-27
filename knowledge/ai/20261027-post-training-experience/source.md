# Post-Training 变革（上）：2026 年，真正稀缺的已经不是数据，而是“可学习的经验”

- 作者/公众号：Jason的算法日志
- 发布时间：2026-08-23 21:08
- 发布地：北京
- 原文：https://mp.weixin.qq.com/s/py2IXm2Qe23gCZYEKnd9Pw
- 本地获取：2026-10-27，通过 Codex 内部浏览器可访问性快照提取

> 说明：正文中的公式在微信可访问性快照中未完整呈现；头图记录为“2024—2026 Post-Training 范式演进”。正文引用到〔10〕，但页面末尾可见引用列表只显示〔1〕—〔9〕。

2025 年我们的判断是：数据要高质量、多样化、适配 base model，并与 RL 形成闭环。这个判断没有错，但还不够。2026 年行业真正发生的变化，是“数据”的定义变了——从 prompt-response，变成环境中的状态、动作、反馈与完整轨迹。

## 一、原来的五阶段判断仍然成立，但已经解释不了 2026

通用 post-training 的数据工作，过去几年大致经历了五个阶段。

1. **数据积累**：SFT 数据稀缺时，加量本身就能涨点。ShareGPT、用户日志、强模型蒸馏成为主要来源。
2. **质量与多样性**：量级到达天花板后，重复数据开始浪费训练预算，覆盖与质量成为主要矛盾。
3. **专项合成**：数学、创作、指令遵循、function calling 各自建立数据 workflow。
4. **Model-oriented 筛选**：数据不再被视为绝对的好或坏，而要看它对当前 base model 是否有学习价值。
5. **与 RL 联动**：模型采样、verifier 打分、筛选和继续训练形成循环，SFT 与 RL 的边界开始模糊。

Self-Instruct、Evol-Instruct、WebInstruct 代表了早期的合成范式：从种子任务出发，生成更复杂的指令与回答，再做过滤。IFD、LESS、MoDS、DEITA 则把问题推进到“哪些样本更值得当前模型学习”。到 2025 年 8 月，这条路线已经相当成熟。但它仍然默认一件事：训练数据的基本单位是一条问答。

2026 年，训练对象越来越像一条轨迹。其中 `s_t` 是模型看到的状态，`a_t` 是回答、思考或工具动作，`o_{t+1}` 是环境返回的观察。一条数据好不好，不再只看 prompt 是否复杂、response 是否优雅，而要回答：环境是否真实，状态是否覆盖生产任务，工具反馈是否可信，失败是否可以复现，整条轨迹能否验证。

这就是 2026 年通用 post-training 的第一条共识：**数据工程正在变成环境工程。**

## 二、2026 年已经形成的五条共识

### 共识一：Pre-training 决定模型的能力底座，post-training 决定能力如何被调用

OpenAI 的 reasoning 路线已经证明，增加 RL train-time compute 与 test-time compute，可以显著改变模型解决问题的方式。Qwen3 则把长 CoT 冷启动、reasoning RL、思考模式融合和通用 RL 串成四阶段流程。行业不再把 post-training 理解成“让回答更礼貌”，而是把它看成能力路由器与行为塑形器。〔1〕〔2〕

### 共识二：训练单元从 response 升级为 trajectory 和 session

Silver 与 Sutton 把这一变化称为“经验时代”：未来 agent 不应只处理短对话，而要生活在持续的经验流中，行动、观察环境后果，并根据长期目标调整策略。Kimi K3 已经把 million-token agentic RL、持久 rollout 和 sandbox state 写进技术报告。〔3〕〔4〕

### 共识三：Environment 和 verifier 比换一个 RL 算法更稀缺

数学题有标准答案，代码可以运行测试；但写作、研究、经营、医疗问诊怎样形成低成本且不易被 hack 的 reward？这是今天最难的部分。Qwen3-Coder 把“hard to solve, easy to verify”作为大规模 Code RL 的核心，并建设两万个并行环境；GLM 的 slime 系统则让数学、代码、sandbox、verifier 和长程环境像数据源一样接入训练流。〔5〕〔6〕

### 共识四：SFT、RL、蒸馏不再是单向流水线，而是循环

模型先用少量 SFT 学会协议，再通过 RL 探索；成功轨迹经过 rejection sampling 或教师修正后重新进入训练；On-Policy Distillation 又让教师在学生真正访问到的状态上给出分布。数据、policy 与教师同步更新，已经比“SFT 做完再交给 RL 团队”更符合实际。〔7〕

### 共识五：安全数据必须覆盖 agent 环境，聊天数据不能自然泛化过去

Anthropic 复盘 Claude 4 时发现，大多数 alignment training 仍是没有工具使用的标准聊天 RLHF，这对聊天模型曾经够用，却不足以覆盖 agentic tool use。后来他们把 constitutional documents、高质量对话和多样环境共同纳入训练，并明确强调：只训练正确动作不够，还要教模型为什么某种行为更好。〔8〕

## 三、最大的非共识：堆更多环境，还是解决真正的泛化

2026 年最重要的争论，并不是 PPO、GRPO、GSPO 谁更好，而是：**不断增加 RL 环境，究竟是在提升通用智能，还是在建设一套更隐蔽的题库？**

Silver 与 Sutton 的观点相当鲜明。他们认为人类数据存在天然上限，未来能力将来自 agent 与环境交互产生的经验；reward 也应更多来自现实后果，而不是人类在结果发生前做出的偏好判断。健康指标、实验结果、代码测试、成本与收益，都可以成为 grounded reward。〔3〕

Ilya Sutskever 的警告则直指当前实践的软肋。他认为模型在 benchmark 上很强、进入真实工作却表现“锯齿化”，核心是可靠泛化不足。他特别提到，公司的团队不断生产新的 RL environments，而这些环境很容易受到 eval 启发。结果可能是模型对评测越来越熟练，却没有学会跨场景的判断力。〔9〕

这两种观点并不完全矛盾：

- Silver/Sutton 回答的是：下一代数据从哪里来？答案是环境经验。
- Ilya 追问的是：这些经验为什么能泛化？仅仅扩大环境数量，并不能自动给出答案。

因此，更准确的判断是：环境扩张是必要条件，但不是充分条件。真正的通用 post-training 不能只追求 environment count，还要追求环境之间可迁移的结构。

一个环境如果只是在替换数字、变量名和 UI 皮肤，数量再大仍可能是同一道题。相反，如果一组环境覆盖了计划、验证、恢复、权限冲突、信息不足和长期目标，它们才更可能训练出可复用的策略。

可以把环境价值粗略写成一项由环境与 verifier 质量 `Q`、对当前 policy 的新颖性 `N`、向其他任务迁移的潜力 `T`，以及 reward hacking 和评测泄漏风险 `H` 共同决定的量。原网页中的具体公式未被可访问性快照提取出来。

## 四、头部公司已经怎样落地：不是一条 recipe，而是一套系统

2026 年几份技术报告给出的信号非常一致：头部团队开始把 post-training 当成一套长期运行的“能力工厂”。

| 团队 | 对 2026 最有代表性的实践 | 真正说明了什么 |
|---|---|---|
| GLM-5.3 | 沿用 GLM-5.2 的 base model，能力提升全部来自 post-training；继续增加环境、任务多样性和训练计算 | 同一个 base 上，post-training 已能成为主要能力增量来源 |
| Kimi K3 | 在 general、coding、agentic domain 上联合 RL；支持百万 token 轨迹、持久 rollout 与 sandbox state | 长程 RL 的瓶颈是状态与环境连续性，不只是上下文长度 |
| DeepSeek-V4 | 为 agent 长上下文设计高效注意力、专用工具 token 与 DSec sandbox | 架构、推理成本和 RL 环境必须协同设计 |
| Qwen3-Coder | 将真实代码任务放入两万个并行环境，以执行反馈做长程 Agent RL | 环境并行度和自动验证决定 rollout 是否能够规模化 |
| Anthropic | 从聊天 RLHF 扩展到原则文档、高质量 reasoning 和多样环境；强调“教为什么” | 对齐不是复制正确动作，而是学习能跨环境迁移的原则 |

其中最值得重视的是 GLM-5.3 的表述：他们没有换 base model，“所做的就是扩大 post-training”。这不是说 pre-training 不重要，而是说明在一个足够强的底座上，环境、任务组合和 RL compute 已经能够产生显著的新能力。〔6〕

田渊栋对 2025 年 LLM RL 一线问题的总结也很接近这个结论：真正进入核心训练后，遇到的是 RL stability、training-inference interaction、架构、长上下文、数据生成和 RL infra 的联动，而不是某个孤立算法。〔10〕

换句话说，2026 年不存在一条所有团队照抄都有效的“神奇 recipe”。存在的是一组越来越稳定的工程共识：**先建设可验证环境，再建设大规模 rollout；先保证训练与推理一致，再讨论优化器收益。**

## 五、一套可以实际落地的通用 Post-Training 数据栈

如果今天重新建设数据体系，我会把它拆成六层。

### 第一层：Base capability map

不要先问“我们有什么数据”，而要先测模型在不同任务、难度和工具条件下的成功分布。除了 pass@1，还要保留 pass@k、错误类型和失败轨迹，区分“模型不会”与“模型会但采不到”。

### 第二层：Bootstrap SFT

用少量高质量数据让模型掌握输出协议、工具 schema、基本安全边界和最低任务能力。目标不是把答案模式训死，而是让模型具备进入环境探索的资格。

### 第三层：Environment registry

每个环境都应保存任务模板、状态空间、动作空间、工具权限、终止条件、可验证信号、难度参数和版本。环境必须能够重放，否则 reward 漏洞无法定位。

### 第四层：Verifier stack

优先级通常是：程序化验证 > 执行结果 > 领域规则 > 独立模型 judge > 人工复核。对高风险任务，最终安全条件应使用 veto 或硬约束，不能与其他分数简单平均。

### 第五层：Policy-oriented sampler

样本价值必须相对当前 policy 计算。已经稳定解决的任务降低采样权重；完全无法探索的任务先通过教师轨迹、课程学习或子任务拆解降难度；最有价值的是当前模型“偶尔成功、但尚不稳定”的区域。

### 第六层：数据血缘和回归评测

保存 policy、环境、工具、verifier 和教师版本，记录每次能力上涨来自哪一类经验。上线前用独立环境做 OOD、reward hacking、指令层级、成本和长程稳定性测试。

这套体系的最终产物不再是一个静态 SFT 数据库，而是一个持续运行的闭环：

> 评测发现缺口 → 生成或选择环境 → policy rollout → verifier 评分 → RL/蒸馏更新 → 独立回归 → 重新进入评测。

2026 年的共识不是“数据不重要了”，恰恰相反：数据的重要性从未如此之高。只是现在最有价值的数据，已经不是别人写好的答案，而是模型在真实约束下行动后留下的、可验证的经验。

## 引用资料

1. OpenAI，《Learning to reason with LLMs》。
2. Qwen Team，《Qwen3: Think Deeper, Act Faster》。
3. David Silver、Richard S. Sutton，《Welcome to the Era of Experience》。
4. Kimi Team，《Kimi K3: Open Frontier Intelligence》。
5. Qwen Team，《Qwen3-Coder: Agentic Coding in the World》。
6. Z.ai，《GLM-5.3: Frontier Coding with Emergent Cyber Capabilities》。
7. Thinking Machines Lab，《On-Policy Distillation》。
8. Anthropic，《Teaching Claude why》。
9. Ilya Sutskever，《We're moving from the age of scaling to the age of research》。

> 注：正文出现〔10〕，但原网页末尾可见的引用列表未显示对应条目。
