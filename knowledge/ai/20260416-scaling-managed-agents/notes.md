# Scaling Managed Agents: Decoupling the brain from the hands

**类型**: 叙事
**来源**: https://www.anthropic.com/engineering/managed-agents
**作者**: Lance Martin, Gabe Cemaj, Michael Cohen (Anthropic)

---

## 🗺️ 全局地图

### 一句话摘要
> Anthropic 借鉴操作系统"虚拟化硬件为抽象接口"的思想，将 agent 系统拆解为 brain（harness）、hands（sandbox）、session（事件日志）三个独立接口，使系统能在模型能力快速迭代时保持架构稳定。

### 段落分类

| 章节/段落 | 分类 | 一句话说明 |
|-----------|------|-----------|
| 开头：harness 编码的假设会过时 | [连接] | 引出问题——harness 中的假设随模型进步而失效 |
| context anxiety 例子 | [支撑] | 具体例子：Sonnet 4.5 的 context anxiety 在 Opus 4.5 上消失 |
| OS 虚拟化类比 | [核心] | 核心隐喻：像 OS 虚拟化硬件一样，虚拟化 agent 的组件 |
| 三大抽象定义（session/harness/sandbox） | [核心] | 定义 Managed Agents 的三个核心接口 |
| "Don't adopt a pet" — 耦合架构的问题 | [核心] | 讲述初始单容器架构的三个致命问题 |
| "Decouple the brain from the hands" — 解耦方案 | [核心] | 解耦后的架构设计：harness 离开容器、故障恢复、安全边界 |
| Session ≠ context window | [核心] | session 作为 context window 之外的持久化上下文对象 |
| Many brains, many hands — 规模化收益 | [核心] | 解耦带来的性能和扩展性收益（TTFT 下降 60%/90%） |
| Conclusion — meta-harness | [连接] | 总结：Managed Agents 是一个 meta-harness |
| Acknowledgements | [连接] | 致谢 |

---

## 📖 完整叙事

### 背景

Anthropic 工程博客此前已发布多篇关于 agent harness 设计的文章。一个反复出现的主题是：**harness 编码了对 Claude 能力局限的假设，但这些假设会随模型进步而失效**。

典型例子：Sonnet 4.5 在接近 context 上限时会过早结束任务（"context anxiety"），团队为此在 harness 中加入了 context reset。但当同样的 harness 用在 Opus 4.5 上时，这个行为已经消失了——reset 变成了死代码。这个现象直接呼应了 Rich Sutton 的 "Bitter Lesson"。

### 核心故事

**第一幕：单容器的"宠物"困境**

最初，Anthropic 将 session、harness、sandbox 全部放进一个容器。好处是简单——文件编辑就是 syscall，没有服务边界。但这创造了一个 "pet"（宠物服务器）：

1. **可靠性问题**：容器挂了 = session 丢失。容器卡了 = 必须进去救
2. **可观测性问题**：唯一的观察窗口是 WebSocket event stream，但它无法区分 harness bug、网络丢包还是容器宕机——所有故障看起来都一样。调试需要进入容器 shell，但容器里有用户数据，因此实际上无法调试
3. **连接性问题**：harness 假设所有资源都在本地容器内。当客户想连接自己的 VPC 时，要么做网络 peering，要么在客户环境跑 Anthropic 的 harness——一个 harness 内的假设变成了架构级约束

**第二幕：解耦——brain / hands / session 分离**

解决方案：将 "brain"（Claude + harness）从 "hands"（sandbox/tools）和 "session"（事件日志）中解耦。每个组件变成一个接口，可以独立失败和替换。

**Harness 离开容器**：harness 不再住在容器里，而是通过 `execute(name, input) → string` 调用容器，就像调用任何其他工具一样。容器变成了 cattle（牲畜）。容器死了？harness 捕获错误传给 Claude。Claude 决定重试？用 `provision({resources})` 启动新容器。

**Harness 自身也变成 cattle**：session log 在 harness 外部，harness 崩溃不丢状态。新 harness 用 `wake(sessionId)` 启动 → `getSession(id)` 获取事件日志 → 从最后一个事件恢复。运行中用 `emitEvent(id, event)` 持久化记录。

**安全边界**：在耦合架构中，Claude 生成的不可信代码和凭证在同一容器——prompt injection 只需让 Claude 读环境变量。解耦后，凭证永远不进入 sandbox：
- Git：用 access token 在初始化时 clone repo 并配置 remote，sandbox 内 push/pull 正常工作但接触不到 token
- 自定义工具：OAuth token 存在 secure vault，Claude 通过 MCP proxy 调用工具，proxy 用 session token 从 vault 取凭证——harness 本身也不知道凭证

### 关键转折

**Session ≠ context window**

长时间任务超出 context window 时，传统方案（compaction、context trimming、memory tool）都涉及**不可逆的决策**——难以预知未来需要哪些 token。

Managed Agents 的方案：session 是一个**活在 context window 之外的持久化上下文对象**。接口 `getEvents()` 允许 harness 按位置切片访问事件流——可以从上次停止处继续、倒回某时刻之前几个事件、或重新阅读特定操作前的上下文。

获取的事件在进入 context window 前可以在 harness 中做任意变换（prompt cache 优化、context engineering）。**关注点分离**：session 保证持久性和可查询性，harness 负责具体的 context 管理策略——因为无法预知未来模型需要什么样的 context engineering。

