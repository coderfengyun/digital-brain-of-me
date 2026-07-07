# 每个任务一个 harness：Claude Code 中的动态工作流

**作者**: Thariq Shihipar、Sid Bidasaria — Anthropic Claude Code 团队  
**来源**: https://claude.com/blog/a-harness-for-every-task-dynamic-workflows-in-claude-code  
**日期**: 2026-06-02

---

Claude Code 现在可以即时编写并编排自己的多 agent harness。本文解释动态工作流如何运作，以及哪些模式最能发挥它们的价值。

上周，我们在 Claude Code 中发布了动态工作流。Claude 现在可以即时编写自己的 harness，为当前任务定制。

默认的 Claude Code harness 是为编码而构建的，但它也适用于许多其他类型的任务，因为很多任务其实都类似编码任务。不过，有些任务类别需要我们在 Claude Code 之上构建自定义 harness，才能达到最佳表现，例如 Research、安全分析、agent teams 或 Code Review。

工作流允许你在 Claude Code 之上动态创建 harness，让 Claude 更自然地解决这些问题。你也可以与他人分享和复用这些工作流。

在本文中，我会介绍自己对工作流的初步体验和经验，帮助你更充分地利用它。请记住，最佳实践仍在发展中：动态工作流通常会使用更多 token，更适合复杂、高价值的任务。

## 示例 prompt

在进入技术细节之前，我想先给出几个示例 prompt，帮助你开始想象工作流的可能性：

- “这个测试大约每 50 次运行会失败 1 次。设置一个工作流来复现它。围绕这个竞态条件形成相互竞争的理论，并且不要停止，直到有一个理论经受住证据检验。”
- “用一个工作流，查看我最近 50 个 session，挖掘我反复做出的纠正，并把反复出现的纠正转成 CLAUDE.md 规则。”
- “用一个工作流，翻查过去六个月 Slack 的 #incidents，找出反复出现但没人提交 ticket 的根因。”
- “拿我的商业计划跑一个工作流，让不同 agent 分别从投资人、客户和竞争对手视角拆解它。”
- “这里有一个包含 80 份简历的文件夹，用工作流为后端岗位排序，并复查前十名。用 AskUserQuestion 工具采访我，以建立 rubric。”
- “我需要给这个 CLI 工具起名。用一个工作流头脑风暴出一批选项，并通过锦标赛选出前三名。”
- “用一个工作流，把我们的 User model 在所有地方重命名为 Account。”
- “用一个工作流检查我的博客草稿，并对照代码库验证每一条技术声明。我不想发布错误内容。”

## 动态工作流如何工作

动态工作流会执行一个 JavaScript 文件，其中包含几个特殊函数，用于创建和协调 subagents。

动态工作流也包含标准 JavaScript 函数，例如 JSON、Math 和 Array，用于处理数据。

一个特别有用的点是：动态工作流可以决定某个 agent 使用哪个模型，以及 subagents 是否运行在自己的 worktree 中。这让 Claude 可以选择任务所需的智能水平和隔离程度。

如果工作流被中断，例如用户操作或退出终端，恢复 session 后工作流可以从中断处继续执行。

## 为什么需要动态工作流

当你要求默认 Claude Code harness 执行任务时，它需要在同一个上下文窗口中同时计划和执行。对于很多编码任务，这非常有效；但对于长时间运行、大规模并行、高度结构化和/或对抗性的任务，它可能会失效。

原因是：Claude 在单一上下文窗口中处理复杂任务的时间越长，越容易受到几种特定失效模式影响：

- **Agentic laziness** 指 Claude 在尚未完成特别复杂、多部分任务时就停止，并在只取得部分进展后宣布任务完成。例如，安全审查中 50 项只处理了 35 项。
- **Self-preferential bias** 指 Claude 倾向于偏好自己的结果或发现，尤其是在被要求依据 rubric 验证或评判这些结果时。
- **Goal drift** 指经过多轮对话后，对原始目标的忠实度逐渐下降，尤其是在 compaction 之后。每次摘要都会损失信息，边界条件或“不要做 X”这类约束可能会丢失。

创建工作流可以通过编排独立的 Claude subagents 来对抗这些问题。每个 subagent 都有自己的上下文窗口，以及聚焦、隔离的目标。

## 动态工作流 vs 静态工作流

