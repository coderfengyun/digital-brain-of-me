# YC掌门人60天写了60万行代码，一个人干20人的活，他把方法论全开源了

> 来源：AI寒武纪公众号 | 2026年3月20日
> 原文链接：https://mp.weixin.qq.com/s/-kJeOfYHMvetALarZOuZFw

Y Combinator总裁兼CEO Garry Tan，最近做了一件事。

过去60天，他写了超过60万行生产代码，其中35%是测试代码。这是他在完成全部CEO职责的同时，作为日常工作的一部分完成的。

他最近7天的开发数据：三个项目合计新增14万751行代码，362次提交，净增约11.5万行。每天可用代码产出在1万到2万行之间。

他把这套方法论整理成了一个开源工具，叫做 **gstack**。

github: https://github.com/garrytan/gstack

## 从772到1237

Garry Tan 2013年在YC内部构建社交网络Bookface时，全年代码贡献数是772次。

2026年，这才3月份，他的贡献数已经达到1237次，还在增长。

同一个人，不同时代，差距来自工具。

## gstack是什么

gstack的核心逻辑是：把Claude Code变成一支你可以真正管理的虚拟工程团队。

它包含15个专家角色和6个增强工具，全部以斜杠命令的形式调用，全部用Markdown编写，MIT协议，免费开源，现在就能用。

这15个角色分别是：

**流程类（按Sprint顺序排列）：**

- `/office-hours`：产品重构。在你写一行代码之前，重新定义问题本身
- `/plan-ceo-review`：CEO视角。找出需求里隐藏的更好产品，支持扩展、收缩、维持范围四种模式
- `/plan-eng-review`：工程负责人。锁定架构、数据流、边界情况和测试方案，把隐藏假设逼出来
- `/plan-design-review`：资深设计师。对每个设计维度0-10打分，说明满分是什么样，然后修改方案达到满分。带AI低质量内容检测
- `/design-consultation`：设计合伙人。从零构建完整设计系统，提出创意风险，生成真实产品原型图
- `/review`：Staff工程师。找到通过CI但会在生产环境爆炸的bug，自动修复明显问题，标记完整性缺口
- `/investigate`：调试专家。系统性根因分析。铁律：不调查不修复。追踪数据流，验证假设，3次修复失败后停止
- `/design-review`：会写代码的设计师。与/plan-design-review审计方式相同，然后修复发现的问题，原子提交，前后对比截图
- `/qa`：QA负责人。测试应用、找bug、原子提交修复、重新验证，为每个修复自动生成回归测试
- `/qa-only`：QA报告员。与/qa方法相同，但只出报告，不改代码
- `/ship`：发布工程师。同步主分支、跑测试、审计覆盖率、推送、开PR，一条命令
- `/document-release`：技术写作。更新所有项目文档，自动发现过时的README
- `/retro`：工程负责人。团队维度的周度复盘，包含个人数据、发布连续性、测试健康趋势
- `/browse`：QA工程师。给AI代理装上眼睛，真实Chromium浏览器，真实点击，真实截图，约100毫秒每个命令
- `/setup-browser-cookies`：会话管理。把Chrome、Arc、Brave、Edge的cookie导入无头浏览器会话

**增强工具类：**

- `/codex`：第二意见，来自OpenAI Codex CLI的独立代码审查，三种模式：审查（通过/不通过）、对抗性挑战、开放咨询
- `/careful`：安全护栏，在执行rm -rf、DROP TABLE、强制推送等破坏性命令前发出警告
- `/freeze`：编辑锁定，把文件编辑限制在一个目录内，调试时防止意外改动范围外的代码
- `/guard`：完整安全，/careful加/freeze合并成一条命令
- `/unfreeze`：解除/freeze限制
- `/gstack-upgrade`：自我更新，升级gstack到最新版本

## 一次典型Sprint的样子

你说：我想做一个日历日报应用。

你运行 `/office-hours`。

Claude不接受这个表述。它问你具体的痛点，不要假设场景。你说：多个Google日历，活动信息过时，地点有误，准备要花很长时间，结果还不够好。

Claude说：我要质疑你的表述框架。你说的是日报应用，但你描述的其实是一个个人首席助理AI。然后它提取了5个你没意识到自己在描述的能力，挑战了4个前提假设，生成了3种实现方案和工作量估算，并给出建议：明天先交付最小可用版本，完整愿景是3个月的项目，从真正能用的日报功能开始。

它写出一份设计文档，自动流入下游所有技能。

你运行 `/plan-ceo-review`，审查范围，运行10个维度的评估。

你运行 `/plan-eng-review`，得到数据流ASCII图、状态机、错误路径、测试矩阵、故障模式、安全问题。

你批准方案，退出规划模式。

8分钟内，11个文件，2400行代码写完。

