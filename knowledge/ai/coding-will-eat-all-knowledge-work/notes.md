# Coding Will Eat All Knowledge Work

**类型**: 叙事
**作者**: Peter Yang（Roblox PM，Behind the Craft / Creator Economy newsletter 作者）
**访谈者**: Anish Acharya（a16z General Partner）
**来源**: a16z Show (YouTube) + Substack Note
**视频**: https://www.youtube.com/watch?v=UE8jx4dvlSQ （29 分钟）
**日期**: 2026-04-06

---

## 🗺️ 全局地图

### 一句话摘要
> Peter Yang 和 Anish Acharya 以 OpenClaw 实践为起点，讨论了 AI agent 时代的六个核心议题：个人 agent 的日常使用体验、agent 对 SaaS/App 生态的冲击、coding agents 的现状（Claude Code vs Codex）、"编程吞噬知识工作"的论点、未来公司形态（极致小团队）、以及 agent 对消费产品和经济的影响。

### 段落分类

| 章节（视频时间戳） | 分类 | 一句话说明 |
|-----------|------|-----------|
| 0:00 Intro | [连接] | 背景：Yang 和 Anish 在 Credit Karma 共事过 |
| 1:56 Using OpenClaw for voice, memory & daily life | [支撑] | 个人 agent 实践：语音交互、记忆系统、Telegram 集成 |
| 6:14 Will agents kill apps & SaaS? | [核心] | Agent 替代任务型 App；娱乐型 App 存活 |
| 11:57 Coding agents: Claude Code vs. Codex | [核心] | 两种 coding agent 的产品定位与体验差异；"coding 将吞噬所有知识工作" |
| 17:00 Future of work: small teams, agents & company culture | [核心] | 大公司的协调成本问题；2-3 人 + agents 的未来公司形态 |
| 24:00 How agents change consumer products & the economy | [核心] | Agent stack 正在浮现；消费产品商业模式变化；人类野心没有天花板 |

---

## 📖 完整叙事

### 背景

Peter Yang 和 Anish Acharya 曾在 Credit Karma 共事。Yang 现在有双重身份：白天是 Roblox 的 PM，业余是知名的 AI/创业 newsletter 作者和 YouTuber。他是 OpenClaw 的深度用户，同时重度使用 Claude Code 和 Codex。Anish 是 a16z 的 GP，从投资人视角看 AI 对各行业的影响。

### 第一部分：个人 Agent 的真实体验 [1:56]

**Yang 的 OpenClaw 使用方式：**
- 给 agent 取名 Zoe（原本想给女儿取的名字）
- **核心界面是 Telegram 语音**，70-80% 的使用是语音对话，而非写代码
- 接入了 YouTube analytics、Mercury 银行、Google Docs、日历、邮件（只读）
- 在 Telegram 上设了多个频道：一个随聊、一个做项目、一个公开 demo

**关于记忆系统的坦诚评价：**
- 默认的 memory.md 每日更新机制 "actually not that great"，agent 经常忘东西
- Yang 安装了一个三层记忆系统（含 Toby 的 QMD 搜索工具），2GB 存储，稍有改善
- 仍需在 agents.md 里写提醒："回答任何问题前先过一遍所有记忆"
- Agent 还经常忘记自己有什么能力："Can you update my Google Doc?" "Oh I can't do that." "Yes you can, it's in your file."

**个人 agent 的意义 — 不是功能，而是感觉：**
- "坦白说，这些事 Claude 或 ChatGPT 都能做。差别在于它装在 Telegram 里，感觉更 personal"
- "我在床上跟它发消息，通勤时跟它语音，它 feels more like an actual human"
- 经典故事：散步时 Zoe 给了一段 3 分钟的 pep talk——"你一直在聊事业，但你的孩子 7 岁和 4 岁，很快就不想跟你玩了，你应该优先陪他们"

### 第二部分：Agent 会杀死 App 和 SaaS 吗？ [6:14]

**Yang 的观察：**
- 接入 Mercury MCP 等之后，"I don't actually open those apps much anymore"
- **分化规则**：完成任务的 App（Mercury, Workspace）→ 使用减少；消费注意力的 App（X/Twitter）→ 不受影响
- "你相当于有了一个非常好的 admin 替你做事"

**Anish 的补充 — 感觉驱动的 App 使用：**
- 人们打开 App 是为了 **feel a feeling**：WhatsApp = 连接感，Slack = 效率感，TikTok = 娱乐感
- 如果只有一个 agent，如何做 context switching？Yang 的解法：Telegram 多频道

**SaaS 替代的现实案例：**
- Yang 提到一家 AI-native 创业公司（vibe coding 领域），让 vibe coders 构建内部工具替代他们付费的 SaaS
- Anish 的反驳：Calendly 才 $20/月，你真的想自己维护一个 Calendly 吗？除非你雇专人做 vibe code，但那个成本可能还不如直接买 SaaS