你以前可能使用 Claude Agent SDK 或 `claude -p` 创建过静态工作流，用来协调多个 Claude Code 实例。

但因为静态工作流需要覆盖所有边界情况，它们通常更通用。借助 Claude Opus 4.8 和动态工作流，Claude 现在已经足够智能，可以为你的具体用例编写量身定制的 harness。

## 使用动态工作流的有用模式

你可以直接要求 Claude 创建一个动态工作流，也可以使用触发词 “ultracode” 来确保 Claude Code 创建工作流。

但建立一个关于动态工作流如何运作的心智模型，会帮助你理解什么时候该使用它们，以及如何通过 prompt 给 Claude 提示。

Claude 在构建工作流时可能会使用并组合几种常见模式：

### Classify-and-act

使用分类器 agent 判断任务类型，然后根据任务路由到不同 agent 或行为。也可以在最后使用分类器来确定输出。

### Fan-out-and-synthesize

把任务拆成许多更小的步骤，对每个步骤运行一个 agent，然后综合这些结果。当任务包含大量小步骤，或者每个步骤都受益于干净上下文窗口、避免互相干扰或交叉污染时，这尤其有用。综合步骤是一个 barrier：它等待所有 fan-out agents 完成，然后把它们的结构化输出合并为一个结果。

### Adversarial verification

对于每个创建出来的 agent，再运行一个独立创建的 agent，根据 rubric 或标准对其输出进行对抗性验证。

### Generate-and-filter

围绕一个主题生成多个想法，然后根据 rubric 或验证进行过滤，去除重复项，只返回质量最高、经过测试的想法。

### Tournament

不是拆分工作，而是让 agents 在同一任务上竞争。创建 N 个 agent，让它们用不同方法尝试同一任务。然后由 prompt 或模型通过 judging agent 以 pairwise 方式评判结果，直到得出胜者。

### Loop until done

对于工作量未知的任务，循环创建 agents，直到满足停止条件，例如没有新发现，或日志中没有更多错误，而不是固定运行若干轮。

## 用例

可以创造性地思考何时以及如何要求 Claude Code 创建动态工作流。我发现，工作流有时在非技术工作中甚至更有用。

### 迁移和重构

Bun 使用工作流从 Zig 重写为 Rust。你可以在 Jarred 的 X thread 中阅读更多相关内容。

关键是把任务拆成一系列需要操作的步骤，例如 callsites、失败测试、模块等。为每个修复在 worktree 中派生一个 subagent 来完成修复，然后让另一个 agent 进行对抗性审查，并合并它们。可以考虑告诉 agent 不要使用资源密集型命令，这样你可以最大程度并行化，同时避免耗尽本机资源。

### 深度研究

我们在 Claude Code 中发布了一个使用动态工作流的 deep research skill（`/deep-research`）。具体来说，它会 fan-out 网页搜索、获取来源、对声明进行对抗性验证，并综合成带引用的报告。

但这类研究不只适用于网页搜索。例如，可以要求 Claude 从 Slack 上下文编写状态报告，或通过深入探索代码库来研究某个功能如何运作。

### 深度验证

另一方面，如果你有一份报告，希望检查并溯源其中引用的每一条事实声明，可以生成一个工作流，让一个 agent 识别所有事实声明，然后为每条声明派生一个 subagent 进行详细检查。你也可以让一个 verification agent 检查 source subagent，确保其来源质量足够高。

### 排序

你可能有一组项目，希望按照某种 Claude Code 擅长评估的定性指标排序，例如按 bug 严重程度排序 support tickets。但如果你试图在一个 prompt 中排序 1000 多行，质量会下降，并且无法放进上下文。相反，可以运行 tournament、一条 pairwise-comparison agents 的 pipeline（比较判断比绝对评分更可靠），或者并行 bucket-rank 后再合并。每次比较都是自己的 agent，因此确定性循环负责持有 bracket，只有运行顺序留在上下文中。

### 记忆和规则遵循

如果你有一组特定规则，Claude 即使放进 CLAUDE.md 中也会漏掉或难以遵守，可以创建一个工作流，列出必须由 verifier agents 检查的规则，每条规则一个 verifier。创建一个 skeptic persona subagent 来审查这些规则是否合理，可以帮助避免过多假阳性。