你运行 `/review`，2个问题自动修复，1个竞态条件你手动确认修复。

你运行 `/qa`，打开真实浏览器，点击每个流程，发现并修复1个bug。

你运行 `/ship`，测试从42个增加到51个，PR开出来了。

8条命令。

## 并行运行10到15个Sprint

gstack单个Sprint已经很强。同时跑10个才是真正的变化。

Garry Tan用一个叫Conductor的方式，把多个Claude Code会话并行运行在各自隔离的工作区里。一个会话对新想法运行/office-hours，另一个对PR运行/review，第三个实现某个功能，第四个对Staging跑/qa，还有六个在其他分支上跑。同时进行。他常规会同时运行10到15个Sprint，这也是目前的实际上限。

让并行运行能够工作的是Sprint结构本身。没有流程，十个代理是十个混乱来源。有了流程——思考、规划、构建、审查、测试、发布——每个代理知道自己该做什么、什么时候该停下来。管理它们的方式和CEO管理团队的方式一样：在重要的决策上介入，其余的让它们跑。

## 几个值得单独说的能力

**QA让并行能力翻倍。**
/qa让他从6个并行工作流扩展到12个。Claude Code说出"我看到问题所在"，然后真的修复它、生成回归测试、验证修复，这改变了工作方式。代理现在有眼睛了。

**设计贯穿整个系统。**
/design-consultation不只选字体。它研究你所在领域的现状，提出保守选择和创意风险，生成真实产品的原型图，写出DESIGN.md，然后/design-review和/plan-eng-review都会读取你的选择。设计决策流经整个系统。

**文档不再滞后。**
/document-release读取项目里每个文档文件，交叉对比diff，更新所有漂移的内容——README、架构文档、CONTRIBUTING、CLAUDE.md、TODO全部自动更新。/ship现在会自动调用它，不需要额外命令。

**AI卡住时的浏览器交接。**
遇到验证码、认证墙或MFA？浏览器交接功能会在同一页面打开一个可见的Chrome窗口，带上所有cookie和标签页。你解决问题，告诉Claude完成了，它从原地继续。代理在连续失败3次后会自动建议这个操作。

**双AI交叉审查。**
/codex让OpenAI的Codex CLI对同一个diff做独立审查。当/review（Claude）和/codex（OpenAI）都审查过同一个分支，你会得到一份交叉分析，显示哪些发现两个模型都有，哪些是各自独有的。

**主动建议下一步。**
gstack判断你所处的阶段——头脑风暴、审查、调试、测试——并建议合适的技能。不需要的话，说"停止建议"，它会跨会话记住。

## 安装

需要：Claude Code，Git，Bun v1.0及以上版本。

**第一步：安装到本机（约30秒）**

打开Claude Code，粘贴以下内容，Claude完成剩余操作：

```
Install gstack: run git clone https://github.com/garrytan/gstack.git ~/.claude/skills/gstack && cd ~/.claude/skills/gstack && ./setup then add a "gstack" section to CLAUDE.md that says to use the /browse skill from gstack for all web browsing, never use mcp__claude-in-chrome__* tools, and lists the available skills: /office-hours, /plan-ceo-review, /plan-eng-review, /plan-design-review, /design-consultation, /review, /ship, /browse, /qa, /qa-only, /design-review, /setup-browser-cookies, /retro, /investigate, /document-release, /codex, /careful, /freeze, /guard, /unfreeze, /gstack-upgrade. Then ask the user if they also want to add gstack to the current project so teammates get it.
```

**第二步（可选）：添加到项目仓库，让团队成员共享**

```
Add gstack to this project: run cp -Rf ~/.claude/skills/gstack .claude/skills/gstack && rm -rf .claude/skills/gstack/.git && cd .claude/skills/gstack && ./setup then add a "gstack" section to this project's CLAUDE.md that says to use the /browse skill from gstack for all web browsing, never use mcp__claude-in-chrome__* tools, lists the available skills: /office-hours, /plan-ceo-review, /plan-eng-review, /plan-design-review, /design-consultation, /review, /ship, /browse, /qa, /qa-only, /design-review, /setup-browser-cookies, /retro, /investigate, /document-release, /codex, /careful, /freeze, /guard, /unfreeze, /gstack-upgrade, and tells Claude that if gstack skills aren't working, run cd .claude/skills/gstack && ./setup to build the binary and register skills.
```

实际文件会被提交到仓库（不是子模块），git clone直接可用。所有内容都在.claude/目录内，不会修改PATH，不会在后台运行任何东西。

## 现在，还是以后

模型在快速变好。现在真正搞懂怎么和它们协作的人，会有巨大优势。

gstack是免费的，MIT协议，开源，现在就能用，没有付费版，没有等待名单。

详细信息: https://github.com/garrytan/gstack