### 结果与意义

**Many brains**：harness 不在容器里 → 不需要容器的 session 也不用等容器启动。推理在编排层从 session log 拉取事件后立即开始。效果：**p50 TTFT 下降约 60%，p95 下降超过 90%**。扩展到多个 brain 只是启动多个无状态 harness。

**Many hands**：每个 hand 就是一个 `execute(name, input) → string` 接口——可以是容器、手机、甚至 Pokémon 模拟器。harness 不关心 sandbox 是什么。因为 hand 和 brain 不耦合，brain 之间可以传递 hand。

**Meta-harness 哲学**：Managed Agents 不是一个具体的 harness，而是一个 meta-harness——对接口有主张（session 操纵状态、sandbox 执行计算），对实现不做假设（brain 和 hands 的数量和位置）。Claude Code 是一个 harness，特定领域的 agent harness 也可以是——Managed Agents 能容纳所有这些。

---

## 🔑 关键洞察

| 论点 | 创新点 | 支撑数据 | 数据来源 | 说服力评估 |
|------|--------|----------|----------|------------|
| Harness 编码的假设会随模型进步失效 | 将 Bitter Lesson 应用到 agent 架构 | **例子**: Sonnet 4.5 有 context anxiety 需要 harness 加 reset，同一 harness 在 Opus 4.5 上 reset 变成死代码 | Anthropic 内部经验 | 强——一手经验，且问题具有普遍性 |
| 像 OS 虚拟化硬件一样虚拟化 agent 组件 | 用 OS 的 process/file 抽象类比 session/harness/sandbox | **例子**: `read()` 不关心底层是 1970s 的磁盘组还是现代 SSD；同理 `execute(name, input) → string` 不关心 sandbox 是容器还是 Pokémon 模拟器 | Unix 设计哲学 (Eric S. Raymond) | 强——类比精准，设计原则经过几十年验证 |
| 耦合架构产生"宠物"问题 | pets-vs-cattle 在 agent infra 中的体现 | **例子**: 容器故障时唯一观察窗口是 WebSocket event stream，无法区分 harness bug/网络丢包/容器宕机；调试需进入含用户数据的容器 | 内部运维经验 | 中强——真实痛点，但未给出故障频率等量化数据 |
| 凭证不应进入 sandbox | 结构性安全 vs. 权限收窄 | **例子**: Git token 在初始化时注入 remote 配置，sandbox 内 push/pull 正常但不接触 token；MCP OAuth token 存 vault，通过 proxy 取用 | 架构设计 | 强——解决了 prompt injection → 凭证泄露的根本问题，不依赖"Claude 不够聪明"的假设 |
| 解耦后 TTFT 大幅下降 | 延迟加载 sandbox | p50 TTFT 下降约 60%，p95 下降超过 90% | 生产数据 | 强——有明确的量化数据 |

---

## 🧠 批判性思考

### 1. 这篇文章最反直觉的观点是什么？

"不要为 agent 写最好的 harness，而是写一个能容纳未来所有 harness 的 meta-harness。" 

这反直觉是因为：工程团队的本能是优化当前方案，而不是抽象出接口层再在上面跑各种方案。但 Anthropic 的核心论证很有力——模型能力进步的速度使得任何"当前最优"的 harness 都会快速过时。这让问题从"怎么写好一个 harness"变成了"怎么设计一个架构让 harness 可以自由迭代"。

### 2. 这个设计有什么潜在的局限或未解决的问题？

1. **接口本身也会过时**：文章的核心假设是 `execute(name, input) → string` 和 `getEvents()` 这些接口足够通用，能在未来模型能力跃升时保持稳定。但如果未来模型需要的交互模式超出了"工具调用 + 事件日志"的范式（比如直接操控持续运行的进程、流式双向通信），这些接口也需要演化。文章承认了这个风险（"we're opinionated about the shape of these interfaces"）但没有深入讨论。

2. **Context engineering 的复杂性被推迟而非解决**：session 和 context window 的分离是优雅的，但"harness 负责具体的 context 管理策略"意味着核心难题（如何选择性加载 context）只是从一个地方搬到了另一个地方。对于真正长时间运行的任务，`getEvents()` 的位置切片可能不够——需要语义级检索。

3. **多 brain 协调**：文章提到 "brains can pass hands to one another"，但没有展开讨论多 brain 之间的协调问题——谁决定任务分配？共享 session 还是各自维护？状态一致性怎么保证？

### 3. 这篇文章对我的工作/思考有什么启发？

**对 agent 系统设计的启发**：
- **"假设会过时"是一个设计原则**：在设计任何与 LLM 交互的系统时，应该问"这个设计编码了哪些关于模型能力的假设？如果模型变强了，哪些部分会变成死代码？"
- **接口 > 实现**：Managed Agents 的核心不是具体的 harness 实现，而是 session/harness/sandbox 三个接口的定义。这和我在 digital-brain 系统中做的 data/skill 分离、progressive disclosure 是同一个思想——把稳定的（数据结构、接口定义）和易变的（处理逻辑、prompt 策略）分开
- **安全边界的结构性方案**：不要依赖"AI 不会做坏事"的假设来做安全，而是在架构上让凭证和不可信代码物理隔离。这对任何给 LLM 赋予执行能力的系统都适用