**关于 Figma 的讨论：**
- Yang：设计师需要学写代码，否则几年后会过时
- Anish 的反驳（重要洞察）：**Thinking tools vs Making tools**。IDE 以前是 making tool（执行场所），现在正变成 thinking tool（思考场所）。"我经常先用最笨的方式让 agent 做一遍，然后让它总结'你会怎么做得更好'，再回到起点重做。" Figma 兼具设计执行和设计思考两个功能，这是它在新 stack 中保持相关性的机会。

### 第三部分：Coding Agents — Claude Code vs Codex [11:57]

**Yang 的分类：**
- **Codex**：想认真做东西时用，thinking harder，更准确，但延迟高，难进入 flow state
- **Claude Code**：vibing 时用，"it's almost like a slot machine"，每次结果不同，很 addictive

**Anish 的 slot machine 理论（精彩观点）：**
- 类比社交网络时代的 **variable scheduled rewards**——打开 Facebook feed，偶尔无聊无聊然后突然一个超棒的内容
- Coding agents 有完全一样的属性，而且**时间也是 variable 的**——有时 1 秒出结果，有时 5 分钟
- 这种 variable time + variable reward 给了它"赌场般的感觉"

**产品策略差异：**
- Codex：产品自解释
- Claude Code：需要自己定制（hooks, skills, plugins），"如果你不刷 X 就完全不知道怎么定制"，但定制后 "you feel like it's part of you"，很难切换
- Claude Code 的 harness 优势：截图直接粘贴、语音输入、连接 Chrome；Codex 都还没做

**"Coding will eat all knowledge work" 的完整论述 [约 15:00]：**
- Yang："I feel like interesting that software will eat the world. I feel like coding will eat all knowledge work."
- 具体例子：Lovable 刚发布了支持做 slides 的功能。"I don't want to use PowerPoint anymore. I hate writing Google Docs."
- Yang 写博客的方式已经变了：用 Claude Code 给反馈让它写，AI 做 80%，自己 tweak 最后 20%，"I never start from zero."
- Anish 的 Excel 类比（引 Satya Nadella）：Excel 是全球最流行的编程语言，1亿+ 人在用，但没人觉得自己在编程。Coding agents 将是这个概念的千倍放大——连"写 Google Docs"这种主观感觉的工作都可以在 coding 领域里更高效地完成。
- Yang 的回应：Excel 流行是因为 approachable，现在代码被抽象掉了，"you're just talking to some agent and getting it to do stuff"

### 第四部分：未来公司形态 [17:00]

**Yang 的"hot take"：**
- "公司越大，工作体验越差。因为要 align 太多人了。"
- 回忆在 Credit Karma 的 OKR 会议：3 小时坐在房间里讨论 OKR，"this is a waste of my life"
- 期望：更多公司保持小规模。2-3 人产品团队 + agents，取代 10 人团队
- "跟 agents 对齐和跨团队 launch 比跟人类容易多了"

**Anish 的延伸 — Agent 去除情绪因素：**
- "想象你的 agent 和我的 agent 去谈判，得出结论后双方都不会有情绪。Very objective."
- 提升 "work NPS"：回顾人类历史——公元前 1 万年别被狮子吃、100 年前别被工厂机器压死、现在别被 50 条 Slack thread 的 VP 争吵消耗。Agent 可以处理这些高情绪的协调工作。

**关于速度 vs 深思：**
- Yang：AI 工具让人很容易同时朝 10 个方向冲，有时需要慢下来想清楚方向。但传统年度规划已经不 work 了。
- Anish 的 **hill climbing 框架**（引 Hiten Shah 的讨论）：爬到一个 local maxima 的底部后，应该用 agents 极速冲顶（fully express the insight）；但要找到下一个 hill，得停下来，"go touch grass"。**未来的工作节奏是 fast 和 slow 的交替**。

**PM 的未来：**
- "我认识的所有 PM 晚上和周末都在学写代码"
- PM 的核心技能（跟用户聊、定义问题）仍然重要，但还要学会自己 prototype
- Yang 对孩子的计划："高中就开始做 bootstrapped business，跳过大学和公司生涯"
- Anish：以前非程序员孩子想创业的唯一渠道是做 YouTuber，现在可以做任何东西

### 第五部分：Agent 改变消费产品与经济 [24:00]

**产品界面的双层结构：**
- Agent 通过 API 处理事务性操作
- 人类通过消费型界面（feed）浏览和消费内容
- 两者共存："maybe people will do both"，像 Credit Karma 用户有时看信用分，有时让 agent 自动优化

**商业模式的简化（Anish 的重要观察）：**
- 过去消费产品复杂化（retention, engagement, whales, ads）是因为不直接收费
- AI 时代消费者愿意付费，而且有 consumption-based revenue（token 付费）
- 同时有真实的 inference 成本 → "day one 就必须向客户收费"
- 这种商业模式简化会改善很多传统消费产品的问题