反向流程也成立：挖掘你最近的 sessions 和 code review comments 中反复做出的纠正，用并行 agents 对它们聚类，对每个候选规则进行对抗性验证（这条规则是否本可以阻止真实错误？），然后把幸存下来的规则提炼回 CLAUDE.md。

### 根因调查

调试在提出多个独立假设并测试它们时效果最好。但如果只使用一个上下文窗口，Claude 可能会遇到 self-preferential bias。

工作流可以通过创建 agents 从互不重叠的证据中生成假设，结构性地防止这一点。例如，为日志、文件和数据分别设置 agents。每个假设随后都可以面对一组 verifiers 和 refuters。

这并不只适用于代码。工作流也可以用于销售（为什么三月销售下降？）、数据工程（为什么这条 pipeline 失败？），或任何事后复盘练习。

### 大规模分流

每个团队都有 support queue、bug reports 或其他无法由人类完全处理的 backlog。

分流工作流会对每个项目分类，与已跟踪事项去重，并采取行动。这可能意味着尝试修复，或升级给人类用户。

分流工作流中的一个有用模式是 quarantine。它禁止读取不可信公共内容的 agents 执行高权限操作；高权限操作改由负责基于信息行动的 agents 执行。

把分流工作流和 `/loop` 结合，可以让 Claude 持续执行。

### 探索和品味

当探索不同解决方案时，工作流会很有用，尤其是基于品味的任务，例如设计或命名，并且会受益于 rubric。

可以要求 Claude 探索一批方案，并给 review agent 一个关于好方案标准的 rubric。当 review agent 认为已经满足标准时，任务完成。方案也可以基于 rubric 通过 tournament 排序或选择。

### Evals

你可以为特定任务运行轻量级 evals：在 worktree 中派生独立 agents，然后派生 comparison agents，根据 rubric 比较并评分具体输出。例如，依据特定标准评估并改进你创建的 skill。

### 模型和智能路由

创建一个针对你的任务调优的 classifier agent，用来决定使用哪个模型。当任务会涉及大量工具调用，并且执行前的研究可以识别最合适模型时，这会很有帮助。

例如，对于“解释 auth 模块如何工作”这个任务，最佳模型取决于 auth 模块中有多少文件，以及代码库的形态。classifier agent 可以做这项研究，然后根据预期任务复杂度路由到 Sonnet 或 Opus。

## 何时不使用动态工作流

工作流是新事物。虽然它在许多用例中会带来超额结果，但并非每个任务都需要它，而且它最终可能会使用显著更多 token。

最好创造性地使用工作流，把 Claude Code 推向你之前未曾尝试过的方式。对于常规编码任务，试着问自己：它真的需要更多 compute 吗？例如，大多数传统编码任务并不需要一个由 5 个 reviewers 组成的 panel。

## 构建动态工作流的技巧

### Prompting

详细 prompting，并使用上文描述的具体技巧，会为动态工作流带来最佳结果。

工作流并不只适用于大型任务。你可以提示模型使用“quick workflow”。例如，可以对一个假设创建一次快速对抗性审查。

### 与 /goal 和 /loop 结合

在使用可重复运行的工作流时，例如分流、研究或验证，可以把它们与 `/loop` 配对以定期运行，并用 `/goal` 设置硬性完成要求。

### Token 使用预算

你可以为动态工作流设置明确的 token 使用预算，以限制任务使用多少 token。可以在 prompt 中设置预算，例如 “use 10k tokens”，这会设置上限。

### 保存和分享动态工作流

你可以在工作流菜单中按 “s” 保存工作流。可以把它们提交到 `~/.claude/workflows`，或通过 skill 分发。

要通过 skill 分享它们，把你的 JavaScript 工作流文件放到 skill 文件夹中，并在 `SKILL.MD` 中引用它们。为了保留更多灵活性，你可能希望提示 Claude 把 skill 中的工作流视为模板，而不是必须逐字运行的脚本。

## 发现的新起点

工作流是一种扩展 Claude Code 的有用新方式。我鼓励你把它们视为一个起点，用来探索使用 Claude 帮你完成任务的新方式。关于如何最好地使用它们，仍有许多东西有待发现。告诉我你发现了什么。

关于 harness 中首先应该包含什么原则，请参见我们关于使用 Claude 构建时的三种 harness design patterns。

本文由 Thariq Shihipar 和 Sid Bidasaria 撰写，他们是 Anthropic 负责 Claude Code 的技术团队成员。
