# Extreme Harness Engineering for Token Billionaires

**类型**: 叙事
**嘉宾**: Ryan Lopopolo（OpenAI Frontier Product Exploration）
**主持**: swyx（Latent Space）、Vibhu
**来源**: Latent Space Podcast + Substack
**视频**: https://www.youtube.com/watch?v=CeOXx-XTYek （72 分钟）
**原始博文**: https://openai.com/index/harness-engineering/
**日期**: 2026-04-08

---

## 🗺️ 全局地图

### 一句话摘要
> OpenAI Frontier 团队的 Ryan Lopopolo 讲述了他们如何在五个月内用零人类手写代码构建了一个百万行级别的 Electron 产品，并由此发展出 harness engineering 方法论和 Symphony 多 agent 编排系统——核心理念是：当 agent 犯错时，不要试图让它"更努力"，而要问"缺了什么 context、能力或结构"。

### 段落分类

| 章节（视频时间戳） | 分类 | 一句话说明 |
|-----------|------|-----------|
| 0:00 Introduction | [连接] | Ryan 背景介绍：Snowflake/Brex/Stripe/Citadel → OpenAI Frontier |
| 2:47 Zero Code Experiment | [核心] | 五个月零人类代码实验的起源和约束 |
| 3:46 Model Upgrades & Build Systems | [支撑] | 从 Codex Mini 到 GPT-5.4 的模型代际变化和 build 系统演进 |
| 6:02 One Minute Build Loop | [核心] | 构建时间必须 < 1 分钟的铁律 |
| 7:46 Humans as Bottleneck | [核心] | 人类成为瓶颈 → 系统思维 → 可观测性 |
| 8:19 Agent Code Review & Autonomous Merging | [核心] | 从人类 review 到 agent review 到 post-merge review 的演进 |
| 11:28 Docs, Skills, Guardrails | [核心] | 用文档、技能、质量分数编码工程品味 |
| 15:19 Autonomous Merging Flow | [支撑] | 完整的 PR 自动化生命周期 |
| 17:00 Agent-Legible Software | [核心] | 软件需要为模型的可读性而写，不只是人类 |
| 23:47 Encoding Requirements | [核心] | 把非功能性需求变成 prompt inject agent 的方式 |
| 25:57 Inlining Dependencies / Ghost Libraries | [核心] | Brett Taylor 回应：依赖会消失；Ghost Library 概念 |
| 29:36 Spec-Driven Software & Symphony 起源 | [核心] | 用 spec 分发软件，agent 从 spec 重建系统 |
| 32:46 Symphony: Terminal-Free Orchestration | [核心] | Elixir 编排层，移除人类终端操作 |
| 36:30 Multi Human Chaos | [支撑] | 多人多 agent 的协调挑战 |
| 39:35 Standardizing Skills and Code | [支撑] | 6 个技能统一全团队的 agent 行为 |
| 40:39 Self Improvement via Logs | [核心] | Agent 从自己的 session logs 中学习，团队级知识蒸馏 |
| 42:44 Tool Access and CLI First | [支撑] | 给 agent 完全访问权限，CLI 优先 |
| 44:14 UI Perception and Rasterizing | [支撑] | 将 UI 光栅化为图片帮助 agent 感知布局 |
| 45:07 Coordination Layer with Elixir | [支撑] | Elixir 的进程监督天然适配 agent 编排 |
| 46:57 Agent-Friendly CLI Output | [核心] | CLI 输出需要 token-efficient，只输出失败信息 |
| 49:15 Blueprint Spec and Guardrails | [支撑] | Symphony spec 是蓝图，不是静态规范 |
| 51:53 Trust Building with PR Videos | [支撑] | Agent 生成 PR demo 视频建立信任 |
| 53:59 Spark vs Reasoning Models | [支撑] | GPT-5.3 Spark 的定位：快速小修改 |
| 55:38 Current Model Limitations | [核心] | 模型仍不擅长从 0 到 1 的新产品和复杂重构 |
| 58:00 Frontier Enterprise Platform | [核心] | Frontier 产品愿景：企业级 agent 安全部署 |
| 1:00:11 Dashboards and Data Agents | [支撑] | 内部数据 agent 和语义层 |
| 1:03:13 Company Context and Memes | [支撑] | core_beliefs.md 包含团队信息；agent 生成 meme 的技能 |
| 1:07:21 Harness vs Training Tension | [核心] | harness 工程与模型训练之间的张力：on-policy harness |
| 1:09:08 Closing & Hiring | [连接] | Bellevue 办公室、Codex 200 万周活跃用户、招聘 |

---

## 📖 完整叙事

### 背景