**100% 自动化 vs 效率提升：**
- Anish 从投资角度看：能做到 100% 自动化的岗位（如客服：Decagon, Sierra）非常稀少
- 大多数 AI 产品能提供巨大效率提升，但最后 5% 仍需人类完成
- 效率提升的结果可能不是更少的工作，而是"European style 四天工作周"或公司效率翻倍

**经济形态变化，不是萎缩：**
- Yang：大公司裁员 → 更多 solopreneurs 和小公司
- Anish：**"I don't think there's going to be less jobs. Human ambition has no ceiling. Human desire has no ceiling."** 随便读一本科幻小说就知道，人类的需求远没有到顶。
- Yang 引用推文："The job market is so bad that I can only pursue my dreams now"

**Agent Stack 正在浮现：**
- Identity, payments, marketing, CLI vs MCP — "all of these are really new things, the old playbook goes away"
- Yang：2025 年觉得 agents 过度炒作，现在觉得真的来了
- Anish 对 "agent" 一词的吐槽：太 overloaded 了，"can we just say model in a loop? Model that uses tools in a loop." 但没人喜欢听这个，agent 听着更 flashy

---

## 🔑 关键洞察

- **"编程"的重新定义**：这里的 coding 不是写 Python/Java，而是指**用自然语言指挥 agent 完成任务**的能力。当所有知识工作都可以被 agent 执行时，"编程"就变成了最通用的 meta-skill——你在编排（orchestrate）而不是执行（execute）。Excel 用户不觉得自己在编程，但他们确实在用结构化指令操控数据。Coding agents 是这个逻辑的千倍放大。

- **Thinking tools vs Making tools（Anish 的框架）**：IDE 从 making tool 变成 thinking tool。"用最笨的方式先做一遍，让 agent 总结教训，再回到起点重做。" 这改变了 Figma 等设计工具的存亡逻辑——如果你同时是 thinking tool，你就不会被 agent 替代。

- **Coding agents 的 slot machine 效应**：Variable reward（每次结果不同）+ Variable time（1 秒到 5 分钟不等）= 赌场般的 addictive 体验。这解释了为什么人们能连续几小时 vibe code。

- **协调成本 > 执行成本**：大组织的真正瓶颈不是"干活的人不够"，而是"决定干什么"的过程太慢。Agent 最大的杠杆是去除协调中的情绪因素——让 agent 代表你去谈判，结果是客观的，没有 50 条 Slack thread 的 VP 内斗。

- **Fast/Slow 交替的工作节奏（Anish 的 hill climbing 框架）**：找到一个 local maxima → 用 agents 极速冲顶 → 停下来 touch grass → 找到下一个 hill。不是永远快，也不是年度规划式的慢。

- **Agent 从工具到伙伴的跃迁**：Yang 的 OpenClaw 提醒他关注孩子的故事，暗示 agent 的终局不是更高效的工具，而是更深刻理解你的伙伴。但现实很 janky——记忆系统不好用，agent 忘记自己的能力，需要用户不断提醒。

---

## 🤔 批判性思考

**1. "80% 由 AI 完成"的边界在哪里？**

Yang 说知识工作的前 80% 可以交给 AI，自己只做 20% 打磨。但他自己也承认使用场景主要是写博客、拉 analytics、做网站等偏模板化的工作。涉及利益相关方政治的战略文档、需要深度领域专业知识的分析、或者需要反复沟通达成共识的文件，AI 能完成的比例可能远低于 80%。有趣的是，Anish 作为投资人看到的数据也支持这一点：大多数 AI 产品能提供巨大效率提升，但 100% 替代一个 job function 的案例（如客服自动化）仍然非常稀少。

**2. OpenClaw 的真实体验 vs 叙事**

Yang 非常坦诚地承认 OpenClaw 还很 janky：记忆系统不好用、agent 经常忘事、忘记自己的能力、延迟大。他说 70-80% 的使用就是语音聊天，大多数功能用 Claude 或 ChatGPT 也能做。他自己承认核心差异是**界面和感觉**（Telegram 里更 personal），而不是能力层面的突破。这提示我们：当前阶段 personal agent 的价值可能更多在于心理层面的拟人化体验，而非功能上的不可替代性。

**3. "小团队+agent" vs Anish 自己的反驳**

这个对话中最有价值的 tension 在于 Anish 既支持小团队论点，又不断提供反驳：Calendly 才 $20/月 为什么要自己维护？100% 自动化的岗位极为稀少，大多数效率提升不意味着更少的工作。他的 hill climbing 框架也暗示：小团队适合在一个已知方向上快速冲刺，但**找到正确方向**本身可能需要更多元的视角和更深入的讨论——恰恰是大团队/多元团队擅长的。
