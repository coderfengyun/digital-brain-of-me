# Post-Training 变革（上）：从“数据”到“可学习经验”

**类型**: 综述  
**作者/公众号**: Jason的算法日志  
**原文日期**: 2026-08-23  
**阅读日期**: 2026-10-27  
**原文**: [微信公众号文章](https://mp.weixin.qq.com/s/py2IXm2Qe23gCZYEKnd9Pw)

---

## 🗺️ 全局地图

### 一句话摘要

> 通用 post-training 的核心资产正在从静态问答数据迁移到可重放、可验证、针对当前 policy 产生的环境经验；但环境数量只有在覆盖可迁移结构、避免评测泄漏并保留完整血缘时，才能转化为真实泛化能力。

### 段落分类

| 章节/段落 | 分类 | 一句话说明 |
|-----------|------|-----------|
| 原来的五阶段判断 | [连接] | 回顾从数据积累、质量、多样性、专项合成到 model-oriented 筛选和 RL 联动的演化 |
| 数据工程变成环境工程 | [核心] | 训练基本单位由 prompt-response 变为 state-action-observation 组成的 trajectory |
| 五条行业共识 | [核心] | 总结能力塑形、长程轨迹、环境与验证器、训练闭环、agent 安全五个变化 |
| 堆环境与真正泛化的争论 | [核心] | 环境经验是未来数据来源，但环境数量本身不能保证迁移能力 |
| GLM、Kimi、DeepSeek、Qwen、Anthropic 案例 | [支撑] | 用头部实验室的一手材料展示工程路线正在汇合 |
| 六层 Post-Training 数据栈 | [核心] | 作者提出从能力地图到独立回归测试的一套能力生产系统 |
| 引用资料 | [支撑] | 提供主要出处，但正文〔10〕缺失，DeepSeek 一行也缺少明确对应引用 |

### 结构地图

```text
旧范式：高质量、多样、适配 base model 的 prompt-response 数据
↓
新观察：agent 的能力表现发生在连续状态、工具动作和环境反馈中
↓
对象变化：response → trajectory / session
↓
稀缺资源变化：答案数据 → 环境、verifier、可重放状态与数据血缘
↓
训练流程变化：SFT → RL → rejection sampling / 教师修正 → 蒸馏 → 再训练
↓
核心争议
├─ 经验派：与环境交互产生的 grounded experience 是下一代能力来源
└─ 泛化派：评测启发的环境可能只是更隐蔽的训练题库
↓
作者结论：建设六层环境数据栈，并用独立 OOD 回归约束闭环
```

---

## 📖 领域全景

### 发展脉络

```text
阶段 1：数据积累
SFT 数据稀缺，增加问答样本就能提升能力
↓
阶段 2：质量与多样性
去重、覆盖、难度与质量开始比单纯规模更重要
↓
阶段 3：专项合成
数学、代码、写作、工具调用各自形成数据流水线
↓
阶段 4：面向当前模型筛选
样本价值取决于当前 base/policy 会什么、缺什么，而非固定质量分
↓
阶段 5：数据与 RL 联动
模型采样、验证器评分、筛选、继续训练形成循环
↓
当前：环境工程
任务、状态、动作、工具、终止条件、verifier、快照和版本共同构成训练资产
```

文章最有价值的概念移动，是把“数据”拆成三个层次：

1. **环境定义**：规定模型身处什么世界，可以观察什么、执行什么，以及怎样结束和评分。
2. **任务实例**：给环境填入具体初始状态、目标、约束、随机种子和难度。
3. **经验轨迹**：记录某个 policy 在这个实例上的完整状态、动作、观察、奖励和终态。

这样一来，训练样本不再只是一条最终答案。模型打开了哪个文件、调用了什么工具、遇到什么报错、是否恢复、验证器为何给分，都会成为可学习和可审计的信息。

### 五条共识的准确含义

**1. Post-training 是能力路由与行为塑形。** 强 base model 提供潜在能力；post-training 决定模型遇到问题时是否分解、验证、调用工具、花费更多推理计算，以及遵守何种行为边界。它不能凭空补上 base model 从未学过的世界知识，因此“决定能力如何调用”比“创造全部能力”更准确。

**2. 训练单元扩展为 trajectory/session。** 对 agent 来说，最终答案无法解释成功来自计划、工具、恢复还是偶然命中。长程轨迹保留因果上下文，允许逐步信用分配、失败诊断和行为蒸馏。

**3. 环境和 verifier 成为系统瓶颈。** 数学和代码容易获得程序化反馈；研究、经营、医疗和开放写作的目标多维、延迟且容易被代理指标替代。RL 优化器再强，也只会更有效地追逐它收到的 reward。

**4. SFT、RL、筛选和蒸馏形成循环。** 先用 SFT 教会协议，再让 policy 探索；成功轨迹可经 rejection sampling 回流为示范，教师也可在学生真正访问到的状态上提供 token 级分布。训练数据会随 policy 一起变化。

**5. Agent 安全必须在 agent 环境中训练和评估。** 聊天偏好数据缺少工具权限、跨步后果、提示层级冲突和不可逆操作。安全训练需要覆盖这些状态，并解释原则为何成立，才能提高跨环境迁移的机会。

---

## 🗂️ 方法分类

| 类别 | 代表工作 | 核心思路 | 优势 | 局限 |
|------|----------|----------|------|------|
| Bootstrap SFT | Qwen3 长 CoT 冷启动；工具协议示范 | 用少量高质量轨迹让模型掌握格式、工具 schema 和最低能力 | 启动稳定、便于控制行为 | 容易模仿表面模式，覆盖不了探索产生的新状态 |
| 可验证环境 RL | Qwen3-Coder；Kimi K3 | 在可执行环境中 rollout，以测试、工具反馈和终态评分学习 | reward 相对客观，可扩展到长程任务 | 环境昂贵；容易把测试漏洞学成策略 |
| Rejection sampling / 轨迹回收 | 多次采样后由 verifier 选出成功轨迹，再用于 SFT 或蒸馏 | 将当前 policy 偶尔做到的成功行为固化下来 | 简单、并行友好，可快速提高成功模式密度 | 丢掉失败中的信息；验证器偏差会被放大；可能只学到幸存者轨迹 |
| On-policy distillation | Thinking Machines Lab | 教师对学生实际访问到的状态给出分布，而非只教离线答案 | 降低离线分布偏移，提供稠密训练信号 | 依赖强教师和高推理成本；教师错误会传递 |
| 原则与原因训练 | Anthropic “Teaching Claude why” | 不只给正确动作，还给行为原则、理由和多样环境 | 更可能跨任务迁移，适合安全边界 | 原则之间可能冲突；真实工具行为仍需环境验证 |
| 独立 OOD 回归 | 作者提出的第六层 | 用未参与训练的环境族测试泛化、reward hacking、成本和长程稳定性 | 能识别“刷题式进步” | 必须严格隔离；长期维护成本高 |

### Rejection sampling 在本文闭环中的位置

这里的 rejection sampling 不是经典概率论中用提议分布精确采样目标分布的那套推导，而是一种工程筛选流程：

```text
同一任务生成多条轨迹
↓
verifier 检查结果、约束和过程
↓
拒绝失败或低分轨迹，保留高质量轨迹
↓
作为下一轮 SFT / 蒸馏数据，或与 RL 继续交替
```

它把“偶尔成功”转成更密集的正例，但不能替代 RL。若只保留成功样本，模型看不到失败为何发生，也可能从验证器漏洞中选择出看似高分的坏轨迹。成熟系统还应保存失败分类、reward 分解和人工争议样本。

---

## 📊 数据证据层

| 论点 | 创新点 | 支撑数据/例子 | 数据来源 | 说服力评估 |
|------|--------|---------------|----------|------------|
| Post-training 已从简单偏好对齐扩展到系统性推理与 agent 能力塑形 | 四阶段而非单次 SFT/RL | Qwen3 官方材料列出长 CoT 冷启动、reasoning RL、思考模式融合、通用 RL；通用 RL 覆盖 20 多类任务 | [Qwen3 官方博客](https://qwenlm.github.io/blog/qwen3/)；[OpenAI o1 研究](https://openai.com/index/learning-to-reason-with-llms/) | ⭐⭐⭐⭐ 强：流程有一手材料；“能力路由器”仍是作者的概括，不是独立定律 |
| 长程 agent 训练需要持续状态与环境 | 从单轮 response 转向 session | Kimi K3 报告 1M context，并描述 million-token agentic RL、persistent rollout 和 sandbox state | [Kimi K3 论文](https://arxiv.org/abs/2607.24653)；[官方仓库](https://github.com/MoonshotAI/Kimi-K3) | ⭐⭐⭐⭐ 强：具体基础设施可核验；尚不能单独证明所有任务都需要百万 token |
| 环境并行与自动验证使 agent RL 规模化 | 将真实代码任务放入大量独立环境 | Qwen3-Coder 官方称并行运行 20,000 个独立环境，用环境反馈训练长程规划与工具使用 | [Qwen3-Coder 官方博客](https://qwenlm.github.io/blog/qwen3-coder/) | ⭐⭐⭐⭐ 强：规模数字明确；效果和成本主要由团队自报 |
| 同一 base 上，扩大 post-training 可带来显著能力增量 | 控制 base 不变后扩环境、任务和计算 | GLM-5.3 官方称沿用 GLM-5.2 base，“Scaling post-training is all we did” | [Z.ai GLM-5.3](https://z.ai/blog/glm-5.3) | ⭐⭐⭐ 中强：对“同 base”很直接；基准收益缺少独立复现，不能外推为普遍比例 |
| SFT、RL、蒸馏可以形成 policy-relative 循环 | 教师在学生实际状态上给稠密信号 | On-Policy Distillation 从学生采样轨迹，由教师为每个 token/state 评分；官方报告 AIME 2024 达 70%，计算效率较外推 SFT 高 9–30 倍 | [Thinking Machines Lab](https://thinkingmachines.ai/blog/on-policy-distillation/) | ⭐⭐⭐ 中强：支持 on-policy 蒸馏本身；不能单独证明文章提出的整套闭环已成为行业标准 |
| 聊天 RLHF 不能自然覆盖 agent 安全 | 训练理由与原则，并扩大环境分布 | Anthropic 回顾 Claude 4 训练时指出，大部分 HHH 数据是没有 agentic tool use 的标准聊天 RLHF；加入理由和多样环境后泛化更好 | [Anthropic “Teaching Claude why”](https://www.anthropic.com/research/teaching-claude-why) | ⭐⭐⭐⭐ 强：问题、干预和局限均有披露；结论仍来自单一实验室和特定评测 |
| 更多环境不等于更强泛化 | 区分经验来源与经验可迁移性 | Silver/Sutton 提出持续经验和 grounded reward；Ilya 则警告 eval-inspired RL environments 可能造成隐藏题库和锯齿化表现 | [The Era of Experience](https://storage.googleapis.com/deepmind-media/Era-of-Experience%20/The%20Era%20of%20Experience%20Paper.pdf)；[Ilya 访谈](https://www.youtube.com/watch?v=aR20FWCCjAs) | ⭐⭐ 中：是关键理论争论，但主要是立场和现象总结，缺少跨实验室的受控定量比较 |
| 六层数据栈可以作为通用 post-training 架构 | 把能力地图、环境、验证、采样和血缘放入同一闭环 | **例子**：环境 registry、policy-oriented sampler、独立 OOD 回归 | 本文作者综合 | ⭐⭐ 中：工程上合理，尚不是经过统一 benchmark 验证的行业标准 |

### 证据边界与引用问题

- 文章把技术报告、实验室博客、访谈判断和作者自己的系统设计放在同一叙事中。它们适合构成趋势判断，但证据等级不同。
- 头部公司材料能证明“这些系统已经被建设”，不能单独证明某个组件是能力提升的唯一原因。大部分案例缺少环境数量、计算量、数据质量的受控消融。
- DeepSeek-V4 官方页面可以核验 1M context、高效注意力与 agent integration，但本文表格中“专用工具 token 与 DSec sandbox”的具体组合没有在文末给出明确引用，因此不宜视为已完整核实。
- 正文引用到〔10〕并把它用于田渊栋的 RL 工程总结，但页面可见参考资料只有〔1〕—〔9〕。这是一处应补齐的来源缺口。
- 原网页中环境价值公式未被内部浏览器的可访问性快照完整提取，只能确认变量涉及质量 `Q`、新颖性 `N`、迁移潜力 `T` 与风险 `H`，不应恢复或猜测具体运算形式。

---

## 🔮 开放问题与趋势

1. **怎样度量环境的结构多样性？** 环境数量容易统计，但换数字、变量名和界面皮肤可能仍是同一种任务。需要按计划结构、反馈延迟、权限冲突、故障恢复和信息缺失等机制划分环境族。
2. **怎样证明经验可以跨环境迁移？** 最有价值的测试不是同模板新实例，而是留出完整环境族，观察策略是否迁移到新的工具、界面和目标组合。
3. **怎样防止 verifier 被优化穿透？** 应保存 reward 分项、构造对抗轨迹、设置硬性 veto，并用与训练 verifier 独立的审计器检查 Goodhart 效应。
4. **失败轨迹怎样进入学习？** Rejection sampling 偏向成功样本；超时、循环、误用权限、错误恢复和“接近成功”的轨迹需要单独分类，才能训练诊断和恢复能力。
5. **怎样分配 rollout 预算？** 当前 policy 已稳定解决的任务回报低，完全不会的任务又没有可学习信号。采样器应寻找成功率居中、学习进展最快且有迁移价值的区域。
6. **怎样保存足以复现的状态？** 工具和外部服务会变化。真正的重放可能需要容器镜像、依赖锁、网络响应、随机种子、数据库快照和时间语义，而不只是一份 prompt。
7. **安全原则怎样处理现实冲突？** 帮助性、用户授权、隐私、可逆性和组织政策会在长程任务中冲突。原则训练仍要配合权限系统、人工升级路径和真实后果评测。

---

## 🤔 批判性思考

| 问题 | 分析 |
|------|------|
| 核心假设及失效场景 | 文章假设环境中的经验具有可学习结构，verifier 与真实目标基本一致，且环境可以保真重放。若 reward 只是代理指标、环境由 benchmark 反推、真实外部状态无法复现，或者训练 policy 已学会识别环境模板，闭环会稳定地产生高分但不可迁移的策略。开放研究、长期经营和医疗决策还存在数月乃至数年的延迟结果，很难直接获得 grounded reward。 |
| 关键局限 | ① 这是一篇趋势综述，不是受控实验；② 多项证据来自厂商自报，环境规模、训练计算与结果同时变化，因果贡献不清；③ “行业共识”没有明确调查口径；④ 六层栈是作者提出的工程框架，尚未和替代架构比较；⑤ DeepSeek 一行、正文〔10〕及环境价值公式存在来源或提取缺口；⑥ 文章强调成功经验，较少讨论失败轨迹、人工反馈成本和环境维护成本。 |
| 证据是否充分、如何证伪 | 现有材料足以支持“头部团队正在扩建环境化 post-training 系统”，还不足以证明“环境与 verifier 普遍比算法更稀缺”或“更多可验证经验必然带来通用泛化”。更强证据应固定 base、训练计算和优化器，分别改变环境数量、结构多样性、verifier 质量与重放保真度；测试集应留出完整环境族，并报告迁移、成本、安全、校准和 reward hacking。若同等预算下环境规模扩大却不提升跨族任务，或随机表面多样性和结构多样性效果相同，文章的核心判断就需要修正。 |

### 我的判断

文章最强的贡献是一套有用的数据库视角：**post-training 的关键资产不再是一堆“正确答案”，而是一组保留因果上下文的实验记录。** 每条记录都要知道模型处于什么状态、具有什么权限、采取了什么动作、环境返回什么、为何得分，以及这套环境和验证器是哪一版。

我会把“可学习的经验”再收紧一步：真正稀缺的不是经验本身，而是**因果上下文、验证依据和来源血缘都完整的经验**。缺少上下文，成功轨迹无法解释；缺少 verifier，经验无法筛选；缺少版本和重放，reward 漏洞无法定位；缺少独立测试，环境就可能退化成隐藏题库。

作者关于环境数量与泛化的自我质疑尤其重要。环境工程如果只追求并行度和 episode 数，很容易把数据规模时代的问题重新复制一遍。更好的单位不是“多少个环境”，而是“覆盖了多少种可迁移的决策结构，以及这些结构在多少个未见环境族上成立”。

### 一个可审计环境的最小示例

```yaml
environment:
  id: repo-bugfix
  version: 1.3.0
  image_digest: sha256:...
  task_template: "修复仓库中的指定故障，并保持测试通过"
  state_space:
    - repository_snapshot
    - terminal_history
    - changed_files
    - test_results
  action_space:
    - read_file
    - edit_patch
    - run_command
  tool_permissions:
    network: false
    writable_paths: ["/workspace"]
  termination:
    success: "hidden_tests_pass"
    failure: ["step_limit", "timeout", "policy_violation"]
  verifier:
    id: repo-tests
    version: 2.1.0
    signals: ["public_tests", "hidden_tests", "lint", "policy_checks"]
  difficulty:
    changed_modules: 2
    hidden_failures: 3
  replay:
    random_seed: 18427
    fixture_snapshot: fixtures-v8
```

这个 manifest 只定义环境。一次可复现实验还应另存任务实例、`trace.jsonl`、工具输出、终态快照、reward 分解，以及 policy、教师和 verifier 的版本。这样才能回答“模型为什么成功或失败”，而不只是留下一个总分。