Ryan Lopopolo 的职业背景横跨 Snowflake、Brex、Stripe、Citadel 等企业级产品公司，现在在 OpenAI 的 Frontier Product Exploration 团队，负责新产品开发——具体是在 OpenAI Frontier 这个企业平台上，探索如何将 AI agents 安全部署到企业中。他的团队被给予了"自由烹饪"的空间，这让他们得以进行一个极端实验。

### 第一部分：零代码实验的起源与代价 [2:47]

**核心约束**：Ryan 刻意设定了"自己不写任何一行代码"的约束。逻辑是：如果我们想让 agent 在企业中做有经济价值的工作，它就应该能做我能做的所有事情。经过 6-8 个月与 coding models 的工作，他认为模型已经"同构于我的能力"。

**惨痛的开始**：从最早版本的 Codex CLI + Codex Mini 模型开始，模型能力远不如今天。让模型构建一个产品功能，它根本无法组装各个部分。这定义了核心方法论：**当模型做不到时，打开任务，分解成更小的构建块，然后重新组装**。第一个半月是 10 倍慢于自己手写，但正因为付出了这个成本，最终建成了一个让 agent 能完成全部工作的"组装站"。

**模型代际变化**：从 GPT-5、5.1、5.2、5.3 到 5.4，每代模型都有不同的"性格"和工作方式，代码库需要适配。最关键的变化是 5.3 引入了 background shells——agent 可以在后台生成命令继续工作，但副作用是它变得"不耐心"，不愿意阻塞等待长构建。这迫使团队将整个构建系统从 Makefile → Bazel → Turbo → NX，直到构建时间降到一分钟以内。

### 第二部分：人类成为瓶颈 [7:46]

**核心转变**：模型是"天然可并行的"——有多少 GPU 和 token 就有多少工作能力。唯一真正稀缺的是人类团队的同步注意力。"一天只有这么多小时，我们需要吃午饭，我想睡觉。"

**系统思维方法论**：不断问三个问题——(1) Agent 在哪里犯错？(2) 我在哪里花时间？(3) 怎样才能不再花那些时间？然后为自动化建立信心。

**Review 的演进**：
- 早期：人类仔细审查每一行代码
- 中期：加入 agent code review。代码作者 agent 推上 PR → 审查 agent 发评论 → 指令要求代码 agent 至少回应反馈。但初期代码 agent 太容易被 reviewer "欺负"，导致来回振荡不收敛
- 解决方案：reviewer agent 被指示"偏向合并"、"不报告 P2 以上的问题"；代码 agent 被允许"推迟或反驳审查反馈"——就像人类 code review 中 FYI 性质的评论一样
- 最终状态：**post-merge review**。大部分人类 review 发生在合并之后。人类像管理 500 人工程组织的 group tech lead 一样，抽样查看代码推断趋势，不深入每个 PR

### 第三部分：编码工程品味为 Context [11:28]

**Agent.md 结构**：只有约 100 行的总目录表，加上多个小 skill 文件（core_beliefs.md、tech_tracker 等）。这种结构使得向仓库注入新内容来引导 agent 和人类变得非常便宜。

**Tech Tracker 和 Quality Score**：一个 markdown 表格形式的小脚手架，作为 Codex 的 hook——让它审查所有业务逻辑是否符合已定义的 guardrail，并为自己提出后续工作。在有 Linear 等 ticketing 系统之前，所有后续工作就用 markdown 文件中的笔记来跟踪。

**反脆弱式知识编码**：当收到一个 page（因为缺少超时），Ryan 在 Slack 上 @Codex 说："我要加一个超时修复这个，请更新我们的可靠性文档，要求所有网络调用都有超时。" 这样不仅做了当下修复，还**持久编码了关于"好"是什么的过程知识**。这些知识被注入给根 coding agent，也可以用来蒸馏测试或代码审查 agent。

**全面委托的 PR 生命周期**：调用一个 `$land` skill，指导 Codex 推 PR → 等人类/agent review → 等 CI 通过 → 修 flake → 合并上游 → 处理冲突 → 放入 merge queue → 处理 flake 直到进入 main。"完全委托"。

### 第四部分：非功能性需求 = Prompt Injection [23:47]

Ryan 对 Twitter 上一条评论的回应：所有编码进文档、测试、review agent 中的东西，本质上都是把构建高规模、高质量、可靠软件的**非功能性需求**放入了可以 "prompt inject" agent 的空间。

核心过程是：**从团队所有工程师的脑子里提取他们认为"好"是什么样的、他们默认会怎么做、他们会如何指导新人**——然后写下来。Agent 犯的每一个错误，都是"某个尚未写下来的非功能性需求"的信号。

### 第五部分：Ghost Libraries 和 Spec-Driven Software [29:36]

**Brett Taylor 的回应**：软件依赖正在消失——它们可以被 vendor 化。Ryan 100% 同意。当前可以内部化的依赖复杂度是"低到中"——几千行的依赖，一个下午就能内部化，而且可以只保留需要的部分。

**安全优势**：当 Codex Security 扫描仓库时，能以更低摩擦审查和修改内部化的依赖，而不用像推补丁到上游、等发布、检查传递兼容性那样麻烦。

**Ghost Libraries（幽灵库）**：分发软件的新方式——不分发代码，而是分发 spec。定义一个规范，指定 coding agent 在本地重建所需的一切细节。Symphony 就是这样发布的。具体流程：
1. 在私有仓库中有所有脚手架
2. 创建新仓库，让 Codex 以私有仓库为参考写 spec
3. 启动一个独立 Codex 实现 spec
4. 启动另一个 Codex 对比实现和上游，更新 spec 使其偏差更小
5. Ralph 式循环直到 spec 能高保真重建系统

**人们直接把博文链接喂给 Codex**说"让我的仓库变成这样"——效果出奇地好。

### 第六部分：Symphony — 无终端编排 [32:46]

**起源**：2024 年底团队每工程师每天 3.5 个 PR。GPT-5.2 发布后，上升到每人 5-10 个 PR/天。人类被频繁的 tmux 面板切换累垮了。所以再次问："怎样移除人类在 loop 中的存在？"

**Symphony 的核心**：一个 Elixir 编排层（模型自己选的语言，因为 Elixir 的 BEAM 虚拟机有天然的进程监督和 GenServer，非常适配 agent 任务编排）。每个任务启动一个小 daemon 驱动到完成。

**Rework 机制**：当 PR 不合格，整个 worktree 和 PR 被彻底丢弃，从零重做。在此之前需要反思"agent 哪里做得不好"，修复后再恢复进行。

**"我的生活在海滩"**：理想终态是每天打开 Linear 两次，对事项说 yes/no。Ryan 对代码几乎零投入感，"如果是垃圾就丢掉重做"。

**多人多 agent 的挑战**：仓库被架构成 500 个 NPM 包——对 7 人团队来说过度架构，但如果每人等于 10-50 个 agent，这种深度分解和接口边界就合理了。需要 45 分钟的每日站会来同步知识。

### 第七部分：Self-Improvement 和 CLI First [39:35]

**统一技能**：整个代码库只有 6 个 skill。如果某个 SDLC 环节没有覆盖，首先尝试编码进现有 skill——这样改变 agent 行为比改变人类行为更便宜。

**Skill 蒸馏（自我改进）**：
- 个人层面：让 Codex 分析自己的 session logs，告诉你如何更好地使用工具
- 团队层面：将所有人的 agent 轨迹汇入 blob storage，每天运行 agent 循环，找出"作为团队哪里可以做得更好"，反映回仓库。PR 评论、失败 build 都是信号——"agent 缺少 context"

**CLI First 理念**：
- "不要把 agent 放在盒子里——但给盒子里放满它需要的一切"
- 模型最擅长读文本和使用工具，CLI 是最高效的界面
- CLI 输出需要 token-efficient：`prettier --silent`（agent 不关心哪些文件已格式化，只想知道通过还是没通过）；PNPM recursive 的海量输出需要包装脚本只输出失败的测试
- 最小化云依赖，尽量本地运行（Prometheus 等开源工具）

**UI 感知**：agent 不像人类那样视觉感知 UI。它们看到的是 "red box button" 而不是红色方块。解决方案：将 UI **光栅化**为图片，然后同时提供图片和结构化描述，帮助模型更好地理解它操作的对象。

### 第八部分：当前模型局限与 Frontier 产品 [55:38]

**模型仍不擅长的领域**：
- **从 0 到 1 的新产品**：将 mock 翻译成可玩的产品仍需大量人类引导。"我自己也不擅长这个"——模型同构于人类，白空间项目中，人类自己头脑中缺的东西也是模型缺的
- **最复杂的重构**：分解单体等需要最多人类干预的工作。但每次模型升级都在推进复杂度边界，"不要赌模型不行"

**Frontier 产品愿景**：
- 企业级 AI 部署平台：可观测、安全、可控、可识别的 agent
- 接入公司原有 IAM、安全工具、工作空间工具
- Agents SDK：提供默认可用的 harness，从 Shell tool 到 Codex Harness 的所有能力
- 安全 spec 是企业定制的，提供 hook 让企业定义数据防泄漏规则、内部代号等
- Dashboard：多层级下钻，从全局到单个 agent 轨迹

**数据 Agent**：内部数据 agent 用 Frontier 技术让数据本体对 agent 可访问，理解数据仓库中的内容。这是构建超越 coding 的 agent 的关键——理解"什么是收入"、"什么是活跃用户"。

### 第九部分：Harness vs Training 的张力 [1:07:21]

**核心张力**：是投入更深的 harness，还是投入更深的训练让模型默认就能做更多？

**Ryan 的回答**：成功意味着模型获得更好的 taste（因为我们能指出方向），同时我们构建的东西不会主动降低 agent 性能。"我们做的本质上就是运行测试——运行测试本来就是写可靠软件的一部分。" 如果围绕 Codex 构建一个单独的 Rust 脚手架来限制输出，那才会是需要被丢弃的额外 harness。

**swyx 的 RL 类比**：这就像 on-policy vs off-policy。Ryan 的方法是构建 **on-policy harness**——已经在分布内，从那里修改。Off-policy 的 harness 没什么用。

---

## 🔑 关键洞察

- **"缺什么 Context？" 而非 "Try Harder"**：这是整篇文章最核心的方法论转变。当 agent 犯错，不要优化 prompt 或让它重试，而要问：缺了什么能力、上下文或结构？每个 agent 错误都是一个"尚未被文档化的非功能性需求"的信号。这将 agent 管理从"调教"转变为"系统设计"。

- **人类注意力是唯一真正稀缺资源**：Token 便宜到可以无限并行，但人类一天只有那么多小时。整个 harness engineering 的方法论可以归结为：识别人类在哪里花时间 → 构建自动化移除人类 → 对自动化建立信心。从 review 到 merge 到 debug，每一步的演进都遵循这个逻辑。

- **Agent-Legible Software（为 Agent 可读性设计的软件）**：就像你会为 TypeScript 全栈项目选择能跨前后端共享类型的架构一样，现在需要为 agent 选择最优的代码组织方式。500 个 NPM 包对 7 人团队过度设计，但对"每人等于 10-50 个 agent"的团队来说恰到好处。软件不再只为人类可读性而写。

- **Ghost Libraries / Spec-Driven 分发**：软件的分发方式正在改变——从"给你代码"变成"给你 spec，agent 在你本地重建"。这比开源更灵活（自动裁剪只保留你需要的部分）、比 SaaS 更可控（代码在你手里）。Symphony 本身就是这种方式发布的——它不是一个你要安装的库，而是一个 spec。

- **On-Policy Harness 原则**：harness 应该用模型自然产出的东西（代码、测试、CLI 输出）来引导，而不是在外面套一层限制系统。Ryan 的团队所有 guardrail 都是"原生于代码的"——文档、测试、lint 规则。这样当模型进步时，harness 不会成为阻碍，反而继续提供价值。这是"不赌模型不行"理念的实操体现。

- **反脆弱知识编码循环**：每次 incident → 修复问题 + 更新文档/guardrail → 下次 agent 不再犯同样的错。每个 PR 评论、失败 build、页面告警都是"agent 缺少 context"的信号，被收集起来用于团队级学习。这不是事后回顾，而是持续运转的反馈循环。

---

## 🤔 批判性思考

**1. "零人类代码"叙事的实际含义**

Ryan 非常坦诚地指出：这是在完全 greenfield 仓库上的实验，"不应该将其笼统推广"；产品是 Electron 桌面应用，不是基础设施级的高可用系统；仍有人类在 loop 中切 release branch 和做 smoke test。所以"0% human code, 0% human review"标题虽然吸引眼球，但实际上人类从"写代码"转变为"设计 context + 系统 + 做最终判断"。这种人类角色的转变比"零代码"本身更值得关注。评论区 richardstevenhack 的激烈反对（"post-merge review 不等于 0% review"、"45% AI 代码不安全"）虽然情绪化，但指向了一个真实问题：对于安全性要求极高的系统（金融基础设施、医疗等），这种方法论的适用边界在哪里？

**2. 第一个月"10 倍慢"的隐藏前提**

Ryan 承认前 1.5 个月比自己手写慢 10 倍。但他的团队有一个关键的不公平优势：OpenAI 内部无速率限制、最早获得每一代新模型、对 Codex 产品路线有直接影响力（skills 功能就是从他们的需求中产生的）。对于外部团队，"先慢 10 倍再快 5 倍"的投资回报需要在没有这些优势的情况下重新评估。此外，Ryan 本人有 Snowflake/Stripe/Citadel 级别的系统工程经验——他的"不写代码"实际上意味着"用 10 年经验设计 context"，这不是可以轻易复制的。

**3. Spec-Driven Distribution 的 Bootstrap 问题**

Ghost Library 概念很诱人——分发 spec 而非代码，agent 本地重建。但这依赖一个前提：实现 spec 的 agent 足够强大。Ryan 自己说"hard + new"象限仍需人类驱动。那么如果 spec 描述的系统恰好落在这个象限（大多数有价值的专业软件都是），ghost library 能否 work？此外，spec 的版本管理、演进、兼容性问题都还未被讨论。当 spec 自身需要被修改时（Ryan 说"the blueprint is meant to be vibed later"），如何确保多个独立重建的实例之间的一致性？这可能是一个全新的分布式系统问题。
